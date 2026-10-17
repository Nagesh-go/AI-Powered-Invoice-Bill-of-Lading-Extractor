import React, { useState } from "react";
import { Check, ChevronRight, FileSpreadsheet, Code, Table as TableIcon } from "lucide-react";

export default function ExtractedFieldsList({ response, isLoading }) {
  const [activeTab, setActiveTab] = useState("fields"); // 'fields' | 'items' | 'json'

  if (isLoading) {
    return (
      <div className="extracted-card">
        <div className="card-header">
          <h3>Extracted Data</h3>
          <span className="badge-pill">Analyzing...</span>
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
          <span>Upload an Invoice or Bill of Lading to see extracted entities.</span>
        </div>
      </div>
    );
  }

  const { document_type, data } = response;
  const isInvoice = document_type === "invoice";

  // Build field rows dynamically based on document type
  const fields = isInvoice
    ? [
        { label: "Invoice No", value: data.invoice_number },
        { label: "Invoice Date", value: data.invoice_date },
        { label: "Due Date", value: data.due_date },
        { label: "Bill To / Customer", value: data.customer_name },
        { label: "Customer Address", value: data.customer_address },
        { label: "Vendor / Supplier", value: data.vendor_name },
        { label: "Subtotal", value: data.subtotal ? `${data.currency || "$"} ${data.subtotal}` : null },
        { label: "Tax Amount", value: data.tax_amount ? `${data.currency || "$"} ${data.tax_amount}` : null },
        { label: "Total Amount Due", value: data.total_amount ? `${data.currency || "$"} ${data.total_amount}` : null, highlight: true },
      ]
    : [
        { label: "BOL Number", value: data.bol_number, highlight: true },
        { label: "Shipment Date", value: data.shipment_date },
        { label: "Shipper / Exporter", value: data.shipper_name },
        { label: "Consignee", value: data.consignee_name },
        { label: "Vessel & Voyage", value: `${data.vessel_name || ""} ${data.voyage_number ? `(${data.voyage_number})` : ""}`.trim() || null },
        { label: "Port of Loading", value: data.port_of_loading },
        { label: "Port of Discharge", value: data.port_of_discharge },
        { label: "Container(s)", value: data.container_numbers ? data.container_numbers.join(", ") : null },
        { label: "Gross Weight", value: data.gross_weight ? `${data.gross_weight} ${data.weight_unit || ""}` : null },
      ];

  return (
    <div className="extracted-card">
      {/* Card Header & Tabs */}
      <div className="card-header">
        <div className="header-title-row">
          <h3>Extracted Data</h3>
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

      {/* Tab 1: Key Fields (Matches Screenshot Design) */}
      {activeTab === "fields" && (
        <div className="fields-table">
          {fields.map((f, idx) => (
            <div key={idx} className={`field-row ${f.highlight ? "highlight-row" : ""}`}>
              <span className="field-label">{f.label}</span>
              <span className="field-value">
                {f.value || <span className="field-null">—</span>}
              </span>
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
          ))}
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
          <pre>
            <code>{JSON.stringify(response, null, 2)}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
