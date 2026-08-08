"""
Legacy schema module forwarding to app.schemas package.
"""

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    CustomerData,
    RootResponse,
    HealthResponse,
    ModelInfoResponse,
)

__all__ = [
    "PredictionRequest",
    "PredictionResponse",
    "CustomerData",
    "RootResponse",
    "HealthResponse",
    "ModelInfoResponse",
]
