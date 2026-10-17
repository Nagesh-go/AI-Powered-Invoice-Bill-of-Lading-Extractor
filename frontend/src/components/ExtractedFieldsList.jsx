import React, { useState } from "react";
import { Check, Edit2, CheckCircle2, RotateCcw, Copy } from "lucide-react";

export default function ExtractedFieldsList({ response, isLoading, onUpdateField }) {
  const [activeTab, setActiveTab] = useState("fields"); // 'fields' | 'items' | 'json'
  const [editingKey, setEditingKey] = useState(null);
  const [editValue, setEditValue] = useState("");
  const [copied, setCopied] = useState(false);

  if (isLoading) {
    return (
      <div className="extracted-card">
        <div className="card-header">
          <h3>Extracted Data</h3>
          <span className="badge-pill">Analyzing Document...</span>
        </div>
        <div className="skeleton-list">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="skeleton-row">
              <div className="skeleton-label"></div>
              <div className="skeleton-value"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!response || !response.data) {
    return (
      <div className="extracted-card empty-card">
        <div className="card-header">
          <h3>Extracted Data</h3>
        </div>
        <div className="empty-fields-state">
          <p>No document processed yet.</p>
          <span>Select an Invoice or Bill of Lading from the left preview.</span>
        </div>
      </div>
    );
  }

  const { document_type, data } = response;
  const isInvoice = document_type === "invoice";

  const fields = isInvoice
    ? [
        { key: "invoice_number", label: "Invoice No", value: data.invoice_number },
        { key: "invoice_date", label: "Invoice Date", value: data.invoice_date },
        { key: "due_date", label: "Due Date", value: data.due_date },
        { key: "customer_name", label: "Bill To Name", value: data.customer_name },
        { key: "customer_address", label: "Address", value: data.customer_address },
        { key: "vendor_name", label: "Vendor / Supplier", value: data.vendor_name },
        { key: "subtotal", label: "Subtotal", value: data.subtotal },
        { key: "tax_amount", label: "Tax Amount", value: data.tax_amount },
        { key: "total_amount", label: "Total Due", value: data.total_amount, highlight: true },
      ]
    : [
        { key: "bol_number", label: "BOL Number", value: data.bol_number, highlight: true },
        { key: "shipment_date", label: "Shipment Date", value: data.shipment_date },
        { key: "shipper_name", label: "Shipper / Exporter", value: data.shipper_name },
        { key: "consignee_name", label: "Consignee", value: data.consignee_name },
        { key: "vessel_name", label: "Vessel Name", value: data.vessel_name },
        { key: "voyage_number", label: "Voyage Number", value: data.voyage_number },
        { key: "port_of_loading", label: "Port of Loading", value: data.port_of_loading },
        { key: "port_of_discharge", label: "Port of Discharge", value: data.port_of_discharge },
        { key: "gross_weight", label: "Gross Weight", value: `${data.gross_weight || ""} ${data.weight_unit || ""}`.trim() },
      ];

  const handleStartEdit = (key, currentVal) => {
    setEditingKey(key);
    setEditValue(currentVal || "");
  };

  const handleSaveEdit = (key) => {
    if (onUpdateField) {
      onUpdateField(key, editValue);
    }
    setEditingKey(null);
  };

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(response, null, 2)).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="extracted-card">
      {/* Card Header & Tabs */}
      <div className="card-header">
        <div className="header-title-row">
          <div>
            <h3>Extracted Data</h3>
            <span className="subtitle-hint">Click any field to edit manually</span>
          </div>
          <span className="doc-type-pill">
            {isInvoice ? "Invoice" : "Bill of Lading"}
          </span>
        </div>

        <div className="tab-pills">
          <button
            type="button"
            className={`tab-btn ${activeTab === "fields" ? "active" : ""}`}
            onClick={() => setActiveTab("fields")}
          >
            Key Fields
          </button>
          {isInvoice && data.line_items && data.line_items.length > 0 && (
            <button
              type="button"
              className={`tab-btn ${activeTab === "items" ? "active" : ""}`}
              onClick={() => setActiveTab("items")}
            >
              Line Items ({data.line_items.length})
            </button>
          )}
          <button
            type="button"
            className={`tab-btn ${activeTab === "json" ? "active" : ""}`}
            onClick={() => setActiveTab("json")}
          >
            Raw JSON
          </button>
        </div>
      </div>

      {/* Tab 1: Key Fields */}
      {activeTab === "fields" && (
        <div className="fields-table">
          {fields.map((f) => {
            const isEditing = editingKey === f.key;
            return (
              <div
                key={f.key}
                className={`field-row ${f.highlight ? "highlight-row" : ""} ${
                  isEditing ? "is-editing" : ""
                }`}
              >
                <span className="field-label">{f.label}</span>

                {isEditing ? (
                  <div className="field-edit-box">
                    <input
                      type="text"
                      className="field-input"
                      value={editValue}
                      autoFocus
                      onChange={(e) => setEditValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleSaveEdit(f.key);
                        if (e.key === "Escape") setEditingKey(null);
                      }}
                    />
                    <button
                      type="button"
                      className="btn-save-inline"
                      onClick={() => handleSaveEdit(f.key)}
                    >
                      <Check size={14} />
                    </button>
                  </div>
                ) : (
                  <span
                    className="field-value clickable"
                    onClick={() => handleStartEdit(f.key, f.value)}
                    title="Click to edit value"
                  >
                    {f.value || <span className="field-null">—</span>}
                    <Edit2 size={12} className="edit-hint-icon" />
                  </span>
                )}

                <div className="field-status">
                  {f.value ? (
                    <span className="check-badge" title="Validated with Pydantic">
                      <Check size={14} />
                    </span>
                  ) : (
                    <span className="empty-badge">—</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Tab 2: Itemized Line Items Table */}
      {activeTab === "items" && isInvoice && (
        <div className="line-items-view">
          <table className="mini-table">
            <thead>
              <tr>
                <th>Description</th>
                <th style={{ textAlign: "right" }}>Qty</th>
                <th style={{ textAlign: "right" }}>Unit Price</th>
                <th style={{ textAlign: "right" }}>Total</th>
              </tr>
            </thead>
            <tbody>
              {data.line_items.map((item, i) => (
                <tr key={i}>
                  <td className="item-title">{item.description}</td>
                  <td style={{ textAlign: "right" }}>{item.quantity ?? "—"}</td>
                  <td style={{ textAlign: "right" }}>
                    {item.unit_price ? `${data.currency || "$"} ${item.unit_price}` : "—"}
                  </td>
                  <td style={{ textAlign: "right", fontWeight: "600" }}>
                    {item.line_total ? `${data.currency || "$"} ${item.line_total}` : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 3: Formatted Raw JSON */}
      {activeTab === "json" && (
        <div className="raw-json-view">
          <div className="json-toolbar">
            <button type="button" className="btn-copy-sm" onClick={handleCopyJson}>
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? "Copied!" : "Copy JSON"}
            </button>
          </div>
          <pre>
            <code>{JSON.stringify(response, null, 2)}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
