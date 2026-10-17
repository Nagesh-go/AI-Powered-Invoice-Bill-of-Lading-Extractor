"""
Integration and End-to-End Tests for Document Extraction Pipeline.
Tests:
- POST /api/extract with Invoice PDF (mocked LLM)
- POST /api/extract with Bill of Lading PDF (mocked LLM)
- POST /api/extract with Scanned/Blank PDF (OCR failure state)
- Pipeline sanity warnings generation
- Corrupted file rejection
"""
import json
from decimal import Decimal
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app, extractor_pipeline
from backend.app.schemas import (
    DocumentType,
    ExtractionStatus,
    InvoiceExtraction,
    BillOfLadingExtraction,
)
from backend.app.extractor import DocumentExtractorPipeline

client = TestClient(app)


@patch("backend.app.llm_service.genai.Client")
def test_api_extract_invoice_end_to_end(mock_client_class):
    """Verify POST /api/extract processes an invoice PDF and returns structured JSON."""
    extractor_pipeline.llm_service._client = None

    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "document_type": "invoice",
        "invoice_number": "INV-2024-0042",
        "invoice_date": "2024-10-15",
        "vendor_name": "Apex Industrial Supplies Ltd.",
        "customer_name": "Nexus Logistics Corp",
        "currency": "USD",
        "subtotal": 1018.0,
        "tax_amount": 86.53,
        "shipping_amount": 75.0,
        "discount_amount": 25.0,
        "total_amount": 1154.53,
        "line_items": [
            {
                "description": "Heavy Duty Steel Strapping",
                "quantity": 10,
                "unit_price": 45.0,
                "line_total": 450.0,
            }
        ],
    })

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client_instance

    with open("samples/sample_invoice.pdf", "rb") as f:
        files = {"file": ("sample_invoice.pdf", f, "application/pdf")}
        response = client.post("/api/extract", files=files)

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["document_type"] == "invoice"
    assert res_json["extraction_status"] == "success"
    assert res_json["data"]["invoice_number"] == "INV-2024-0042"
    assert res_json["data"]["vendor_name"] == "Apex Industrial Supplies Ltd."
    assert res_json["data"]["total_amount"] == "1154.53"
    assert len(res_json["data"]["line_items"]) == 1
    assert res_json["raw_text_preview"] is not None


@patch("backend.app.llm_service.genai.Client")
def test_api_extract_bol_end_to_end(mock_client_class):
    """Verify POST /api/extract processes a BOL PDF and returns shipping JSON."""
    extractor_pipeline.llm_service._client = None

    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "document_type": "bill_of_lading",
        "bol_number": "BOL-ONEY-8829103",
        "shipper_name": "Orient Global Manufacturing Ltd.",
        "consignee_name": "Pacific Imports & Distribution LLC",
        "vessel_name": "EVER FORWARD",
        "voyage_number": "V.042W",
        "port_of_loading": "Port of Shenzhen, China",
        "port_of_discharge": "Port of Long Beach, USA",
        "container_numbers": ["ONEU9876543"],
        "gross_weight": 8450.0,
        "weight_unit": "KGS",
    })

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client_instance

    with open("samples/sample_bol.pdf", "rb") as f:
        files = {"file": ("sample_bol.pdf", f, "application/pdf")}
        response = client.post("/api/extract", files=files)

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["document_type"] == "bill_of_lading"
    assert res_json["extraction_status"] == "success"
    assert res_json["data"]["bol_number"] == "BOL-ONEY-8829103"
    assert res_json["data"]["vessel_name"] == "EVER FORWARD"
    assert "ONEU9876543" in res_json["data"]["container_numbers"]


def test_api_extract_scanned_pdf_returns_ocr_required():
    """Verify POST /api/extract handles blank/scanned documents gracefully without crashing."""
    with open("samples/blank_sample.pdf", "rb") as f:
        files = {"file": ("blank_sample.pdf", f, "application/pdf")}
        response = client.post("/api/extract", files=files)

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["extraction_status"] == "failed"
    assert res_json["data"] is None
    assert "OCR is required" in res_json["error_message"]
    assert any("OCR" in w for w in res_json["warnings"])


def test_pipeline_sanity_warnings():
    """Verify that sanity checks detect missing invoice number and math discrepancies."""
    pipeline = DocumentExtractorPipeline(llm_service=MagicMock())

    # Invoice with mismatching totals (100 subtotal + 10 tax != 200 total) and missing invoice_number
    bad_invoice = InvoiceExtraction(
        invoice_number=None,
        subtotal=Decimal("100.00"),
        tax_amount=Decimal("10.00"),
        total_amount=Decimal("200.00"),
    )

    warnings = pipeline._generate_sanity_warnings(bad_invoice, DocumentType.INVOICE)
    assert any("Invoice number was not detected" in w for w in warnings)
    assert any("differs slightly from printed total" in w for w in warnings)
