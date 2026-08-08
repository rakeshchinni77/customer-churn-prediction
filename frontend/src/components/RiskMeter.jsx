import React from 'react';

export default function RiskMeter({ probability = 0.5 }) {
  // Map probability 0.0 - 1.0 to rotation angle -90 to +90 degrees
  const angle = Math.min(Math.max(probability * 180 - 90, -90), 90);

  let riskLevel = 'Low Risk';
  let badgeClass = 'badge-low-risk';
  if (probability >= 0.7) {
    riskLevel = 'High Risk';
    badgeClass = 'badge-high-risk';
  } else if (probability >= 0.3) {
    riskLevel = 'Medium Risk';
    badgeClass = 'badge-med-risk';
  }

  return (
    <div className="text-center my-3">
      <h6 className="text-uppercase text-muted fw-bold mb-2" style={{ letterSpacing: '1px', fontSize: '0.8rem' }}>
        Customer Risk Meter
      </h6>
      <div className="gauge-container" style={{ position: 'relative', width: '220px', height: '120px', margin: '0 auto' }}>
        <svg viewBox="0 0 200 110" width="220" height="120">
          {/* Gauge Arc Background Segments */}
          {/* Low Risk Segment (Green) */}
          <path d="M 20 100 A 80 80 0 0 1 73 27" fill="none" stroke="#10b981" strokeWidth="18" strokeLinecap="round" />
          {/* Medium Risk Segment (Yellow) */}
          <path d="M 73 27 A 80 80 0 0 1 127 27" fill="none" stroke="#f59e0b" strokeWidth="18" />
          {/* High Risk Segment (Red) */}
          <path d="M 127 27 A 80 80 0 0 1 180 100" fill="none" stroke="#ef4444" strokeWidth="18" strokeLinecap="round" />

          {/* Pivot Circle */}
          <circle cx="100" cy="100" r="8" fill="#f8fafc" />

          {/* Animated Needle */}
          <g transform={`rotate(${angle}, 100, 100)`} className="needle">
            <line x1="100" y1="100" x2="100" y2="35" stroke="#f8fafc" strokeWidth="4" strokeLinecap="round" />
            <polygon points="100,30 95,45 105,45" fill="#f8fafc" />
          </g>
        </svg>
      </div>
      <div className="mt-2">
        <span className={badgeClass}>{riskLevel}</span>
      </div>
    </div>
  );
}
