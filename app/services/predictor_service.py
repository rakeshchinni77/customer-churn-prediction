"""
Predictor service layer for invoking model loading, inference, and metric retrieval.
"""

import json
from typing import Dict, Any
from app.config import settings
from app.logger import logger
from app.predictor import load_model, predict, predict_proba
from app.schemas.prediction import PredictionRequest, PredictionResponse, ModelInfoResponse


def is_model_loaded() -> bool:
    """Check if model pipeline file exists and can be loaded."""
    try:
        pipeline = load_model()
        return pipeline is not None
    except Exception as e:
        logger.warning(f"Model health check failed: {str(e)}")
        return False


def get_model_metrics_info() -> Dict[str, Any]:
    """Retrieve model metadata and metrics from saved json file."""
    metrics_path = settings.METRICS_PATH
    if not metrics_path.exists():
        logger.error(f"Metrics file missing at: {metrics_path}")
        raise FileNotFoundError("Model metrics artifact missing.")

    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)

        return {
            "model_name": "RandomForestClassifier",
            "model_file": settings.MODEL_PATH.name,
            "accuracy": metrics_data.get("accuracy", 0.0),
            "precision": metrics_data.get("precision", 0.0),
            "recall": metrics_data.get("recall", 0.0),
            "f1_score": metrics_data.get("f1_score", 0.0),
            "roc_auc": metrics_data.get("roc_auc", 0.0),
        }
    except Exception as e:
        logger.error(f"Failed to read model metrics file: {str(e)}")
        raise RuntimeError(f"Could not load model info: {str(e)}") from e


def run_churn_prediction(payload: PredictionRequest) -> PredictionResponse:
    """
    Execute churn prediction for incoming Pydantic payload.

    Parameters
    ----------
    payload : PredictionRequest
        Validated Pydantic model.

    Returns
    -------
    PredictionResponse
        Prediction result containing label, probability, and confidence.
    """
    customer_dict = payload.model_dump()
    logger.info(f"Processing prediction request for customer tenure={payload.tenure}, Contract='{payload.Contract}'")

    raw_prediction = predict(customer_dict)
    probability = predict_proba(customer_dict)

    label = "Churn" if raw_prediction == "Yes" else "No Churn"
    confidence_str = f"{probability * 100:.2f}%"

    return PredictionResponse(
        prediction=raw_prediction,
        prediction_label=label,
        probability=probability,
        confidence=confidence_str,
    )
