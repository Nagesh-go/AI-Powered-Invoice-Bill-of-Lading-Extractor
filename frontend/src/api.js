/**
 * API Service for Document Extractor Backend.
 * Decouples network calls and error serialization from React components.
 */

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Checks backend health and server connectivity.
 * @returns {Promise<{status: string, service: string, version: string}>}
 */
export async function checkBackendHealth() {
  try {
    const res = await fetch(`${BASE_URL}/api/health`, { method: "GET" });
    if (!res.ok) {
      throw new Error(`Health check failed with status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error("Backend health check failed:", err);
    throw new Error(
      "Unable to connect to FastAPI backend server. Ensure backend is running on http://localhost:8000."
    );
  }
}

/**
 * Uploads a PDF file and executes end-to-end extraction.
 * @param {File} file - PDF file selected by the user.
 * @returns {Promise<Object>} ExtractionResponse object from backend.
 */
export async function extractDocument(file) {
  if (!file) {
    throw new Error("No file selected for extraction.");
  }

  // Enforce client-side file type check before making network request
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    throw new Error("Only PDF files (.pdf) are supported.");
  }

  // Enforce 10MB limit on the client side
  const maxBytes = 10 * 1024 * 1024;
  if (file.size > maxBytes) {
    throw new Error(
      `File size (${(file.size / (1024 * 1024)).toFixed(1)} MB) exceeds the 10 MB limit.`
    );
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${BASE_URL}/api/extract`, {
      method: "POST",
      body: formData,
      // Note: Do NOT set Content-Type header; browser must set boundary automatically!
    });

    const data = await res.json();

    if (!res.ok) {
      // Backend returned HTTP 4xx or 5xx with { detail: "..." }
      throw new Error(data.detail || `Upload failed with status code ${res.status}`);
    }

    return data;
  } catch (err) {
    if (err.message.includes("Failed to fetch") || err.name === "TypeError") {
      throw new Error(
        "Network Error: Cannot reach FastAPI backend. Make sure the backend server is running on http://localhost:8000."
      );
    }
    throw err;
  }
}
