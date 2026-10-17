"""
FastAPI Backend Application Entrypoint.

Provides:
- Health check endpoint (GET /api/health)
- Complete End-to-End Extraction endpoint (POST /api/extract)
- PDF upload and text extraction preview (POST /api/extract/text)
- CORS middleware for React frontend integration
- Request validation, size limit enforcement, and magic byte verification
"""
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.app.config import settings
from backend.app.schemas import ExtractionResponse
from backend.app.extractor import DocumentExtractorPipeline
from backend.app.pdf_parser import (
    PDFParser,
    PDFExtractionResult,
    CorruptedPDFError,
    EmptyPDFError,
)

logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "REST API for extracting structured data from Invoices and Bills of Lading "
        "using pypdf, Pydantic, and Large Language Models."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Cross-Origin Resource Sharing (CORS) for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate singleton extraction pipeline
extractor_pipeline = DocumentExtractorPipeline()


@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root traffic to interactive Swagger UI."""
    return RedirectResponse(url="/docs")


@app.get(
    f"{settings.API_PREFIX}/health",
    tags=["System"],
    summary="Health Check",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """
    Returns the operational status of the backend API.
    Used for monitoring, deployment readiness probes, and client liveness checks.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


@app.post(
    f"{settings.API_PREFIX}/extract",
    tags=["Document Extraction"],
    summary="Upload PDF and Extract Structured Data",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_document(file: UploadFile = File(...)):
    """
    End-to-end extraction endpoint:
    1. Validates file extension, size limit, and PDF magic bytes.
    2. Extracts text using pypdf.
    3. Detects scanned documents requiring OCR.
    4. Classifies document as Invoice or Bill of Lading.
    5. Prompts Gemini with schema-constrained JSON outputs.
    6. Validates data with Pydantic and returns structured response.
    """
    # 1. Filename validation
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files (.pdf) are supported.",
        )

    # 2. Read in-memory bytes
    content = await file.read()
    file_size = len(content)

    # 3. Check for empty upload
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF file is empty (0 bytes).",
        )

    # 4. Enforce upload size limit
    if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File size exceeds maximum permitted limit of {settings.MAX_UPLOAD_SIZE_MB} MB. "
                f"Uploaded size: {file_size / (1024 * 1024):.2f} MB."
            ),
        )

    # 5. Magic byte verification
    if not content.startswith(settings.PDF_MAGIC_BYTES):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid PDF structure. File header does not match PDF specification (%PDF).",
        )

    # 6. Process through unified extraction pipeline
    result = extractor_pipeline.process_document(content, filename=file.filename)
    return result


@app.post(
    f"{settings.API_PREFIX}/extract/text",
    tags=["PDF Processing"],
    summary="Upload PDF and Extract Raw Text",
    status_code=status.HTTP_200_OK,
)
async def extract_pdf_text(file: UploadFile = File(...)):
    """
    Inspect raw extracted text from a PDF without invoking the LLM.
    Useful for quick text validation, debugging, and testing OCR requirements.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files (.pdf) are supported.",
        )

    content = await file.read()
    file_size = len(content)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF file is empty (0 bytes).",
        )

    if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB} MB limit.",
        )

    if not content.startswith(settings.PDF_MAGIC_BYTES):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid PDF structure. File header does not match PDF specification (%PDF).",
        )

    try:
        extraction: PDFExtractionResult = PDFParser.extract_text(
            content, strict_ocr_check=False
        )
    except (CorruptedPDFError, EmptyPDFError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        logger.error(f"Error parsing PDF text {file.filename}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error occurred while processing PDF text.",
        )

    warnings = []
    if extraction.requires_ocr:
        warnings.append(
            "No extractable text found. This document appears to be a scanned image or empty. "
            "Optical Character Recognition (OCR) is required for scanned documents."
        )

    return {
        "filename": file.filename,
        "file_size_bytes": file_size,
        "page_count": extraction.page_count,
        "char_count": extraction.char_count,
        "word_count": extraction.word_count,
        "requires_ocr": extraction.requires_ocr,
        "warnings": warnings,
        "raw_text": extraction.raw_text,
    }
