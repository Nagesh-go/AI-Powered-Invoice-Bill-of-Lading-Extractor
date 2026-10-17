import React from "react";

export default function Logo({ size = 32, showText = true }) {
  return (
    <div className="docuflow-brand-logo">
      <div className="logo-symbol-wrap" style={{ width: size, height: size }}>
        <svg
          viewBox="0 0 40 40"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="brand-svg"
        >
          <defs>
            <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#4F46E5" />
              <stop offset="50%" stopColor="#7C3AED" />
              <stop offset="100%" stopColor="#06B6D4" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#4F46E5" floodOpacity="0.35" />
            </filter>
          </defs>

          {/* Hexagonal Document Crystal Badge */}
          <rect
            x="3"
            y="3"
            width="34"
            height="34"
            rx="10"
            fill="url(#logoGrad)"
            filter="url(#glow)"
          />

          {/* Inner Document Flow Lines */}
          <path
            d="M12 14C12 12.8954 12.8954 12 14 12H22L28 18V26C28 27.1046 27.1046 28 26 28H14C12.8954 28 12 27.1046 12 26V14Z"
            fill="white"
            fillOpacity="0.95"
          />
          <path
            d="M22 12V17C22 17.5523 22.4477 18 23 18H28"
            fill="#C7D2FE"
          />

          {/* Dynamic Laser Flow Pulse Dots */}
          <circle cx="16" cy="21" r="1.5" fill="#4F46E5" />
          <circle cx="20" cy="21" r="1.5" fill="#4F46E5" />
          <circle cx="24" cy="21" r="1.5" fill="#4F46E5" />
          <rect x="15" y="24" width="10" height="1.8" rx="0.9" fill="#7C3AED" />
        </svg>
      </div>

      {showText && (
        <div className="brand-text-block">
          <div className="brand-title-line">
            <span className="brand-name-primary">DocuFlow</span>
            <span className="brand-name-ai">AI</span>
          </div>
          <span className="brand-tagline">Intelligent Document Engine</span>
        </div>
      )}
    </div>
  );
}
