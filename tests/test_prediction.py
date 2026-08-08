"""
Unit tests for app.predictor module logic.
"""

import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.predictor import load_model, predict, predict_proba
from app.exceptions import ModelNotFoundException, InvalidInputException


@pytest.fixture
def sample_customer_payload():
    return {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 1,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 95.70,
        "TotalCharges": 95.70,
    }


def test_load_model_returns_pipeline():
    """Verify load_model() loads a valid Scikit-Learn pipeline."""
    pipeline = load_model()
    assert hasattr(pipeline, "predict")
    assert hasattr(pipeline, "predict_proba")


def test_load_model_missing_file_raises_exception():
    """Verify load_model() raises ModelNotFoundException when path is invalid."""
    with pytest.raises(ModelNotFoundException):
        load_model(model_path="invalid/path/nonexistent.joblib")


def test_predict_returns_yes_or_no(sample_customer_payload):
    """Verify predict() returns 'Yes' or 'No' string."""
    result = predict(sample_customer_payload)
    assert result in ["Yes", "No"]


def test_predict_proba_returns_valid_float(sample_customer_payload):
    """Verify predict_proba() returns float between 0.0 and 1.0."""
    proba = predict_proba(sample_customer_payload)
    assert isinstance(proba, float)
    assert 0.0 <= proba <= 1.0


def test_predict_invalid_input_raises_exception():
    """Verify invalid/empty input payload raises InvalidInputException."""
    with pytest.raises(InvalidInputException):
        predict({})

    with pytest.raises(InvalidInputException):
        predict(None)  # type: ignore
