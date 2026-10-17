"""
Automated tests for Pydantic Schemas.
Tests:
- InvoiceExtraction validation & monetary Decimal cleaning
- InvoiceLineItem parsing and price cleaning
- BillOfLadingExtraction validation & weight cleaning
- Rejection of invalid data (ValidationError)
- Missing optional fields defaulting to None
- ExtractionResponse unified response wrapper
- JSON serialization
"""
from decimal import Decimal
import pytest
from pydantic import ValidationError

from backend.app.schemas import (
    DocumentType,
    ExtractionStatus,
    InvoiceExtraction,
    InvoiceLineItem,
    BillOfLadingExtraction,
    ExtractionResponse,
)


def test_valid_invoice_schema():
    """Verify that a valid invoice dictionary parses cleanly with Decimal coercion."""
    payload = {
        "document_type": "invoice",
        "invoice_number": "INV-2024-0042",
        "invoice_date": "2024-10-15",
        "due_date": "2024-11-14",
        "vendor_name": "Apex Industrial Supplies Ltd.",
        "customer_name": "Nexus Logistics Corp",
        "currency": "USD",
        "subtotal": "$1,018.00",
        "tax_amount": "$86.53",
        "shipping_amount": "$75.00",
        "discount_amount": "-$25.00",
        "total_amount": "$1,154.53",
        "line_items": [
            {
                "description": "Heavy Duty Steel Strapping",
                "quantity": "10",
                "unit_price": "$45.00",
                "line_total": "$450.00",
            }
        ],
    }

    invoice = InvoiceExtraction(**payload)
    assert invoice.invoice_number == "INV-2024-0042"
    assert invoice.total_amount == Decimal("1154.53")
    assert invoice.subtotal == Decimal("1018.00")
    assert invoice.tax_amount == Decimal("86.53")
    assert invoice.discount_amount == Decimal("-25.00")
    assert len(invoice.line_items) == 1
    assert invoice.line_items[0].quantity == Decimal("10")
    assert invoice.line_items[0].unit_price == Decimal("45.00")
    assert invoice.line_items[0].line_total == Decimal("450.00")


def test_invoice_missing_optional_fields_are_none():
    """Verify that an invoice with minimal data sets missing fields to None, not fabricated values."""
    minimal_payload = {
        "vendor_name": "Acme Corp",
        "total_amount": "500.00",
    }
    invoice = InvoiceExtraction(**minimal_payload)
    assert invoice.vendor_name == "Acme Corp"
    assert invoice.total_amount == Decimal("500.00")
    assert invoice.invoice_number is None
    assert invoice.due_date is None
    assert invoice.purchase_order_number is None
    assert invoice.line_items == []


def test_valid_bill_of_lading_schema():
    """Verify that a valid BOL dictionary parses correctly and cleans weight strings."""
    payload = {
        "document_type": "bill_of_lading",
        "bol_number": "BOL-ONEY-8829103",
        "shipper_name": "Orient Global Manufacturing Ltd.",
        "consignee_name": "Pacific Imports & Distribution LLC",
        "vessel_name": "EVER FORWARD",
        "voyage_number": "V.042W",
        "port_of_loading": "Port of Shenzhen, China",
        "port_of_discharge": "Port of Long Beach, USA",
        "container_numbers": ["ONEU9876543"],
        "seal_numbers": ["SL-554432"],
        "package_count": "450 Cartons",
        "goods_description": "Precision Industrial Ball Bearings (Grade 5)",
        "gross_weight": "8,450.00 KGS",
        "weight_unit": "KGS",
        "shipment_date": "2024-09-28",
    }

    bol = BillOfLadingExtraction(**payload)
    assert bol.bol_number == "BOL-ONEY-8829103"
    assert bol.vessel_name == "EVER FORWARD"
    assert bol.gross_weight == Decimal("8450.00")
    assert bol.container_numbers == ["ONEU9876543"]
    assert bol.seal_numbers == ["SL-554432"]


def test_invalid_line_item_missing_required_description():
    """Verify that omitting description raises ValidationError."""
    with pytest.raises(ValidationError):
        InvoiceLineItem(quantity=10, unit_price=25.0)


def test_invalid_monetary_value_raises_error():
    """Verify that non-numeric characters in amounts raise an error."""
    with pytest.raises(Exception):
        InvoiceExtraction(total_amount="NotANumber")


def test_unified_extraction_response_invoice():
    """Verify ExtractionResponse wraps an InvoiceExtraction payload properly."""
    invoice = InvoiceExtraction(
        invoice_number="INV-001",
        total_amount=Decimal("100.00"),
    )
    response = ExtractionResponse(
        document_type=DocumentType.INVOICE,
        extraction_status=ExtractionStatus.SUCCESS,
        data=invoice,
        warnings=[],
    )

    json_dict = response.model_dump()
    assert json_dict["document_type"] == "invoice"
    assert json_dict["extraction_status"] == "success"
    assert json_dict["data"]["invoice_number"] == "INV-001"
    assert json_dict["data"]["total_amount"] == Decimal("100.00")


def test_unified_extraction_response_bol():
    """Verify ExtractionResponse wraps a BillOfLadingExtraction payload properly."""
    bol = BillOfLadingExtraction(
        bol_number="BOL-999",
        vessel_name="Maersk Alabama",
    )
    response = ExtractionResponse(
        document_type=DocumentType.BILL_OF_LADING,
        extraction_status=ExtractionStatus.SUCCESS,
        data=bol,
    )

    json_str = response.model_dump_json()
    assert "BOL-999" in json_str
    assert "Maersk Alabama" in json_str
