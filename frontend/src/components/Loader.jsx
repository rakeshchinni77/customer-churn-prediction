import React from 'react';

export default function Loader({ message = 'Running ML Model Inference...' }) {
  return (
    <div className="glass-card p-5 text-center my-4">
      <div className="spinner-border text-primary" role="status" style={{ width: '3rem', height: '3rem' }}>
        <span className="visually-hidden">Loading...</span>
      </div>
      <h5 className="mt-3 text-white fw-bold">{message}</h5>
      <p className="text-muted mb-0">Executing RandomForest Pipeline on customer attributes</p>
    </div>
  );
}
