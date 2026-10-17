"""
Application Configuration.

Loads environment variables from .env file and provides typed settings
for upload limits, CORS origins, and API keys.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Locate project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file if present
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / ".env")


class Settings:
    """Application settings and constants."""
    PROJECT_NAME: str = "AI-Powered Invoice & Bill of Lading Extractor"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # File upload constraints
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    MAX_UPLOAD_SIZE_BYTES: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    # PDF magic byte signature: all standard PDFs start with '%PDF'
    PDF_MAGIC_BYTES: bytes = b"%PDF"

    # CORS configuration for frontend
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite default local dev
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # LLM API key and model (Google AI Studio)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


settings = Settings()
