import React from 'react';
import { useForm } from 'react-hook-form';
import { FORM_OPTIONS, HIGH_RISK_SAMPLE, LOW_RISK_SAMPLE } from '../constants';

export default function CustomerForm({ onSubmit, isLoading }) {
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm({
    defaultValues: HIGH_RISK_SAMPLE,
  });

  const loadPreset = (presetData) => {
    Object.keys(presetData).forEach((key) => {
      setValue(key, presetData[key]);
    });
  };

  return (
    <div className="glass-card mb-4">
      <div className="card-header-custom d-flex flex-wrap justify-content-between align-items-center gap-2">
        <span>📋 Customer Feature Specification Form</span>
        <div className="d-flex gap-2">
          <button
            type="button"
            className="btn-sample"
            onClick={() => loadPreset(HIGH_RISK_SAMPLE)}
            disabled={isLoading}
          >
            🔥 Load High Risk Sample
          </button>
          <button
            type="button"
            className="btn-sample"
            onClick={() => loadPreset(LOW_RISK_SAMPLE)}
            disabled={isLoading}
          >
            🛡️ Load Low Risk Sample
          </button>
        </div>
      </div>

      <div className="p-4">
        <form onSubmit={handleSubmit(onSubmit)}>
          {/* Section 1: Demographics & Account Overview */}
          <div className="mb-4">
            <h6 className="text-primary fw-bold mb-3">1. General Customer Details</h6>
            <div className="row g-3">
              <div className="col-md-4 col-sm-6">
                <label className="form-label">Gender</label>
                <select className="form-select" {...register('gender', { required: true })}>
                  {FORM_OPTIONS.gender.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Senior Citizen</label>
                <select
                  className="form-select"
                  {...register('SeniorCitizen', { valueAsNumber: true, required: true })}
                >
                  {FORM_OPTIONS.SeniorCitizen.map((opt) => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Partner</label>
                <select className="form-select" {...register('Partner', { required: true })}>
                  {FORM_OPTIONS.Partner.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Dependents</label>
                <select className="form-select" {...register('Dependents', { required: true })}>
                  {FORM_OPTIONS.Dependents.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Tenure (Months)</label>
                <input
                  type="number"
                  min="0"
                  className={`form-control ${errors.tenure ? 'is-invalid' : ''}`}
                  {...register('tenure', { valueAsNumber: true, required: true, min: 0 })}
                />
              </div>
            </div>
          </div>

          <hr className="border-secondary opacity-25" />

          {/* Section 2: Telecom & Network Services */}
          <div className="mb-4">
            <h6 className="text-primary fw-bold mb-3">2. Phone & Internet Services</h6>
            <div className="row g-3">
              <div className="col-md-4 col-sm-6">
                <label className="form-label">Phone Service</label>
                <select className="form-select" {...register('PhoneService', { required: true })}>
                  {FORM_OPTIONS.PhoneService.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Multiple Lines</label>
                <select className="form-select" {...register('MultipleLines', { required: true })}>
                  {FORM_OPTIONS.MultipleLines.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Internet Service</label>
                <select className="form-select" {...register('InternetService', { required: true })}>
                  {FORM_OPTIONS.InternetService.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Online Security</label>
                <select className="form-select" {...register('OnlineSecurity', { required: true })}>
                  {FORM_OPTIONS.OnlineSecurity.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Online Backup</label>
                <select className="form-select" {...register('OnlineBackup', { required: true })}>
                  {FORM_OPTIONS.OnlineBackup.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <hr className="border-secondary opacity-25" />

          {/* Section 3: Value Add Services */}
          <div className="mb-4">
            <h6 className="text-primary fw-bold mb-3">3. Value-Added Features & Streaming</h6>
            <div className="row g-3">
              <div className="col-md-3 col-sm-6">
                <label className="form-label">Device Protection</label>
                <select className="form-select" {...register('DeviceProtection', { required: true })}>
                  {FORM_OPTIONS.DeviceProtection.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-3 col-sm-6">
                <label className="form-label">Tech Support</label>
                <select className="form-select" {...register('TechSupport', { required: true })}>
                  {FORM_OPTIONS.TechSupport.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-3 col-sm-6">
                <label className="form-label">Streaming TV</label>
                <select className="form-select" {...register('StreamingTV', { required: true })}>
                  {FORM_OPTIONS.StreamingTV.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-3 col-sm-6">
                <label className="form-label">Streaming Movies</label>
                <select className="form-select" {...register('StreamingMovies', { required: true })}>
                  {FORM_OPTIONS.StreamingMovies.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <hr className="border-secondary opacity-25" />

          {/* Section 4: Contract & Billing */}
          <div className="mb-4">
            <h6 className="text-primary fw-bold mb-3">4. Contract & Payment Terms</h6>
            <div className="row g-3">
              <div className="col-md-4 col-sm-6">
                <label className="form-label">Contract Type</label>
                <select className="form-select" {...register('Contract', { required: true })}>
                  {FORM_OPTIONS.Contract.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Paperless Billing</label>
                <select className="form-select" {...register('PaperlessBilling', { required: true })}>
                  {FORM_OPTIONS.PaperlessBilling.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-4 col-sm-6">
                <label className="form-label">Payment Method</label>
                <select className="form-select" {...register('PaymentMethod', { required: true })}>
                  {FORM_OPTIONS.PaymentMethod.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              <div className="col-md-6 col-sm-6">
                <label className="form-label">Monthly Charges ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className={`form-control ${errors.MonthlyCharges ? 'is-invalid' : ''}`}
                  {...register('MonthlyCharges', { valueAsNumber: true, required: true, min: 0 })}
                />
              </div>

              <div className="col-md-6 col-sm-6">
                <label className="form-label">Total Charges ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  className={`form-control ${errors.TotalCharges ? 'is-invalid' : ''}`}
                  {...register('TotalCharges', { valueAsNumber: true, required: true, min: 0 })}
                />
              </div>
            </div>
          </div>

          <div className="text-center mt-4">
            <button type="submit" className="btn btn-predict" disabled={isLoading}>
              {isLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Processing ML Inference...
                </>
              ) : (
                '🚀 Predict Churn Risk'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
