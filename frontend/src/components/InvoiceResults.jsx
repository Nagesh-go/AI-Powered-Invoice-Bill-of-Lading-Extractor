import React from "react";
import { Building2, User, CreditCard, Calendar, Hash, FileCheck } from "lucide-react";

export default function InvoiceResults({ data }) {
  if (!data) return null;

  const currency = data.currency || "$";

  const formatMoney = (val) => {
    if (val === null || val === undefined || val === "") return "—";
    const num = parseFloat(val);
    if (isNaN(num)) return val;
    return `${currency} ${num.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  };

  return (
    <div className="document-results invoice-results">
      {/* 1. Header Information Bar */}
      <div className="meta-grid">
        <div className="meta-card">
          <div className="meta-icon">
            <Hash size={18} />
          </div>
          <div>
            <span className="meta-label">Invoice Number</span>
            <span className="meta-value highlight">{data.invoice_number || "Not detected"}</span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <Calendar size={18} />
          </div>
          <div>
            <span className="meta-label">Invoice Date</span>
            <span className="meta-value">{data.invoice_date || "—"}</span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <Calendar size={18} />
          </div>
          <div>
            <span className="meta-label">Due Date</span>
            <span className="meta-value">{data.due_date || "—"}</span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <CreditCard size={18} />
          </div>
          <div>
            <span className="meta-label">Payment Terms</span>
            <span className="meta-value">{data.payment_terms || "—"}</span>
          </div>
        </div>
      </div>

      {/* 2. Parties: Vendor vs Customer */}
      <div className="parties-grid">
        <div className="party-card">
          <div className="party-header">
            <Building2 size={18} className="party-icon" />
            <h4>Vendor / Supplier</h4>
          </div>
          <div className="party-body">
            <p className="party-name">{data.vendor_name || "Name not detected"}</p>
            <p className="party-address">{data.vendor_address || "Address not detected"}</p>
            {data.purchase_order_number && (
              <p className="party-extra">
                <strong>PO Number:</strong> {data.purchase_order_number}
              </p>
            )}
          </div>
        </div>

        <div className="party-card">
          <div className="party-header">
            <User size={18} className="party-icon" />
            <h4>Customer / Bill To</h4>
          </div>
          <div className="party-body">
            <p className="party-name">{data.customer_name || "Name not detected"}</p>
            <p className="party-address">{data.customer_address || "Address not detected"}</p>
          </div>
        </div>
      </div>

      {/* 3. Itemized Line Items Table */}
      <div className="section-card">
        <div className="section-title">
          <FileCheck size={18} />
          <h4>Itemized Line Items ({data.line_items ? data.line_items.length : 0})</h4>
        </div>

        {data.line_items && data.line_items.length > 0 ? (
          <div className="table-responsive">
            <table className="items-table">
              <thead>
                <tr>
                  <th style={{ width: "50%" }}>Description</th>
                  <th style={{ textAlign: "right" }}>Qty</th>
                  <th style={{ textAlign: "right" }}>Unit Price</th>
                  <th style={{ textAlign: "right" }}>Line Total</th>
                </tr>
              </thead>
              <tbody>
                {data.line_items.map((item, idx) => (
                  <tr key={idx}>
                    <td className="item-desc">{item.description}</td>
                    <td style={{ textAlign: "right" }}>{item.quantity ?? "—"}</td>
                    <td style={{ textAlign: "right" }}>{formatMoney(item.unit_price)}</td>
                    <td style={{ textAlign: "right", fontWeight: "600" }}>
                      {formatMoney(item.line_total)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="empty-line-items">No itemized line items found on this invoice.</p>
        )}
      </div>

      {/* 4. Financial Totals Card */}
      <div className="totals-wrapper">
        <div className="totals-card">
          <div className="total-row">
            <span>Subtotal (Pre-Tax):</span>
            <span>{formatMoney(data.subtotal)}</span>
          </div>
          <div className="total-row">
            <span>Tax / VAT:</span>
            <span>{formatMoney(data.tax_amount)}</span>
          </div>
          {data.shipping_amount && (
            <div className="total-row">
              <span>Freight / Shipping:</span>
              <span>{formatMoney(data.shipping_amount)}</span>
            </div>
          )}
          {data.discount_amount && (
            <div className="total-row discount">
              <span>Discounts:</span>
              <span>-{formatMoney(data.discount_amount)}</span>
            </div>
          )}
          <div className="total-row grand-total">
            <span>Total Amount Due:</span>
            <span className="grand-amount">{formatMoney(data.total_amount)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
