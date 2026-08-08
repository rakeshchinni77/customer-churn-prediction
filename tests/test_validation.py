"""
Unit tests for Pydantic input request schema validation.
"""

import pytest
from pydantic import ValidationError
from app.schemas.prediction import PredictionRequest


def test_prediction_request_valid_payload():
    """Verify valid dictionary instantiates PredictionRequest cleanly."""
    payload = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 75.2,
        "TotalCharges": 375.5,
    }
    req = PredictionRequest(**payload)
    assert req.gender == "Female"
    assert req.tenure == 5
    assert req.MonthlyCharges == 75.2


def test_prediction_request_invalid_senior_citizen():
    """Verify SeniorCitizen outside 0 or 1 raises ValidationError."""
    payload = {
        "gender": "Female",
        "SeniorCitizen": 5,  # Invalid (>1)
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 75.2,
        "TotalCharges": 375.5,
    }
    with pytest.raises(ValidationError):
        PredictionRequest(**payload)
