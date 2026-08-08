import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import CustomerForm from '../components/CustomerForm';
import PredictionCard from '../components/PredictionCard';
import EmptyState from '../components/EmptyState';
import Loader from '../components/Loader';
import { predictCustomer, modelInfo } from '../api/api';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [submittedData, setSubmittedData] = useState(null);
  const [latency, setLatency] = useState(null);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    modelInfo()
      .then((data) => setMetrics(data))
      .catch((err) => console.log('Metrics load notice:', err.message));
  }, []);

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setPrediction(null);
    setSubmittedData(formData);

    const startTime = performance.now();

    try {
      const result = await predictCustomer(formData);
      const endTime = performance.now();
      const durationMs = Math.round(endTime - startTime);

      setLatency(durationMs);
      setPrediction(result);

      const statusMsg = result.prediction === 'Yes' ? 'Likely to Churn 🔴' : 'Customer Will Stay 🟢';
      toast.success(`Prediction Complete (${durationMs} ms): ${statusMsg}`);
    } catch (error) {
      toast.error(error.message || 'Failed to calculate churn prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Refined Compact Hero Banner */}
      <div className="hero-banner">
        <div className="container">
          <h1 className="hero-title">Customer Churn Risk Predictor</h1>
          <p className="hero-subtitle">
            Predict customer churn probability using our production-trained RandomForest Classifier.
          </p>

          {metrics && (
            <div className="d-flex flex-wrap justify-content-center gap-2 mt-2">
              <div className="bg-dark bg-opacity-50 border border-secondary border-opacity-25 px-2.5 py-1 rounded-pill" style={{ fontSize: '0.8rem' }}>
                <span className="text-muted">Algorithm:</span> <strong className="text-info">{metrics.model_name}</strong>
              </div>
              <div className="bg-dark bg-opacity-50 border border-secondary border-opacity-25 px-2.5 py-1 rounded-pill" style={{ fontSize: '0.8rem' }}>
                <span className="text-muted">Accuracy:</span> <strong className="text-success">{(metrics.accuracy * 100).toFixed(1)}%</strong>
              </div>
              <div className="bg-dark bg-opacity-50 border border-secondary border-opacity-25 px-2.5 py-1 rounded-pill" style={{ fontSize: '0.8rem' }}>
                <span className="text-muted">ROC AUC:</span> <strong className="text-warning">{(metrics.roc_auc * 100).toFixed(1)}%</strong>
              </div>
              <div className="bg-dark bg-opacity-50 border border-secondary border-opacity-25 px-2.5 py-1 rounded-pill" style={{ fontSize: '0.8rem' }}>
                <span className="text-muted">F1 Score:</span> <strong className="text-primary">{metrics.f1_score}</strong>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="container mb-4">
        <div className="row">
          <div className="col-lg-12">
            <CustomerForm onSubmit={handleFormSubmit} isLoading={loading} />
          </div>

          <div className="col-lg-12">
            {loading && <Loader />}

            {prediction && !loading && (
              <PredictionCard
                predictionResult={prediction}
                customerData={submittedData}
                latencyMs={latency}
              />
            )}

            {!prediction && !loading && <EmptyState />}
          </div>
        </div>
      </div>
    </div>
  );
}
