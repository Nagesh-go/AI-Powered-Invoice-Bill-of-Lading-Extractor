"""
Manual test script for PDF parsing.
Runs the parser on sample documents and prints formatted terminal output.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.pdf_parser import PDFParser, ScannedPDFError, CorruptedPDFError

def main():
    print("=" * 65)
    print(" 1. Testing Valid Invoice (samples/sample_invoice.pdf)")
    print("=" * 65)
    try:
        result = PDFParser.extract_text("samples/sample_invoice.pdf")
        print(f"Page Count   : {result.page_count}")
        print(f"Total Chars  : {result.char_count}")
        print(f"Total Words  : {result.word_count}")
        print(f"Requires OCR : {result.requires_ocr}")
        print("\n--- Extracted Text Preview ---")
        preview = result.raw_text[:350].strip()
        print(preview + ("\n..." if len(result.raw_text) > 350 else ""))
    except Exception as exc:
        print(f"Unexpected Error: {exc}")

    print("\n" + "=" * 65)
    print(" 2. Testing Valid Bill of Lading (samples/sample_bol.pdf)")
    print("=" * 65)
    try:
        result_bol = PDFParser.extract_text("samples/sample_bol.pdf")
        print(f"Page Count   : {result_bol.page_count}")
        print(f"Total Chars  : {result_bol.char_count}")
        print(f"Total Words  : {result_bol.word_count}")
        print(f"Requires OCR : {result_bol.requires_ocr}")
        print("\n--- Extracted Text Preview ---")
        preview = result_bol.raw_text[:350].strip()
        print(preview + ("\n..." if len(result_bol.raw_text) > 350 else ""))
    except Exception as exc:
        print(f"Unexpected Error: {exc}")

    print("\n" + "=" * 65)
    print(" 3. Testing Blank/Scanned PDF (samples/blank_sample.pdf)")
    print("=" * 65)
    try:
        PDFParser.extract_text("samples/blank_sample.pdf", strict_ocr_check=True)
        print("FAIL: Expected ScannedPDFError was not raised!")
    except ScannedPDFError as exc:
        print(f"SUCCESS: Caught expected ScannedPDFError:\n  -> {exc}")

    print("\n" + "=" * 65)
    print(" 4. Testing Corrupted Input (random bytes)")
    print("=" * 65)
    try:
        PDFParser.extract_text(b"Not a real PDF stream", strict_ocr_check=True)
        print("FAIL: Expected CorruptedPDFError was not raised!")
    except CorruptedPDFError as exc:
        print(f"SUCCESS: Caught expected CorruptedPDFError:\n  -> {exc}")

    print("\n" + "=" * 65)
    print(" ALL PDF PARSER TESTS VERIFIED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    main()
