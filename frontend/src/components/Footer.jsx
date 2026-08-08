import React from 'react';

export default function Footer() {
  const techStack = [
    { name: 'FastAPI', color: '#059669' },
    { name: 'Scikit-Learn', color: '#f59e0b' },
    { name: 'React 19', color: '#06b6d4' },
    { name: 'Docker', color: '#2563eb' },
    { name: 'Bootstrap 5', color: '#7c3aed' },
    { name: 'RandomForest', color: '#10b981' },
  ];

  return (
    <footer
      className="mt-auto py-4 text-center"
      style={{
        backgroundColor: '#0f172a',
        borderTop: '1px solid rgba(255,255,255,0.08)',
      }}
    >
      <div className="container">
        <div className="d-flex flex-wrap justify-content-center align-items-center gap-2 mb-2">
          <span className="text-muted small fw-semibold">Built with:</span>
          {techStack.map((tech) => (
            <span
              key={tech.name}
              className="badge px-2 py-1"
              style={{
                backgroundColor: 'rgba(255,255,255,0.05)',
                border: `1px solid ${tech.color}`,
                color: tech.color,
                fontSize: '0.78rem',
              }}
            >
              {tech.name}
            </span>
          ))}
        </div>
        <p className="mb-0 text-muted small">
          © 2026 Customer Churn Prediction API — Production AI & MLOps System
        </p>
      </div>
    </footer>
  );
}
