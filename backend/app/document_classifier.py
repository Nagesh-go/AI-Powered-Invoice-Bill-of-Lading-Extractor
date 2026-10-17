"""
Document Classification Module.

Determines whether extracted text belongs to an Invoice, a Bill of Lading,
or an unsupported/unknown document type using keyword density analysis.
"""
import re
from typing import Tuple
from backend.app.schemas import DocumentType


class DocumentClassifier:
    """
    Deterministic rule-based document classifier.
    
    Uses domain keyword density scoring to categorize text into
    INVOICE, BILL_OF_LADING, or UNKNOWN without wasting LLM tokens.
    """

    INVOICE_KEYWORDS = [
        r"\binvoice\b",
        r"\btax invoice\b",
        r"\binvoice number\b",
        r"\binv-\d+",
        r"\bdue date\b",
        r"\bbill to\b",
        r"\bvendor\b",
        r"\bsubtotal\b",
        r"\bunit price\b",
        r"\bpayment terms\b",
        r"\btotal amount\b",
        r"\bamount due\b",
        r"\bpo number\b",
        r"\bpurchase order\b",
    ]

    BOL_KEYWORDS = [
        r"\bbill of lading\b",
        r"\bbol\b",
        r"\bb/l\b",
        r"\bshipper\b",
        r"\bconsignee\b",
        r"\bnotify party\b",
        r"\bvessel\b",
        r"\bvoyage\b",
        r"\bport of loading\b",
        r"\bport of discharge\b",
        r"\bplace of receipt\b",
        r"\bcontainer\b",
        r"\bseal number\b",
        r"\bgross weight\b",
        r"\bocean bill\b",
    ]

    @classmethod
    def classify(cls, text: str) -> Tuple[DocumentType, float]:
        """
        Classifies the document text.

        Args:
            text: Raw extracted document text.

        Returns:
            Tuple of (DocumentType, confidence_score between 0.0 and 1.0).
        """
        if not text or len(text.strip()) < 20:
            return DocumentType.UNKNOWN, 0.0

        lower_text = text.lower()

        # Count keyword matches
        invoice_score = sum(
            1 for pattern in cls.INVOICE_KEYWORDS if re.search(pattern, lower_text)
        )
        bol_score = sum(
            1 for pattern in cls.BOL_KEYWORDS if re.search(pattern, lower_text)
        )

        total_matches = invoice_score + bol_score
        if total_matches == 0:
            return DocumentType.UNKNOWN, 0.0

        if invoice_score > bol_score and invoice_score >= 2:
            confidence = min(0.99, 0.5 + (invoice_score / len(cls.INVOICE_KEYWORDS)) * 0.5)
            return DocumentType.INVOICE, round(confidence, 2)

        if bol_score > invoice_score and bol_score >= 2:
            confidence = min(0.99, 0.5 + (bol_score / len(cls.BOL_KEYWORDS)) * 0.5)
            return DocumentType.BILL_OF_LADING, round(confidence, 2)

        return DocumentType.UNKNOWN, 0.0
