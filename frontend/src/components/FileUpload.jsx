import React, { useState, useRef } from "react";
import { UploadCloud, FileText, X, AlertCircle } from "lucide-react";

export default function FileUpload({ onUpload, isLoading }) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [clientError, setClientError] = useState("");
  const inputRef = useRef(null);

  const formatFileSize = (bytes) => {
    if (!bytes) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  const validateAndSetFile = (file) => {
    setClientError("");
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setClientError("Invalid file type. Please upload a PDF document (.pdf).");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setClientError("File size exceeds 10 MB limit.");
      return;
    }

    setSelectedFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setClientError("");
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFile && !isLoading) {
      onUpload(selectedFile);
    }
  };

  return (
    <div className="upload-card">
      <form onSubmit={handleSubmit}>
        <div
          className={`dropzone ${dragOver ? "dragover" : ""} ${
            selectedFile ? "has-file" : ""
          }`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => !selectedFile && inputRef.current?.click()}
        >
          <input
            type="file"
            ref={inputRef}
            onChange={handleFileChange}
            accept=".pdf,application/pdf"
            style={{ display: "none" }}
          />

          {!selectedFile ? (
            <div className="dropzone-content">
              <div className="icon-circle">
                <UploadCloud className="upload-icon" size={36} />
              </div>
              <h3>Drag & drop your Invoice or Bill of Lading PDF</h3>
              <p className="dropzone-hint">
                Supports text-based invoices and freight documents up to 10 MB
              </p>
              <button
                type="button"
                className="btn-browse"
                onClick={(e) => {
                  e.stopPropagation();
                  inputRef.current?.click();
                }}
              >
                Browse Files
              </button>
            </div>
          ) : (
            <div className="file-preview-content">
              <div className="file-badge">
                <FileText className="file-icon" size={28} />
                <div className="file-info">
                  <span className="file-name">{selectedFile.name}</span>
                  <span className="file-size">
                    {formatFileSize(selectedFile.size)}
                  </span>
                </div>
                {!isLoading && (
                  <button
                    type="button"
                    className="btn-remove-file"
                    onClick={(e) => {
                      e.stopPropagation();
                      clearSelection();
                    }}
                    title="Remove selected file"
                  >
                    <X size={18} />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {clientError && (
          <div className="alert-message error-alert">
            <AlertCircle size={18} />
            <span>{clientError}</span>
          </div>
        )}

        <div className="upload-actions">
          <button
            type="submit"
            className="btn-primary"
            disabled={!selectedFile || isLoading}
          >
            {isLoading ? (
              <span className="btn-loading">
                <span className="spinner"></span> Processing Document...
              </span>
            ) : (
              "Extract Structured Data"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
