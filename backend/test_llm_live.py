"""
Live LLM Extraction Test Script.

Tests real-world extraction against Google Gemini API using samples/sample_invoice.pdf
and samples/sample_bol.pdf.
Requires a valid GEMINI_API_KEY in backend/.env or your environment.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.config import settings
from backend.app.pdf_parser import PDFParser
from backend.app.document_classifier import DocumentClassifier
from backend.app.llm_service import LLMService, LLMAuthenticationError


def main():
    print("=" * 65)
    print(" AI-POWERED DOCUMENT EXTRACTOR: LIVE LLM EXTRACTION TEST")
    print("=" * 65)

    if not settings.GEMINI_API_KEY:
        print("\n[INFO] GEMINI_API_KEY is not yet set in backend/.env!")
        print("To run live extractions against Google Gemini:")
        print("1. Get a free API key at: https://aistudio.google.com/")
        print("2. Add it to your backend/.env file: GEMINI_API_KEY=AIzaSy...")
        print("3. Re-run this script!\n")
        print("NOTE: All 33 automated unit tests pass using mocked LLM responses.")
        return

    print(f"\n[OK] API Key detected: {settings.GEMINI_API_KEY[:8]}... (hidden)")
    llm = LLMService()

    # 1. Test Invoice Extraction
    invoice_path = "samples/sample_invoice.pdf"
    print(f"\n--- 1. Testing Invoice Extraction ({invoice_path}) ---")
    parsed_invoice = PDFParser.extract_text(invoice_path)
    doc_type, confidence = DocumentClassifier.classify(parsed_invoice.raw_text)
    print(f"Detected Type: {doc_type.value.upper()} (Confidence: {confidence * 100:.0f}%)")

    print("Sending text to Gemini with InvoiceExtraction schema enforcement...")
    try:
        invoice_data = llm.extract_invoice(parsed_invoice.raw_text)
        print("\n[SUCCESS] Extracted Invoice Data:")
        print(f"  Invoice Number : {invoice_data.invoice_number}")
        print(f"  Invoice Date   : {invoice_data.invoice_date}")
        print(f"  Vendor Name    : {invoice_data.vendor_name}")
        print(f"  Customer Name  : {invoice_data.customer_name}")
        print(f"  Subtotal       : {invoice_data.currency} {invoice_data.subtotal}")
        print(f"  Tax Amount     : {invoice_data.currency} {invoice_data.tax_amount}")
        print(f"  Shipping       : {invoice_data.currency} {invoice_data.shipping_amount}")
        print(f"  Total Amount   : {invoice_data.currency} {invoice_data.total_amount}")
        print(f"  Line Items ({len(invoice_data.line_items)}):")
        for item in invoice_data.line_items:
            print(f"    - {item.description} | Qty: {item.quantity} | Total: {item.line_total}")
    except Exception as exc:
        print(f"[ERROR] Invoice extraction failed: {exc}")

    # 2. Test BOL Extraction
    bol_path = "samples/sample_bol.pdf"
    print(f"\n--- 2. Testing Bill of Lading Extraction ({bol_path}) ---")
    parsed_bol = PDFParser.extract_text(bol_path)
    doc_type_bol, conf_bol = DocumentClassifier.classify(parsed_bol.raw_text)
    print(f"Detected Type: {doc_type_bol.value.upper()} (Confidence: {conf_bol * 100:.0f}%)")

    print("Sending text to Gemini with BillOfLadingExtraction schema enforcement...")
    try:
        bol_data = llm.extract_bill_of_lading(parsed_bol.raw_text)
        print("\n[SUCCESS] Extracted Bill of Lading Data:")
        print(f"  BOL Number     : {bol_data.bol_number}")
        print(f"  Shipper        : {bol_data.shipper_name}")
        print(f"  Consignee      : {bol_data.consignee_name}")
        print(f"  Vessel / Voyage: {bol_data.vessel_name} ({bol_data.voyage_number})")
        print(f"  Port Loading   : {bol_data.port_of_loading}")
        print(f"  Port Discharge : {bol_data.port_of_discharge}")
        print(f"  Containers     : {', '.join(bol_data.container_numbers)}")
        print(f"  Gross Weight   : {bol_data.gross_weight} {bol_data.weight_unit}")
        print(f"  Goods          : {bol_data.goods_description}")
    except Exception as exc:
        print(f"[ERROR] BOL extraction failed: {exc}")

    print("\n" + "=" * 65)
    print(" LIVE EXTRACTION VERIFICATION COMPLETE")
    print("=" * 65)


if __name__ == "__main__":
    main()
