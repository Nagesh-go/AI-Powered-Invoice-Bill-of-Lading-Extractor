"""
PDF Parsing Module using pypdf.

Extracts text from text-based PDF documents, validates page content,
and detects when a document is empty, corrupted, or scanned (requiring OCR).
"""
import io
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union, BinaryIO
from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)


class PDFParsingError(Exception):
    """Base exception for all PDF parsing errors."""
    pass


class CorruptedPDFError(PDFParsingError):
    """Raised when the PDF file is corrupted or not a valid PDF format."""
    pass


class EmptyPDFError(PDFParsingError):
    """Raised when the PDF contains 0 pages or has zero readable content."""
    pass


class ScannedPDFError(PDFParsingError):
    """Raised when the PDF contains pages, but no extractable text characters (scanned document)."""
    pass


@dataclass
class PageText:
    """Represents text extracted from an individual page."""
    page_number: int
    text: str
    char_count: int


@dataclass
class PDFExtractionResult:
    """Complete result of a PDF text extraction process."""
    raw_text: str
    page_count: int
    char_count: int
    word_count: int
    pages: List[PageText] = field(default_factory=list)
    requires_ocr: bool = False


class PDFParser:
    """
    Parser for extracting text from text-based PDFs.
    
    Minimum character threshold: if total extracted characters across all pages
    is less than MIN_CHAR_THRESHOLD, the document is considered scanned or lacking text.
    """
    MIN_CHAR_THRESHOLD: int = 30

    @classmethod
    def extract_text(
        cls,
        source: Union[str, Path, bytes, BinaryIO],
        strict_ocr_check: bool = True
    ) -> PDFExtractionResult:
        """
        Extract text from a PDF source (filepath, bytes, or file-like stream).

        Args:
            source: File path (str/Path), raw PDF bytes, or file-like BinaryIO stream.
            strict_ocr_check: If True, raises ScannedPDFError when text is below threshold.
                              If False, returns PDFExtractionResult with requires_ocr=True.

        Returns:
            PDFExtractionResult with extracted text, page metrics, and OCR status.

        Raises:
            FileNotFoundError: If a file path is provided but does not exist.
            EmptyPDFError: If the input is 0 bytes or the PDF has 0 pages.
            CorruptedPDFError: If file is malformed, encrypted without password, or not a PDF.
            ScannedPDFError: If strict_ocr_check=True and extracted text is below threshold.
        """
        # 1. Handle file paths
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.is_file():
                raise FileNotFoundError(f"PDF file not found at path: {source}")
            stream = str(path)
        # 2. Handle raw bytes
        elif isinstance(source, bytes):
            if len(source) == 0:
                raise EmptyPDFError("Uploaded file is 0 bytes (empty).")
            stream = io.BytesIO(source)
        # 3. Handle file-like streams
        else:
            stream = source

        try:
            reader = PdfReader(stream)
        except (PdfReadError, Exception) as exc:
            logger.error(f"Failed to read PDF: {exc}")
            raise CorruptedPDFError(f"Invalid or corrupted PDF file: {exc}") from exc

        # Check for encrypted PDFs
        if reader.is_encrypted:
            try:
                decrypted = reader.decrypt("")
                if decrypted == 0:
                    raise CorruptedPDFError("PDF is password protected and cannot be read.")
            except Exception as exc:
                raise CorruptedPDFError(f"Failed to decrypt PDF: {exc}") from exc

        page_count = len(reader.pages)
        if page_count == 0:
            raise EmptyPDFError("The PDF document contains 0 pages.")

        pages_extracted: List[PageText] = []
        full_text_chunks: List[str] = []
        total_chars = 0

        for idx, page in enumerate(reader.pages):
            page_num = idx + 1
            try:
                page_text = page.extract_text() or ""
            except Exception as exc:
                logger.warning(f"Error extracting text from page {page_num}: {exc}")
                page_text = ""

            cleaned_text = page_text.strip()
            char_count = len(cleaned_text)
            total_chars += char_count

            pages_extracted.append(
                PageText(
                    page_number=page_num,
                    text=cleaned_text,
                    char_count=char_count
                )
            )

            if cleaned_text:
                full_text_chunks.append(f"--- PAGE {page_num} ---\n{cleaned_text}")

        full_raw_text = "\n\n".join(full_text_chunks).strip()
        word_count = len(full_raw_text.split()) if full_raw_text else 0

        # Detect scanned document or document with no extractable text
        is_scanned = total_chars < cls.MIN_CHAR_THRESHOLD

        if is_scanned and strict_ocr_check:
            raise ScannedPDFError(
                f"No extractable text found in {page_count}-page document ({total_chars} characters detected). "
                "This document appears to be a scanned image or empty. Optical Character Recognition (OCR) is required."
            )

        return PDFExtractionResult(
            raw_text=full_raw_text,
            page_count=page_count,
            char_count=total_chars,
            word_count=word_count,
            pages=pages_extracted,
            requires_ocr=is_scanned
        )
