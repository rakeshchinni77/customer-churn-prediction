import React, { useEffect, useState } from 'react';
import { healthCheck } from '../api/api';

export default function Navbar() {
  const [apiStatus, setApiStatus] = useState({ loaded: false, status: 'connecting...' });

  useEffect(() => {
    healthCheck()
      .then((data) => setApiStatus({ loaded: data.model_loaded, status: data.status }))
      .catch(() => setApiStatus({ loaded: false, status: 'offline' }));
  }, []);

  return (
    <nav className="navbar navbar-expand-lg sticky-top" style={{ backgroundColor: '#0f172a', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
      <div className="container-fluid px-4">
        <a className="navbar-brand d-flex align-items-center gap-2" href="#">
          <span style={{ fontSize: '1.5rem' }}>⚡</span>
          <span className="fw-bold text-white fs-5">Telco Churn Predictor</span>
        </a>

        <div className="d-flex align-items-center gap-3 ms-auto">
          {apiStatus.status === 'healthy' ? (
            <span className="badge-low-risk py-1 px-3" style={{ fontSize: '0.8rem' }}>
              ● API Online & Model Loaded
            </span>
          ) : (
            <span className="badge-high-risk py-1 px-3" style={{ fontSize: '0.8rem' }}>
              ● API Offline / Disconnected
            </span>
          )}

          <a
            href="https://github.com/rakeshchinni77/customer-churn-prediction"
            target="_blank"
            rel="noreferrer"
            className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1 text-white border-secondary"
          >
            <span>GitHub Repository</span>
          </a>
        </div>
      </div>
    </nav>
  );
}
