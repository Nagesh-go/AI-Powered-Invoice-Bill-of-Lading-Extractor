import React from "react";
import { Ship, Anchor, MapPin, Box, UserCheck, Calendar, ShieldCheck } from "lucide-react";

export default function BillOfLadingResults({ data }) {
  if (!data) return null;

  return (
    <div className="document-results bol-results">
      {/* 1. BOL Key Metadata */}
      <div className="meta-grid">
        <div className="meta-card">
          <div className="meta-icon">
            <Anchor size={18} />
          </div>
          <div>
            <span className="meta-label">Bill of Lading Number</span>
            <span className="meta-value highlight">{data.bol_number || "Not detected"}</span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <Calendar size={18} />
          </div>
          <div>
            <span className="meta-label">Shipment / Onboard Date</span>
            <span className="meta-value">{data.shipment_date || "—"}</span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <Ship size={18} />
          </div>
          <div>
            <span className="meta-label">Vessel & Voyage</span>
            <span className="meta-value">
              {data.vessel_name || "—"} {data.voyage_number ? `(${data.voyage_number})` : ""}
            </span>
          </div>
        </div>

        <div className="meta-card">
          <div className="meta-icon">
            <Box size={18} />
          </div>
          <div>
            <span className="meta-label">Gross Cargo Weight</span>
            <span className="meta-value">
              {data.gross_weight
                ? `${parseFloat(data.gross_weight).toLocaleString()} ${data.weight_unit || ""}`
                : "—"}
            </span>
          </div>
        </div>
      </div>

      {/* 2. Parties Grid */}
      <div className="parties-grid three-col">
        <div className="party-card">
          <div className="party-header">
            <h4>Shipper / Exporter</h4>
          </div>
          <div className="party-body">
            <p className="party-name">{data.shipper_name || "Not detected"}</p>
            <p className="party-address">{data.shipper_address || "—"}</p>
          </div>
        </div>

        <div className="party-card">
          <div className="party-header">
            <h4>Consignee (Receiver)</h4>
          </div>
          <div className="party-body">
            <p className="party-name">{data.consignee_name || "Not detected"}</p>
            <p className="party-address">{data.consignee_address || "—"}</p>
          </div>
        </div>

        <div className="party-card">
          <div className="party-header">
            <UserCheck size={16} className="party-icon" />
            <h4>Notify Party</h4>
          </div>
          <div className="party-body">
            <p className="party-address">{data.notify_party || "Same as Consignee / Not stated"}</p>
          </div>
        </div>
      </div>

      {/* 3. Voyage & Logistics Routing */}
      <div className="section-card">
        <div className="section-title">
          <MapPin size={18} />
          <h4>Routing & Port Logistics</h4>
        </div>
        <div className="logistics-grid">
          <div className="logistics-item">
            <span className="logistics-label">Place of Receipt</span>
            <span className="logistics-value">{data.place_of_receipt || "—"}</span>
          </div>
          <div className="logistics-item">
            <span className="logistics-label">Port of Loading (POL)</span>
            <span className="logistics-value bold">{data.port_of_loading || "—"}</span>
          </div>
          <div className="logistics-item">
            <span className="logistics-label">Port of Discharge (POD)</span>
            <span className="logistics-value bold">{data.port_of_discharge || "—"}</span>
          </div>
          <div className="logistics-item">
            <span className="logistics-label">Final Destination</span>
            <span className="logistics-value">{data.final_destination || "—"}</span>
          </div>
        </div>
      </div>

      {/* 4. Cargo, Containers & Description */}
      <div className="section-card">
        <div className="section-title">
          <Box size={18} />
          <h4>Cargo & Equipment Specification</h4>
        </div>
        <div className="cargo-details">
          <div className="cargo-row">
            <div className="cargo-label">Description of Goods:</div>
            <div className="cargo-text">{data.goods_description || "Not specified"}</div>
          </div>
          <div className="cargo-row">
            <div className="cargo-label">Package Count:</div>
            <div className="cargo-text">{data.package_count || "—"}</div>
          </div>
          <div className="cargo-row">
            <div className="cargo-label">Container Numbers:</div>
            <div className="tags-container">
              {data.container_numbers && data.container_numbers.length > 0 ? (
                data.container_numbers.map((c, i) => (
                  <span key={i} className="chip-tag container-chip">
                    <Box size={12} /> {c}
                  </span>
                ))
              ) : (
                <span className="text-muted">None detected</span>
              )}
            </div>
          </div>
          <div className="cargo-row">
            <div className="cargo-label">Seal Numbers:</div>
            <div className="tags-container">
              {data.seal_numbers && data.seal_numbers.length > 0 ? (
                data.seal_numbers.map((s, i) => (
                  <span key={i} className="chip-tag seal-chip">
                    <ShieldCheck size={12} /> {s}
                  </span>
                ))
              ) : (
                <span className="text-muted">None detected</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
