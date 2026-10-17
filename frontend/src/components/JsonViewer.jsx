import React, { useState } from "react";
import { Code, Copy, Check, ChevronDown, ChevronRight } from "lucide-react";

export default function JsonViewer({ data }) {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const formattedJson = JSON.stringify(data, null, 2);

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(formattedJson).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="json-viewer-container">
      <div className="json-header" onClick={() => setIsOpen(!isOpen)}>
        <div className="json-title">
          {isOpen ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
          <Code size={18} />
          <span>Raw Structured JSON Payload</span>
        </div>
        <button
          type="button"
          className="btn-copy-json"
          onClick={handleCopy}
          title="Copy raw JSON to clipboard"
        >
          {copied ? (
            <>
              <Check size={14} className="text-success" /> Copied!
            </>
          ) : (
            <>
              <Copy size={14} /> Copy JSON
            </>
          )}
        </button>
      </div>

      {isOpen && (
        <div className="json-body">
          <pre className="json-code">
            <code>{formattedJson}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
