"""
Automated tests for Document Classifier.
Tests:
- Invoice text classification
- Bill of Lading text classification
- Unknown / Unsupported document detection
- Empty text handling
"""
from backend.app.schemas import DocumentType
from backend.app.document_classifier import DocumentClassifier
from backend.app.pdf_parser import PDFParser


def test_classify_sample_invoice():
    """Verify that sample invoice text is classified as INVOICE with high confidence."""
    result = PDFParser.extract_text("samples/sample_invoice.pdf")
    doc_type, confidence = DocumentClassifier.classify(result.raw_text)
    
    assert doc_type == DocumentType.INVOICE
    assert confidence >= 0.70


def test_classify_sample_bol():
    """Verify that sample BOL text is classified as BILL_OF_LADING with high confidence."""
    result = PDFParser.extract_text("samples/sample_bol.pdf")
    doc_type, confidence = DocumentClassifier.classify(result.raw_text)
    
    assert doc_type == DocumentType.BILL_OF_LADING
    assert confidence >= 0.70


def test_classify_unknown_document():
    """Verify that non-invoice, non-BOL text returns UNKNOWN."""
    random_text = (
        "Project Proposal: Q4 Marketing Strategy\n"
        "Our objective this quarter is to increase user acquisition by 25% "
        "through organic search optimization, content marketing campaigns, "
        "and partner webinars."
    )
    doc_type, confidence = DocumentClassifier.classify(random_text)
    assert doc_type == DocumentType.UNKNOWN
    assert confidence == 0.0


def test_classify_empty_string():
    """Verify that empty or whitespace strings return UNKNOWN."""
    doc_type, confidence = DocumentClassifier.classify("   ")
    assert doc_type == DocumentType.UNKNOWN
    assert confidence == 0.0
