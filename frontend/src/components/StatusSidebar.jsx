import React from "react";
import {
  FileText,
  CheckCircle2,
  Download,
  RotateCcw,
  FileSpreadsheet,
} from "lucide-react";

export default function StatusSidebar({
  file,
  status,
  progress = 0,
  response,
  onReset,
}) {
  const formatFileSize = (bytes) => {
    if (!bytes) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  const downloadJson = () => {
    if (!response) return;
    const blob = new Blob([JSON.stringify(response, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${file ? file.name.replace(".pdf", "") : "extracted"}_data.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const downloadCsv = () => {
    if (!response?.data) return;
    const data = response.data;
    let csvContent = "Field,Value\n";
    Object.entries(data).forEach(([key, val]) => {
      if (typeof val !== "object" && val !== null) {
        csvContent += `"${key}","${String(val).replace(/"/g, '""')}"\n`;
      }
    });
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${file ? file.name.replace(".pdf", "") : "extracted"}_fields.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const isUploaded = !!file;
  const isScanned = status === "extracting" || status === "completed";
  const isExtracted = status === "completed";
  const isValidated = status === "completed" && response?.extraction_status === "success";

  return (
    <div className="status-sidebar-card">
      {/* 1. Document Details Box */}
      <div className="status-section">
        <h4 className="section-label">Document</h4>
        {file ? (
          <div className="doc-meta-badge">
            <div className="doc-icon-wrap">
              <FileText size={22} className="doc-icon" />
            </div>
            <div className="doc-details">
              <span className="doc-name" title={file.name}>
                {file.name}
              </span>
              <span className="doc-size">{formatFileSize(file.size)}</span>
            </div>
          </div>
        ) : (
          <p className="no-doc-hint">No active document selected.</p>
        )}
      </div>

      {/* 2. Vertical Processing Timeline */}
      <div className="status-section">
        <h4 className="section-label">Processing Status</h4>

        <div className="timeline-vertical">
          <div className={`timeline-node ${isUploaded ? "completed" : "pending"}`}>
            <div className="node-marker">
              {isUploaded ? <CheckCircle2 size={16} /> : <span className="dot"></span>}
            </div>
            <div className="node-content">
              <span className="node-title">Document uploaded</span>
              <span className="node-subtitle">
                {isUploaded ? "Completed" : "Waiting for upload"}
              </span>
            </div>
          </div>

          <div
            className={`timeline-node ${
              status === "scanning"
                ? "in-progress"
                : isScanned
                ? "completed"
                : "pending"
            }`}
          >
            <div className="node-marker">
              {isScanned ? (
                <CheckCircle2 size={16} />
              ) : status === "scanning" ? (
                <span className="pulsing-ring"></span>
              ) : (
                <span className="dot"></span>
              )}
            </div>
            <div className="node-content">
              <span className="node-title">Scanning document</span>
              <span className="node-subtitle">
                {status === "scanning"
                  ? "In progress (pypdf)"
                  : isScanned
                  ? "Completed"
                  : "Pending"}
              </span>
            </div>
          </div>

          <div
            className={`timeline-node ${
              status === "extracting"
                ? "in-progress"
                : isExtracted
                ? "completed"
                : "pending"
            }`}
          >
            <div className="node-marker">
              {isExtracted ? (
                <CheckCircle2 size={16} />
              ) : status === "extracting" ? (
                <span className="pulsing-ring"></span>
              ) : (
                <span className="dot"></span>
              )}
            </div>
            <div className="node-content">
              <span className="node-title">Extracting data</span>
              <span className="node-subtitle">
                {status === "extracting"
                  ? "Gemini 3.8 Flash"
                  : isExtracted
                  ? "Completed"
                  : "Pending"}
              </span>
            </div>
          </div>

          <div className={`timeline-node ${isValidated ? "completed" : "pending"}`}>
            <div className="node-marker">
              {isValidated ? <CheckCircle2 size={16} /> : <span className="dot"></span>}
            </div>
            <div className="node-content">
              <span className="node-title">Review & validate</span>
              <span className="node-subtitle">
                {isValidated ? "Validated with Pydantic" : "Pending"}
              </span>
            </div>
          </div>

          <div className={`timeline-node ${status === "completed" ? "completed" : "pending"}`}>
            <div className="node-marker">
              {status === "completed" ? (
                <CheckCircle2 size={16} />
              ) : (
                <span className="dot"></span>
              )}
            </div>
            <div className="node-content">
              <span className="node-title">Export data</span>
              <span className="node-subtitle">
                {status === "completed" ? "Ready for download" : "Pending"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Overall Progress Bar */}
      <div className="status-section">
        <div className="progress-header">
          <span className="progress-label">Overall progress</span>
          <span className="progress-percent">{progress}%</span>
        </div>
        <div className="progress-track">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* 4. Action Buttons */}
      <div className="status-actions">
        {status === "completed" && (
          <>
            <button
              type="button"
              className="btn-action-primary"
              onClick={downloadJson}
            >
              <Download size={16} /> Export JSON
            </button>
            <button
              type="button"
              className="btn-action-secondary"
              onClick={downloadCsv}
            >
              <FileSpreadsheet size={16} /> Export CSV
            </button>
          </>
        )}

        {file && (
          <button
            type="button"
            className="btn-action-tertiary"
            onClick={onReset}
          >
            <RotateCcw size={15} /> Upload Another File
          </button>
        )}
      </div>
    </div>
  );
}
