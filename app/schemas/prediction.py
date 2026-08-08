"""
Pydantic v2 Schemas for API Requests, Responses, Health, and Model Info.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class PredictionRequest(BaseModel):
    """Input payload model containing all customer features required for churn prediction."""

    gender: str = Field(
        ...,
        description="Customer gender ('Male' or 'Female')",
        json_schema_extra={"example": "Female"},
    )
    SeniorCitizen: int = Field(
        ...,
        description="Whether customer is a senior citizen (1 for Yes, 0 for No)",
        ge=0,
        le=1,
        json_schema_extra={"example": 0},
    )
    Partner: str = Field(
        ...,
        description="Whether customer has a partner ('Yes' or 'No')",
        json_schema_extra={"example": "Yes"},
    )
    Dependents: str = Field(
        ...,
        description="Whether customer has dependents ('Yes' or 'No')",
        json_schema_extra={"example": "No"},
    )
    tenure: int = Field(
        ...,
        description="Number of months customer has stayed with company",
        ge=0,
        json_schema_extra={"example": 5},
    )
    PhoneService: str = Field(
        ...,
        description="Whether customer has phone service ('Yes' or 'No')",
        json_schema_extra={"example": "Yes"},
    )
    MultipleLines: str = Field(
        ...,
        description="Whether customer has multiple lines ('Yes', 'No', 'No phone service')",
        json_schema_extra={"example": "No"},
    )
    InternetService: str = Field(
        ...,
        description="Customer's internet service provider ('DSL', 'Fiber optic', 'No')",
        json_schema_extra={"example": "Fiber optic"},
    )
    OnlineSecurity: str = Field(
        ...,
        description="Whether customer has online security ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "No"},
    )
    OnlineBackup: str = Field(
        ...,
        description="Whether customer has online backup ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "Yes"},
    )
    DeviceProtection: str = Field(
        ...,
        description="Whether customer has device protection ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "No"},
    )
    TechSupport: str = Field(
        ...,
        description="Whether customer has tech support ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "No"},
    )
    StreamingTV: str = Field(
        ...,
        description="Whether customer has streaming TV ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "Yes"},
    )
    StreamingMovies: str = Field(
        ...,
        description="Whether customer has streaming movies ('Yes', 'No', 'No internet service')",
        json_schema_extra={"example": "No"},
    )
    Contract: str = Field(
        ...,
        description="Contract term ('Month-to-month', 'One year', 'Two year')",
        json_schema_extra={"example": "Month-to-month"},
    )
    PaperlessBilling: str = Field(
        ...,
        description="Whether customer has paperless billing ('Yes' or 'No')",
        json_schema_extra={"example": "Yes"},
    )
    PaymentMethod: str = Field(
        ...,
        description="Payment method ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)')",
        json_schema_extra={"example": "Electronic check"},
    )
    MonthlyCharges: float = Field(
        ...,
        description="Monthly charge amount in USD",
        ge=0.0,
        json_schema_extra={"example": 75.2},
    )
    TotalCharges: float = Field(
        ...,
        description="Total charge amount in USD",
        ge=0.0,
        json_schema_extra={"example": 375.5},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


# Alias for CustomerData
CustomerData = PredictionRequest


class PredictionResponse(BaseModel):
    """Output prediction response model."""

    prediction: str = Field(..., description="'Yes' or 'No'", json_schema_extra={"example": "Yes"})
    prediction_label: str = Field(
        ..., description="'Churn' or 'No Churn'", json_schema_extra={"example": "Churn"}
    )
    probability: float = Field(
        ..., description="Churn probability between 0.0 and 1.0", json_schema_extra={"example": 0.81}
    )
    confidence: str = Field(
        ..., description="Formatted confidence percentage string", json_schema_extra={"example": "81.00%"}
    )


class RootResponse(BaseModel):
    """Root endpoint response model."""

    name: str = Field(..., json_schema_extra={"example": "Telco Customer Churn Prediction API"})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    status: str = Field(..., json_schema_extra={"example": "running"})


class HealthResponse(BaseModel):
    """Health status response model."""

    status: str = Field(..., json_schema_extra={"example": "healthy"})
    model_loaded: bool = Field(..., json_schema_extra={"example": True})


class ModelInfoResponse(BaseModel):
    """Model information and metrics response model."""

    model_name: str = Field(..., json_schema_extra={"example": "RandomForestClassifier"})
    model_file: str = Field(..., json_schema_extra={"example": "churn_pipeline.joblib"})
    accuracy: float = Field(..., json_schema_extra={"example": 0.7828})
    precision: float = Field(..., json_schema_extra={"example": 0.6181})
    recall: float = Field(..., json_schema_extra={"example": 0.4759})
    f1_score: float = Field(..., json_schema_extra={"example": 0.5378})
    roc_auc: float = Field(..., json_schema_extra={"example": 0.822})
