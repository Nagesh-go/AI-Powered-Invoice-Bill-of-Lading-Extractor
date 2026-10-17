"""
Document Extraction Pipeline Orchestrator.

Orchestrates the end-to-end extraction lifecycle:
1. PDF text extraction & OCR detection (pypdf)
2. Document type classification (Heuristic/Keyword)
3. Schema selection & LLM extraction (Google Gemini)
4. Field-level sanity checks & warning generation
5. Structured JSON response formulation (ExtractionResponse)
"""
import logging
from typing import Optional, Union, BinaryIO
from backend.app.schemas import (
    DocumentType,
    ExtractionStatus,
    InvoiceExtraction,
    BillOfLadingExtraction,
    ExtractionResponse,
)
from backend.app.pdf_parser import (
    PDFParser,
    PDFExtractionResult,
    PDFParsingError,
    CorruptedPDFError,
    EmptyPDFError,
)
from backend.app.document_classifier import DocumentClassifier
from backend.app.llm_service import (
    LLMService,
    LLMServiceError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMResponseError,
)

logger = logging.getLogger(__name__)


class DocumentExtractorPipeline:
    """
    Unified extraction pipeline connecting parsing, classification,
    LLM inference, and validation.
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize pipeline with an optional LLM service instance.
        If not supplied, instantiates a default LLMService.
        """
        self.llm_service = llm_service or LLMService()

    def process_document(
        self,
        source: Union[str, bytes, BinaryIO],
        filename: str = "document.pdf",
    ) -> ExtractionResponse:
        """
        Executes the complete extraction pipeline for an uploaded PDF.

        Args:
            source: Raw PDF bytes, filepath, or file-like stream.
            filename: Original filename for logging and response tracking.

        Returns:
            ExtractionResponse model containing document type, status,
            validated data payload, warnings, and preview.
        """
        warnings = []

        # ----------------------------------------------------------------------
        # Step 1: PDF Text Extraction
        # ----------------------------------------------------------------------
        try:
            extraction_result: PDFExtractionResult = PDFParser.extract_text(
                source, strict_ocr_check=False
            )
        except EmptyPDFError as exc:
            return ExtractionResponse(
                document_type=DocumentType.UNKNOWN,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"Empty PDF upload: {exc}",
            )
        except CorruptedPDFError as exc:
            return ExtractionResponse(
                document_type=DocumentType.UNKNOWN,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"Corrupted or invalid PDF binary: {exc}",
            )
        except Exception as exc:
            logger.error(f"Unexpected parsing error for {filename}: {exc}")
            return ExtractionResponse(
                document_type=DocumentType.UNKNOWN,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"Failed to parse document text: {exc}",
            )

        raw_text = extraction_result.raw_text
        raw_preview = raw_text[:500] if raw_text else None

        # ----------------------------------------------------------------------
        # Step 2: Handle Scanned / Image-Only PDFs
        # ----------------------------------------------------------------------
        if extraction_result.requires_ocr:
            return ExtractionResponse(
                document_type=DocumentType.UNKNOWN,
                extraction_status=ExtractionStatus.FAILED,
                warnings=[
                    "No selectable text found in the document. This file appears to be a scanned image.",
                    "Optical Character Recognition (OCR) is required for scanned documents."
                ],
                error_message="Document contains no extractable text characters. OCR is required.",
                raw_text_preview=None,
            )

        # ----------------------------------------------------------------------
        # Step 3: Document Type Classification
        # ----------------------------------------------------------------------
        doc_type, confidence = DocumentClassifier.classify(raw_text)

        if doc_type == DocumentType.UNKNOWN:
            return ExtractionResponse(
                document_type=DocumentType.UNKNOWN,
                extraction_status=ExtractionStatus.FAILED,
                warnings=[
                    "Document does not match supported business formats (Invoice or Bill of Lading)."
                ],
                error_message=(
                    "Unsupported document type. Only Invoices and Bills of Lading "
                    "are supported for structured extraction."
                ),
                raw_text_preview=raw_preview,
            )

        # ----------------------------------------------------------------------
        # Step 4: LLM Structured Extraction
        # ----------------------------------------------------------------------
        try:
            extracted_data = self.llm_service.extract_document(raw_text, doc_type)
        except LLMAuthenticationError as exc:
            return ExtractionResponse(
                document_type=doc_type,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"LLM Authentication error: {exc}",
                raw_text_preview=raw_preview,
            )
        except LLMRateLimitError as exc:
            return ExtractionResponse(
                document_type=doc_type,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"LLM Rate limit / quota exceeded: {exc}",
                raw_text_preview=raw_preview,
            )
        except LLMResponseError as exc:
            return ExtractionResponse(
                document_type=doc_type,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"LLM extraction parsing error: {exc}",
                raw_text_preview=raw_preview,
            )
        except Exception as exc:
            logger.error(f"LLM extraction failed for {filename}: {exc}")
            return ExtractionResponse(
                document_type=doc_type,
                extraction_status=ExtractionStatus.FAILED,
                error_message=f"LLM service encountered an unexpected error: {exc}",
                raw_text_preview=raw_preview,
            )

        # ----------------------------------------------------------------------
        # Step 5: Domain Sanity Checks & Warning Generation
        # ----------------------------------------------------------------------
        field_warnings = self._generate_sanity_warnings(extracted_data, doc_type)
        warnings.extend(field_warnings)

        status_result = ExtractionStatus.SUCCESS
        if len(warnings) > 0 and self._has_missing_critical_fields(extracted_data, doc_type):
            status_result = ExtractionStatus.PARTIAL

        return ExtractionResponse(
            document_type=doc_type,
            extraction_status=status_result,
            data=extracted_data,
            warnings=warnings,
            error_message=None,
            raw_text_preview=raw_preview,
        )

    def _generate_sanity_warnings(
        self,
        data: Union[InvoiceExtraction, BillOfLadingExtraction],
        doc_type: DocumentType,
    ) -> list[str]:
        """Inspects extracted fields and returns non-fatal review advisories."""
        warnings = []
        if doc_type == DocumentType.INVOICE and isinstance(data, InvoiceExtraction):
            if not data.invoice_number:
                warnings.append("Invoice number was not detected.")
            if not data.total_amount:
                warnings.append("Total amount due was not detected.")
            if not data.vendor_name:
                warnings.append("Vendor or supplier name was not detected.")
            if not data.line_items:
                warnings.append("No itemized line items were extracted.")
            # Verify mathematical reconciliation if subtotal + tax exist
            if data.subtotal and data.tax_amount and data.total_amount:
                expected_total = (
                    data.subtotal
                    + data.tax_amount
                    + (data.shipping_amount or 0)
                    - (data.discount_amount or 0)
                )
                if abs(expected_total - data.total_amount) > 0.05:
                    warnings.append(
                        f"Calculated subtotal + tax + shipping - discount ({expected_total}) "
                        f"differs slightly from printed total ({data.total_amount}). Please review."
                    )

        elif doc_type == DocumentType.BILL_OF_LADING and isinstance(data, BillOfLadingExtraction):
            if not data.bol_number:
                warnings.append("Bill of Lading number was not detected.")
            if not data.shipper_name:
                warnings.append("Shipper name was not detected.")
            if not data.consignee_name:
                warnings.append("Consignee name was not detected.")
            if not data.vessel_name:
                warnings.append("Vessel name was not detected.")
            if not data.container_numbers:
                warnings.append("No shipping container numbers were identified.")

        return warnings

    def _has_missing_critical_fields(
        self,
        data: Union[InvoiceExtraction, BillOfLadingExtraction],
        doc_type: DocumentType,
    ) -> bool:
        """Determines if any critical identity or amount fields are missing."""
        if doc_type == DocumentType.INVOICE and isinstance(data, InvoiceExtraction):
            return data.invoice_number is None or data.total_amount is None
        elif doc_type == DocumentType.BILL_OF_LADING and isinstance(data, BillOfLadingExtraction):
            return data.bol_number is None or data.shipper_name is None
        return False
