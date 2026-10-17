"""
Automated tests for FastAPI endpoints.
Tests:
- Health check (GET /api/health)
- Root redirect to Swagger UI (GET /)
- PDF Text Extraction with valid Invoice (POST /api/extract/text)
- PDF Text Extraction with valid Bill of Lading (POST /api/extract/text)
- Blank/Scanned PDF handling with OCR warnings
- Non-PDF extension rejection (400 Bad Request)
- Disguised/Fake PDF binary rejection (415 Unsupported Media Type)
- Empty upload rejection (400 Bad Request)
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify health check endpoint returns 200 OK and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_root_redirects_to_docs():
    """Verify accessing root URL redirects to interactive Swagger UI."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_extract_text_valid_invoice():
    """Verify uploading a valid invoice PDF returns extracted text and metadata."""
    with open("samples/sample_invoice.pdf", "rb") as f:
        files = {"file": ("sample_invoice.pdf", f, "application/pdf")}
        response = client.post("/api/extract/text", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "sample_invoice.pdf"
    assert data["page_count"] == 1
    assert data["char_count"] > 100
    assert data["word_count"] > 20
    assert data["requires_ocr"] is False
    assert len(data["warnings"]) == 0
    assert "INV-2024-0042" in data["raw_text"]
    assert "Apex Industrial Supplies" in data["raw_text"]


def test_extract_text_valid_bol():
    """Verify uploading a valid Bill of Lading returns shipping data."""
    with open("samples/sample_bol.pdf", "rb") as f:
        files = {"file": ("sample_bol.pdf", f, "application/pdf")}
        response = client.post("/api/extract/text", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "sample_bol.pdf"
    assert "BOL-ONEY-8829103" in data["raw_text"]
    assert "EVER FORWARD" in data["raw_text"]


def test_extract_text_blank_pdf_flags_ocr():
    """Verify uploading a blank/scanned document returns requires_ocr=True with warning."""
    with open("samples/blank_sample.pdf", "rb") as f:
        files = {"file": ("blank_sample.pdf", f, "application/pdf")}
        response = client.post("/api/extract/text", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["requires_ocr"] is True
    assert len(data["warnings"]) > 0
    assert "Optical Character Recognition" in data["warnings"][0]


def test_reject_non_pdf_extension():
    """Verify that uploading a non-.pdf file returns 400 Bad Request."""
    files = {"file": ("data.txt", b"Some plain text content", "text/plain")}
    response = client.post("/api/extract/text", files=files)

    assert response.status_code == 400
    assert "Only PDF files (.pdf) are supported" in response.json()["detail"]


def test_reject_fake_pdf_magic_bytes():
    """Verify that a file with .pdf extension but non-PDF header returns 415."""
    fake_content = b"This is a text file renamed to fake.pdf"
    files = {"file": ("fake.pdf", fake_content, "application/pdf")}
    response = client.post("/api/extract/text", files=files)

    assert response.status_code == 415
    assert "File header does not match PDF specification" in response.json()["detail"]


def test_reject_empty_file():
    """Verify that an empty (0-byte) file returns 400 Bad Request."""
    files = {"file": ("empty.pdf", b"", "application/pdf")}
    response = client.post("/api/extract/text", files=files)

    assert response.status_code == 400
    assert "empty (0 bytes)" in response.json()["detail"]
