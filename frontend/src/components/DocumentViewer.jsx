import React, { useState, useEffect } from "react";
import { ZoomIn, ZoomOut, Maximize2, RotateCcw, Scan, UploadCloud } from "lucide-react";

export default function DocumentViewer({
  file,
  isScanning,
  onFileSelect,
}) {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [zoom, setZoom] = useState(100);

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setPreviewUrl(null);
    }
  }, [file]);

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 15, 160));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 15, 70));
  const handleResetZoom = () => setZoom(100);

  return (
    <div className="document-viewer-card">
      {/* Top Viewer Header */}
      <div className="viewer-header">
        <div className="viewer-status-badge">
          {isScanning ? (
            <span className="badge-scanning">
              <span className="pulse-dot"></span> Scanning...
            </span>
          ) : file ? (
            <span className="badge-ready">Document Ready</span>
          ) : (
            <span className="badge-empty">Waiting for Upload</span>
          )}
        </div>
        <span className="viewer-filename">
          {file ? file.name : "No file selected"}
        </span>
      </div>

      {/* Main Document Body */}
      <div className="viewer-viewport">
        {isScanning && (
          <div className="scanner-laser-overlay">
            <div className="laser-line"></div>
            <div className="laser-glow"></div>
          </div>
        )}

        {previewUrl ? (
          <div
            className="document-frame-wrapper"
            style={{ transform: `scale(${zoom / 100})`, transformOrigin: "top center" }}
          >
            <iframe
              src={`${previewUrl}#toolbar=0&navpanes=0`}
              title="PDF Preview"
              className="pdf-iframe"
            />
          </div>
        ) : (
          <label className="viewer-dropzone">
            <input
              type="file"
              accept=".pdf,application/pdf"
              style={{ display: "none" }}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  onFileSelect(e.target.files[0]);
                }
              }}
            />
            <div className="dropzone-center">
              <div className="icon-pulse">
                <UploadCloud size={36} />
              </div>
              <h4>Select or Drop PDF Document</h4>
              <p>Click anywhere to browse an Invoice or Bill of Lading</p>
            </div>
          </label>
        )}
      </div>

      {/* Bottom Zoom & Control Bar */}
      <div className="viewer-controls">
        <button
          type="button"
          className="btn-ctrl"
          onClick={handleZoomOut}
          disabled={!previewUrl}
          title="Zoom out"
        >
          <ZoomOut size={16} />
        </button>
        <span className="zoom-indicator">{zoom}%</span>
        <button
          type="button"
          className="btn-ctrl"
          onClick={handleZoomIn}
          disabled={!previewUrl}
          title="Zoom in"
        >
          <ZoomIn size={16} />
        </button>
        <button
          type="button"
          className="btn-ctrl"
          onClick={handleResetZoom}
          disabled={!previewUrl}
          title="Reset zoom"
        >
          <RotateCcw size={14} />
        </button>
      </div>
    </div>
  );
}
