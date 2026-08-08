import React from 'react';
import CountUp from 'react-countup';
import RiskMeter from './RiskMeter';
import ProbabilityBar from './ProbabilityBar';
import PredictionChart from './PredictionChart';

export default function PredictionCard({ predictionResult, customerData, latencyMs }) {
  if (!predictionResult) return null;

  const { prediction, probability, confidence } = predictionResult;
  const isHighRisk = probability >= 0.7;
  const isMedRisk = probability >= 0.3 && probability < 0.7;
  const isLowRisk = probability < 0.3;

  // Extract numerical confidence percentage for badge rule
  const confVal = parseFloat(confidence?.replace('%', '') || (probability * 100).toFixed(2));

  // Task 3: Confidence Badge logic
  let confidenceBadge = (
    <span className="badge px-3 py-2" style={{ backgroundColor: 'rgba(239, 68, 68, 0.2)', color: '#ef4444', border: '1px solid #ef4444' }}>
      🟠 Low Confidence
    </span>
  );
  if (confVal >= 90) {
    confidenceBadge = (
      <span className="badge px-3 py-2" style={{ backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981', border: '1px solid #10b981' }}>
        🟢 High Confidence
      </span>
    );
  } else if (confVal >= 70) {
    confidenceBadge = (
      <span className="badge px-3 py-2" style={{ backgroundColor: 'rgba(245, 158, 11, 0.2)', color: '#f59e0b', border: '1px solid #f59e0b' }}>
        🟡 Moderate Confidence
      </span>
    );
  }

  // Task 8: Risk Level & Prediction Status
  let riskLevelBadge = <span className="badge-high-risk">HIGH RISK</span>;
  let predictionTitle = <span className="text-danger">🔴 Customer Likely To Churn</span>;

  if (isLowRisk) {
    riskLevelBadge = <span className="badge-low-risk">LOW RISK</span>;
    predictionTitle = <span className="text-success">🟢 Customer Will Stay</span>;
  } else if (isMedRisk) {
    riskLevelBadge = <span className="badge-med-risk">MEDIUM RISK</span>;
    predictionTitle = <span className="text-warning">🟡 Customer May Churn</span>;
  }

  return (
    <div className="glass-card mb-4">
      {/* Header */}
      <div className="card-header-custom d-flex flex-wrap justify-content-between align-items-center gap-2">
        <div className="d-flex align-items-center gap-2">
          <span>⚡ Real-Time Churn Risk Assessment</span>
          {latencyMs !== undefined && (
            <span className="badge bg-dark border border-secondary text-info ms-2" style={{ fontSize: '0.8rem' }}>
              ⏱️ Processed in {latencyMs} ms
            </span>
          )}
        </div>
        <div>{riskLevelBadge}</div>
      </div>

      <div className="p-4">
        {/* Task 8: Better Prediction Status Header */}
        <div className="row align-items-center text-center text-md-start mb-4">
          <div className="col-md-6 mb-3 mb-md-0 border-end border-secondary border-opacity-25">
            <span className="text-uppercase text-muted fw-bold" style={{ fontSize: '0.78rem', letterSpacing: '1px' }}>
              Prediction Outcome
            </span>
            <h2 className="fw-extrabold mt-1 mb-1" style={{ fontSize: '1.85rem' }}>
              {predictionTitle}
            </h2>
            <div className="mt-2">{confidenceBadge}</div>
          </div>

          {/* Task 5: Animated Numbers */}
          <div className="col-md-6 ps-md-4">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="text-muted small">Churn Probability:</span>
              <span className="fw-bold text-white fs-4">
                <CountUp start={0} end={probability * 100} decimals={2} duration={1.5} suffix="%" />
              </span>
            </div>
            <div className="d-flex justify-content-between align-items-center">
              <span className="text-muted small">Model Confidence Score:</span>
              <span className="fw-bold text-info fs-5">
                <CountUp start={0} end={confVal} decimals={2} duration={1.5} suffix="%" />
              </span>
            </div>
          </div>
        </div>

        <hr className="border-secondary opacity-25 my-4" />

        {/* Risk Meter & Charts */}
        <div className="row align-items-center mb-4">
          <div className="col-lg-5 mb-4 mb-lg-0">
            <RiskMeter probability={probability} />
          </div>
          <div className="col-lg-7">
            <ProbabilityBar probability={probability} />
            <PredictionChart probability={probability} />
          </div>
        </div>

        {/* Task 2 & Task 4: Model Info & Important Inputs Cards */}
        <div className="row g-3 mt-2">
          {/* Task 4: Important Inputs Section */}
          {customerData && (
            <div className="col-md-7">
              <div className="card h-100 bg-dark bg-opacity-50 border-secondary border-opacity-25 p-3">
                <h6 className="text-primary fw-bold mb-3 d-flex align-items-center gap-1" style={{ fontSize: '0.9rem' }}>
                  <span>🔍 Key Customer Input Factors</span>
                </h6>
                <div className="row g-2 small">
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Contract:</span>{' '}
                    <span className="text-white">{customerData.Contract}</span>
                  </div>
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Internet:</span>{' '}
                    <span className="text-white">{customerData.InternetService}</span>
                  </div>
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Monthly Charges:</span>{' '}
                    <span className="text-white">${customerData.MonthlyCharges}</span>
                  </div>
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Tenure:</span>{' '}
                    <span className="text-white">{customerData.tenure} Months</span>
                  </div>
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Tech Support:</span>{' '}
                    <span className="text-white">{customerData.TechSupport}</span>
                  </div>
                  <div className="col-6">
                    <span className="text-success fw-bold">✓ Online Security:</span>{' '}
                    <span className="text-white">{customerData.OnlineSecurity}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Task 2: Model Information Card */}
          <div className={customerData ? 'col-md-5' : 'col-md-12'}>
            <div className="card h-100 bg-dark bg-opacity-50 border-secondary border-opacity-25 p-3">
              <h6 className="text-info fw-bold mb-3 d-flex align-items-center gap-1" style={{ fontSize: '0.9rem' }}>
                <span>🤖 Model Architecture</span>
              </h6>
              <div className="row g-2 small text-muted">
                <div className="col-6">
                  <div>Model Algorithm</div>
                  <div className="text-white fw-semibold">RandomForest</div>
                </div>
                <div className="col-6">
                  <div>Model Version</div>
                  <div className="text-white fw-semibold">v1.0</div>
                </div>
                <div className="col-6 mt-2">
                  <div>Total Features</div>
                  <div className="text-white fw-semibold">19 Features</div>
                </div>
                <div className="col-6 mt-2">
                  <div>Training Dataset</div>
                  <div className="text-white fw-semibold">7,043 Customers</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
