import React from 'react';
import CountUp from 'react-countup';

export default function ProbabilityBar({ probability = 0.0 }) {
  const percentage = probability * 100;

  let bgClass = 'bg-success';
  let zoneLabel = 'Safe Zone (Low Risk)';
  if (probability >= 0.7) {
    bgClass = 'bg-danger';
    zoneLabel = 'Critical Zone (High Churn Risk)';
  } else if (probability >= 0.3) {
    bgClass = 'bg-warning text-dark';
    zoneLabel = 'Monitor Zone (Moderate Risk)';
  }

  return (
    <div className="my-3 p-3 rounded" style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
      <div className="d-flex justify-content-between align-items-center mb-2">
        <span className="text-muted small fw-semibold">Probability Gauge</span>
        <span className="text-white small fw-bold">
          Risk Score: <CountUp start={0} end={percentage} decimals={2} duration={1.5} suffix="%" />
        </span>
      </div>

      <div className="progress mb-2" style={{ height: '16px', backgroundColor: '#0f172a', borderRadius: '8px' }}>
        <div
          className={`progress-bar progress-bar-striped progress-bar-animated ${bgClass}`}
          role="progressbar"
          style={{ width: `${percentage}%`, transition: 'width 1.5s ease-in-out' }}
          aria-valuenow={percentage}
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>

      {/* Zone Markers */}
      <div className="row text-center g-0 text-muted" style={{ fontSize: '0.75rem' }}>
        <div className="col-4 border-end border-secondary border-opacity-25" style={{ color: probability < 0.3 ? '#10b981' : '#64748b' }}>
          🟢 Safe Zone (0–30%)
        </div>
        <div className="col-4 border-end border-secondary border-opacity-25" style={{ color: probability >= 0.3 && probability < 0.7 ? '#f59e0b' : '#64748b' }}>
          🟡 Monitor (30–70%)
        </div>
        <div className="col-4" style={{ color: probability >= 0.7 ? '#ef4444' : '#64748b' }}>
          🔴 Critical (70–100%)
        </div>
      </div>
    </div>
  );
}
