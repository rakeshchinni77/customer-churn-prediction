"""
Integration tests for FastAPI REST endpoints: GET /, GET /health, GET /model-info, POST /predict.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app

client = TestClient(app)


@pytest.fixture
def valid_customer_payload():
    return {
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


def test_get_root_endpoint():
    """Verify GET / returns 200 OK with API name, version, and status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Telco Customer Churn Prediction API"
    assert "version" in data
    assert data["status"] == "running"


def test_get_health_endpoint():
    """Verify GET /health returns 200 OK with status and model_loaded boolean."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "model_loaded" in data
    assert data["model_loaded"] is True


def test_get_model_info_endpoint():
    """Verify GET /model-info returns 200 OK with evaluation metrics."""
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "RandomForestClassifier"
    assert data["model_file"] == "churn_pipeline.joblib"
    assert "accuracy" in data
    assert "precision" in data
    assert "recall" in data
    assert "f1_score" in data
    assert "roc_auc" in data


def test_post_predict_valid_payload(valid_customer_payload):
    """Verify POST /predict returns 200 OK with valid prediction schema."""
    response = client.post("/predict", json=valid_customer_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in ["Yes", "No"]
    assert "prediction_label" in data
    assert data["prediction_label"] in ["Churn", "No Churn"]
    assert "probability" in data
    assert isinstance(data["probability"], float)
    assert 0.0 <= data["probability"] <= 1.0
    assert "confidence" in data
    assert "%" in data["confidence"]


def test_post_predict_missing_required_field(valid_customer_payload):
    """Verify POST /predict returns 422 Unprocessable Entity when required field is missing."""
    invalid_payload = valid_customer_payload.copy()
    del invalid_payload["Contract"]  # Remove required field

    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert "Contract" in data["error"]


def test_post_predict_invalid_datatype(valid_customer_payload):
    """Verify POST /predict returns 422 Unprocessable Entity when data type is wrong."""
    invalid_payload = valid_customer_payload.copy()
    invalid_payload["tenure"] = "invalid_string_instead_of_int"

    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert "tenure" in data["error"]
