import React from 'react';

export default function EmptyState() {
  return (
    <div
      className="glass-card p-5 text-center my-4"
      style={{
        border: '2px dashed rgba(255, 255, 255, 0.15)',
        backgroundColor: 'rgba(21, 28, 44, 0.6)',
      }}
    >
      <div
        className="mx-auto mb-3 d-flex align-items-center justify-content-center"
        style={{
          width: '70px',
          height: '70px',
          borderRadius: '50%',
          backgroundColor: 'rgba(59, 130, 246, 0.15)',
          fontSize: '2.5rem',
        }}
      >
        🤖
      </div>
      <h4 className="text-white fw-bold mb-2">No Prediction Generated Yet</h4>
      <p className="text-muted mx-auto mb-0" style={{ maxWidth: '500px', fontSize: '1rem' }}>
        Fill in the customer information form above and click{' '}
        <strong className="text-primary">🚀 Predict Churn Risk</strong> to generate a real-time machine learning prediction.
      </p>
    </div>
  );
}
