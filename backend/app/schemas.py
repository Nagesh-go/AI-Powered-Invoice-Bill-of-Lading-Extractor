"""
Pydantic Schemas for Document Extraction.

Defines strict data models for:
- Invoices (metadata, parties, line items, monetary totals)
- Bills of Lading (parties, voyage, cargo, containers)
- Standardized API extraction responses
"""
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


# ==============================================================================
# 1. Enums for Document Classification & Extraction Status
# ==============================================================================
class DocumentType(str, Enum):
    """Supported document classifications."""
    INVOICE = "invoice"
    BILL_OF_LADING = "bill_of_lading"
    UNKNOWN = "unknown"


class ExtractionStatus(str, Enum):
    """Outcome status of the extraction pipeline."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


# ==============================================================================
# 2. Invoice Schemas
# ==============================================================================
class InvoiceLineItem(BaseModel):
    """Individual itemized product or service listed on an invoice."""
    description: str = Field(
        ...,
        description="Detailed description of the product or service billed."
    )
    quantity: Optional[Decimal] = Field(
        default=None,
        description="Number of units billed. Null if not specified."
    )
    unit_price: Optional[Decimal] = Field(
        default=None,
        description="Price per individual unit before tax or discount."
    )
    line_total: Optional[Decimal] = Field(
        default=None,
        description="Total charge for this line item (quantity * unit_price)."
    )

    @field_validator("quantity", "unit_price", "line_total", mode="before")
    @classmethod
    def clean_decimal(cls, val):
        """Clean string representations of numbers (e.g. '$1,250.00' -> '1250.00')."""
        if val is None or val == "":
            return None
        if isinstance(val, (int, float, Decimal)):
            return Decimal(str(val))
        if isinstance(val, str):
            # Strip currency symbols, commas, and whitespace
            cleaned = val.replace("$", "").replace("€", "").replace("£", "").replace(",", "").strip()
            return Decimal(cleaned) if cleaned else None
        return val


class InvoiceExtraction(BaseModel):
    """Structured data extracted from an invoice."""
    document_type: Literal["invoice"] = Field(
        default="invoice",
        description="Identifies this payload as an invoice."
    )
    invoice_number: Optional[str] = Field(
        default=None,
        description="Unique invoice number or reference code."
    )
    invoice_date: Optional[str] = Field(
        default=None,
        description="Date the invoice was issued (in YYYY-MM-DD format if interpretable)."
    )
    due_date: Optional[str] = Field(
        default=None,
        description="Payment due date (in YYYY-MM-DD format if interpretable)."
    )
    purchase_order_number: Optional[str] = Field(
        default=None,
        description="Customer purchase order (PO) number, if present."
    )
    vendor_name: Optional[str] = Field(
        default=None,
        description="Name of the selling vendor or supplier."
    )
    vendor_address: Optional[str] = Field(
        default=None,
        description="Physical address of the selling vendor."
    )
    customer_name: Optional[str] = Field(
        default=None,
        description="Name of the buyer or customer company."
    )
    customer_address: Optional[str] = Field(
        default=None,
        description="Billing or shipping address of the buyer."
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency code (e.g. USD, EUR, GBP) or currency symbol."
    )
    subtotal: Optional[Decimal] = Field(
        default=None,
        description="Pre-tax subtotal amount."
    )
    tax_amount: Optional[Decimal] = Field(
        default=None,
        description="Total sales tax, VAT, or GST applied."
    )
    shipping_amount: Optional[Decimal] = Field(
        default=None,
        description="Freight, delivery, or shipping charges."
    )
    discount_amount: Optional[Decimal] = Field(
        default=None,
        description="Discounts applied to reduce the total."
    )
    total_amount: Optional[Decimal] = Field(
        default=None,
        description="Final grand total amount due."
    )
    payment_terms: Optional[str] = Field(
        default=None,
        description="Payment terms (e.g., 'Net 30 Days', 'Due Upon Receipt')."
    )
    line_items: List[InvoiceLineItem] = Field(
        default_factory=list,
        description="List of itemized goods or services billed."
    )

    @field_validator(
        "subtotal", "tax_amount", "shipping_amount", "discount_amount", "total_amount",
        mode="before"
    )
    @classmethod
    def clean_monetary_values(cls, val):
        """Clean string representations of monetary numbers."""
        if val is None or val == "":
            return None
        if isinstance(val, (int, float, Decimal)):
            return Decimal(str(val))
        if isinstance(val, str):
            cleaned = val.replace("$", "").replace("€", "").replace("£", "").replace(",", "").strip()
            return Decimal(cleaned) if cleaned else None
        return val


# ==============================================================================
# 3. Bill of Lading (BOL) Schemas
# ==============================================================================
class BillOfLadingExtraction(BaseModel):
    """Structured data extracted from an Ocean/Multimodal Bill of Lading."""
    document_type: Literal["bill_of_lading"] = Field(
        default="bill_of_lading",
        description="Identifies this payload as a Bill of Lading."
    )
    bol_number: Optional[str] = Field(
        default=None,
        description="Bill of lading number or tracking number."
    )
    shipper_name: Optional[str] = Field(
        default=None,
        description="Name of the shipping exporter or entity."
    )
    shipper_address: Optional[str] = Field(
        default=None,
        description="Full physical address of the shipper."
    )
    consignee_name: Optional[str] = Field(
        default=None,
        description="Name of the party receiving the shipment (consignee)."
    )
    consignee_address: Optional[str] = Field(
        default=None,
        description="Address of the consignee."
    )
    notify_party: Optional[str] = Field(
        default=None,
        description="Notify party name, address, or contact details."
    )
    vessel_name: Optional[str] = Field(
        default=None,
        description="Name of the marine vessel or primary transport craft."
    )
    voyage_number: Optional[str] = Field(
        default=None,
        description="Voyage or flight designation number."
    )
    port_of_loading: Optional[str] = Field(
        default=None,
        description="Port where goods are received aboard."
    )
    port_of_discharge: Optional[str] = Field(
        default=None,
        description="Port where goods are unloaded."
    )
    place_of_receipt: Optional[str] = Field(
        default=None,
        description="Location where carrier first took custody."
    )
    final_destination: Optional[str] = Field(
        default=None,
        description="Final destination city or warehouse."
    )
    container_numbers: List[str] = Field(
        default_factory=list,
        description="List of shipping container identifiers (e.g. ONEU9876543)."
    )
    seal_numbers: List[str] = Field(
        default_factory=list,
        description="List of container security seal numbers."
    )
    package_count: Optional[str] = Field(
        default=None,
        description="Total quantity and packaging type (e.g., '450 Cartons', '12 Pallets')."
    )
    goods_description: Optional[str] = Field(
        default=None,
        description="Description of the merchandise being shipped."
    )
    gross_weight: Optional[Decimal] = Field(
        default=None,
        description="Total gross weight of the cargo."
    )
    weight_unit: Optional[str] = Field(
        default=None,
        description="Unit of weight (e.g., 'KGS', 'LBS', 'MT')."
    )
    shipment_date: Optional[str] = Field(
        default=None,
        description="Date shipped or on-board date (YYYY-MM-DD if interpretable)."
    )

    @field_validator("gross_weight", mode="before")
    @classmethod
    def clean_weight(cls, val):
        """Clean string representations of cargo weight."""
        if val is None or val == "":
            return None
        if isinstance(val, (int, float, Decimal)):
            return Decimal(str(val))
        if isinstance(val, str):
            cleaned = val.replace(",", "").replace("KGS", "").replace("LBS", "").strip()
            return Decimal(cleaned) if cleaned else None
        return val


# ==============================================================================
# 4. Standardized API Response Models
# ==============================================================================
class ExtractionResponse(BaseModel):
    """
    Unified API response payload returned by /api/extract.
    Guarantees a predictable contract for the React frontend.
    """
    document_type: DocumentType = Field(
        description="Detected classification of the document."
    )
    extraction_status: ExtractionStatus = Field(
        description="Status of the extraction: success, partial, or failed."
    )
    data: Optional[Union[InvoiceExtraction, BillOfLadingExtraction]] = Field(
        default=None,
        description="Validated structured data model for the detected document type."
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Non-fatal warnings (e.g. OCR required, missing critical fields)."
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Descriptive error message if extraction failed."
    )
    raw_text_preview: Optional[str] = Field(
        default=None,
        description="First 500 characters of raw document text for debugging/transparency."
    )
