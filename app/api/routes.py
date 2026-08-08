"""
API Routes definitions for Root, Health, Model Info, and Churn Prediction endpoints.
"""

from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.logger import logger
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    RootResponse,
    HealthResponse,
    ModelInfoResponse,
)
from app.services.predictor_service import (
    is_model_loaded,
    get_model_metrics_info,
    run_churn_prediction,
)

router = APIRouter()


@router.get(
    "/",
    response_model=RootResponse,
    summary="API Root Information",
    description="Returns the API name, current version, and service status.",
    tags=["System"],
)
def get_root():
    """Root endpoint returning API service status."""
    logger.info("Root endpoint hit.")
    return RootResponse(
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
        status="running",
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API & Model Health Check",
    description="Checks service health and confirms whether the serialized ML model pipeline is loaded.",
    tags=["System"],
)
def get_health():
    """Health check endpoint confirming service and model status."""
    logger.info("Health check endpoint hit.")
    loaded = is_model_loaded()
    health_status = "healthy" if loaded else "degraded"
    return HealthResponse(
        status=health_status,
        model_loaded=loaded,
    )


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Model Architecture & Performance Metrics",
    description="Retrieves the classifier algorithm name, model filename, and test evaluation metrics.",
    tags=["Model"],
)
def get_model_info():
    """Endpoint returning stored model performance metrics."""
    logger.info("Model info endpoint hit.")
    try:
        info = get_model_metrics_info()
        return ModelInfoResponse(**info)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading model information: {str(e)}",
        )


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Customer Churn",
    description="Accepts customer features JSON payload, passes data through the ML pipeline, and returns prediction label and probability.",
    tags=["Inference"],
)
def predict_churn(payload: PredictionRequest):
    """Prediction endpoint for customer churn inference."""
    logger.info("Predict endpoint hit.")
    if not is_model_loaded():
        logger.error("Model is not loaded. Cannot execute prediction.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please train the model artifact first.",
        )

    try:
        response = run_churn_prediction(payload)
        return response
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction calculation failed: {str(e)}",
        )
