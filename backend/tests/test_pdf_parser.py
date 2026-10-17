"""
Automated tests for PDF Parser module.
Tests:
- Valid Invoice text extraction
- Valid Bill of Lading (BOL) text extraction
- Word and character metrics
- In-memory bytes vs file path extraction
- Scanned / empty PDF detection (OCR requirement)
- Empty bytes handling
- Missing file handling
- Corrupted file error handling
- Page numbering validation
"""
import pytest
from backend.app.pdf_parser import (
    PDFParser,
    PDFExtractionResult,
    CorruptedPDFError,
    EmptyPDFError,
    ScannedPDFError,
)

SAMPLE_INVOICE_PATH = "samples/sample_invoice.pdf"
SAMPLE_BOL_PATH = "samples/sample_bol.pdf"
BLANK_PDF_PATH = "samples/blank_sample.pdf"


def test_extract_text_from_valid_invoice():
    """Verify that a valid text-based invoice PDF extracts expected text and metadata."""
    result = PDFParser.extract_text(SAMPLE_INVOICE_PATH)
    
    assert isinstance(result, PDFExtractionResult)
    assert result.page_count == 1
    assert result.char_count > 100
    assert result.word_count > 20
    assert result.requires_ocr is False
    
    # Check that key textual elements are present
    assert "INV-2024-0042" in result.raw_text
    assert "Apex Industrial Supplies" in result.raw_text
    assert "Nexus Logistics" in result.raw_text
    assert "$1,154.53" in result.raw_text


def test_extract_text_from_valid_bol():
    """Verify that a valid Bill of Lading PDF extracts expected shipping fields."""
    result = PDFParser.extract_text(SAMPLE_BOL_PATH)
    
    assert isinstance(result, PDFExtractionResult)
    assert result.page_count == 1
    assert result.requires_ocr is False
    
    # Check key BOL shipping data points
    assert "BOL-ONEY-8829103" in result.raw_text
    assert "Orient Global Manufacturing" in result.raw_text
    assert "Pacific Imports & Distribution" in result.raw_text
    assert "EVER FORWARD" in result.raw_text
    assert "ONEU9876543" in result.raw_text
    assert "8,450.00 KGS" in result.raw_text


def test_extract_text_from_bytes():
    """Verify that passing raw bytes produces the same result as passing a filepath."""
    with open(SAMPLE_INVOICE_PATH, "rb") as f:
        pdf_bytes = f.read()

    result = PDFParser.extract_text(pdf_bytes)
    assert result.page_count == 1
    assert "INV-2024-0042" in result.raw_text


def test_scanned_or_blank_pdf_raises_ocr_error():
    """Verify that a document with no text raises ScannedPDFError when strict_ocr_check is True."""
    with pytest.raises(ScannedPDFError) as exc_info:
        PDFParser.extract_text(BLANK_PDF_PATH, strict_ocr_check=True)
    
    assert "Optical Character Recognition (OCR) is required" in str(exc_info.value)


def test_scanned_or_blank_pdf_flag_when_not_strict():
    """Verify that strict_ocr_check=False sets requires_ocr=True instead of raising an error."""
    result = PDFParser.extract_text(BLANK_PDF_PATH, strict_ocr_check=False)
    assert result.requires_ocr is True
    assert result.char_count < PDFParser.MIN_CHAR_THRESHOLD


def test_corrupted_file_raises_corrupted_pdf_error():
    """Verify that non-PDF or truncated bytes trigger CorruptedPDFError."""
    garbage_bytes = b"This is definitely not a PDF file format."
    with pytest.raises(CorruptedPDFError):
        PDFParser.extract_text(garbage_bytes)


def test_empty_bytes_raises_empty_pdf_error():
    """Verify that 0-byte input raises EmptyPDFError."""
    with pytest.raises(EmptyPDFError) as exc_info:
        PDFParser.extract_text(b"")
    assert "0 bytes" in str(exc_info.value)


def test_missing_file_raises_filenotfound():
    """Verify that non-existent file path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        PDFParser.extract_text("samples/non_existent_document.pdf")


def test_page_numbers_are_sequential():
    """Verify that page objects have 1-indexed sequential numbering."""
    result = PDFParser.extract_text(SAMPLE_INVOICE_PATH)
    assert len(result.pages) > 0
    for idx, page in enumerate(result.pages):
        assert page.page_number == idx + 1
