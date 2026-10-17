import React from "react";
import {
  FileText,
  AlertTriangle,
  XCircle,
  RotateCcw,
  CheckCircle2,
  HelpCircle,
} from "lucide-react";
import InvoiceResults from "./InvoiceResults";
import BillOfLadingResults from "./BillOfLadingResults";
import JsonViewer from "./JsonViewer";

export default function ResultsPanel({ response, onReset }) {
  if (!response) return null;

  const {
    document_type,
    extraction_status,
    data,
    warnings,
    error_message,
    raw_text_preview,
  } = response;

  const getDocTypeBadge = () => {
    switch (document_type) {
      case "invoice":
        return <span className="badge badge-invoice">TAX INVOICE</span>;
      case "bill_of_lading":
        return <span className="badge badge-bol">BILL OF LADING</span>;
      default:
        return <span className="badge badge-unknown">UNKNOWN TYPE</span>;
    }
  };

  const getStatusBadge = () => {
    switch (extraction_status) {
      case "success":
        return (
          <span className="status-pill status-success">
            <CheckCircle2 size={14} /> Extraction Complete
          </span>
        );
      case "partial":
        return (
          <span className="status-pill status-partial">
            <AlertTriangle size={14} /> Review Required
          </span>
        );
      case "failed":
        return (
          <span className="status-pill status-failed">
            <XCircle size={14} /> Extraction Failed
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="results-panel">
      {/* 1. Header Toolbar */}
      <div className="results-header">
        <div className="results-title-group">
          {getDocTypeBadge()}
          {getStatusBadge()}
        </div>
        <button type="button" className="btn-secondary" onClick={onReset}>
          <RotateCcw size={16} /> Upload Another File
        </button>
      </div>

      {/* 2. Error Message Banner */}
      {error_message && (
        <div className="alert-message error-alert">
          <XCircle size={20} className="alert-icon" />
          <div className="alert-body">
            <strong>Extraction Error</strong>
            <p>{error_message}</p>
          </div>
        </div>
      )}

      {/* 3. Non-Fatal Review Warnings */}
      {warnings && warnings.length > 0 && (
        <div className="alert-message warning-alert">
          <AlertTriangle size={20} className="alert-icon" />
          <div className="alert-body">
            <strong>System Review Advisories:</strong>
            <ul>
              {warnings.map((w, idx) => (
                <li key={idx}>{w}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* 4. Dynamic Document Content */}
      {document_type === "invoice" && data && <InvoiceResults data={data} />}

      {document_type === "bill_of_lading" && data && (
        <BillOfLadingResults data={data} />
      )}

      {/* 5. Fallback for Unknown / Scanned / Empty Documents */}
      {(!data || document_type === "unknown") && (
        <div className="fallback-card">
          <HelpCircle size={48} className="fallback-icon" />
          <h3>No Structured Data Extracted</h3>
          <p>
            The backend pipeline was unable to extract structured entities from
            this document.
          </p>
          {raw_text_preview && (
            <div className="preview-snippet">
              <span className="preview-label">Extracted Raw Text Snippet:</span>
              <pre>{raw_text_preview}</pre>
            </div>
          )}
        </div>
      )}

      {/* 6. Raw JSON Inspector */}
      <JsonViewer data={response} />
    </div>
  );
}
