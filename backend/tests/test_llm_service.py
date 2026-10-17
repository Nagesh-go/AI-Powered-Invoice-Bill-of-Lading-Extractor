"""
Automated tests for LLM Service using mocked Gemini API responses.
Ensures prompt passing, schema compliance, error translation,
and Pydantic validation are thoroughly tested without incurring API costs.
"""
import json
from decimal import Decimal
from unittest.mock import MagicMock, patch
import pytest
from google.genai.errors import APIError

from backend.app.schemas import DocumentType, InvoiceExtraction, BillOfLadingExtraction
from backend.app.llm_service import (
    LLMService,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMResponseError,
)


def test_missing_api_key_raises_auth_error():
    """Verify that attempting extraction without an API key raises LLMAuthenticationError."""
    service = LLMService(api_key="")
    with pytest.raises(LLMAuthenticationError) as exc_info:
        service.extract_invoice("Sample raw text")
    assert "GEMINI_API_KEY is not configured" in str(exc_info.value)


@patch("backend.app.llm_service.genai.Client")
def test_mock_invoice_extraction(mock_client_class):
    """Verify that a successful Gemini response parses into a valid InvoiceExtraction model."""
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "document_type": "invoice",
        "invoice_number": "INV-2024-0042",
        "invoice_date": "2024-10-15",
        "vendor_name": "Apex Industrial Supplies Ltd.",
        "customer_name": "Nexus Logistics Corp",
        "currency": "USD",
        "total_amount": "1154.53",
        "line_items": [
            {
                "description": "Heavy Duty Steel Strapping",
                "quantity": 10,
                "unit_price": 45.0,
                "line_total": 450.0,
            }
        ]
    })

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client_instance

    service = LLMService(api_key="mock-api-key")
    result = service.extract_invoice("Raw invoice document text")

    assert isinstance(result, InvoiceExtraction)
    assert result.invoice_number == "INV-2024-0042"
    assert result.vendor_name == "Apex Industrial Supplies Ltd."
    assert result.total_amount == Decimal("1154.53")
    assert len(result.line_items) == 1
    assert result.line_items[0].description == "Heavy Duty Steel Strapping"


@patch("backend.app.llm_service.genai.Client")
def test_mock_bol_extraction(mock_client_class):
    """Verify that a successful Gemini response parses into a valid BillOfLadingExtraction model."""
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "document_type": "bill_of_lading",
        "bol_number": "BOL-ONEY-8829103",
        "shipper_name": "Orient Global Manufacturing Ltd.",
        "consignee_name": "Pacific Imports & Distribution LLC",
        "vessel_name": "EVER FORWARD",
        "container_numbers": ["ONEU9876543"],
        "gross_weight": "8450.00",
        "weight_unit": "KGS"
    })

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client_instance

    service = LLMService(api_key="mock-api-key")
    result = service.extract_bill_of_lading("Raw BOL document text")

    assert isinstance(result, BillOfLadingExtraction)
    assert result.bol_number == "BOL-ONEY-8829103"
    assert result.vessel_name == "EVER FORWARD"
    assert result.gross_weight == Decimal("8450.00")
    assert "ONEU9876543" in result.container_numbers


@patch("backend.app.llm_service.genai.Client")
def test_rate_limit_error_handling(mock_client_class):
    """Verify that 429 quota exhaustion from Gemini is translated into LLMRateLimitError."""
    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.side_effect = APIError(
        429, "Resource has been exhausted (e.g. check quota)."
    )
    mock_client_class.return_value = mock_client_instance

    service = LLMService(api_key="mock-api-key")
    with pytest.raises(LLMRateLimitError) as exc_info:
        service.extract_invoice("Raw text")
    assert "rate limit exceeded" in str(exc_info.value).lower()


@patch("backend.app.llm_service.genai.Client")
def test_malformed_llm_response_raises_response_error(mock_client_class):
    """Verify that invalid JSON returned by the model raises LLMResponseError."""
    mock_response = MagicMock()
    mock_response.text = "This is not valid JSON string at all"

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client_instance

    service = LLMService(api_key="mock-api-key")
    with pytest.raises(LLMResponseError) as exc_info:
        service.extract_invoice("Raw text")
    assert "validation" in str(exc_info.value).lower()
