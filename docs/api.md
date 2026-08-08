# Telco Customer Churn Prediction — REST API Reference Specification

Production RESTful API for real-time customer churn risk prediction, built with FastAPI, Scikit-Learn, Pydantic v2, and Docker.

---

## Base URLs
- **Local Development**: `http://127.0.0.1:8000` or `http://localhost:8000`
- **Docker Container**: `http://localhost:8000`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 1. System Endpoints

### 1.1 Root Endpoint
Returns basic API metadata and service status.

- **URL**: `/`
- **Method**: `GET`
- **Authentication**: None
- **Success Response**: `200 OK`

```json
{
  "name": "Telco Customer Churn Prediction API",
  "version": "1.0.0",
  "status": "running"
}
```

---

### 1.2 Health Check Endpoint
Monitors application status and verifies that the serialized model pipeline artifact (`models/churn_pipeline.joblib`) is loaded.

- **URL**: `/health`
- **Method**: `GET`
- **Authentication**: None
- **Success Response**: `200 OK`

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

## 2. Model Information Endpoint

### 2.1 Model Metadata & Evaluation Metrics
Retrieves classifier architecture, serialized filename, and test evaluation metrics.

- **URL**: `/model-info`
- **Method**: `GET`
- **Authentication**: None
- **Success Response**: `200 OK`

```json
{
  "model_name": "RandomForestClassifier",
  "model_file": "churn_pipeline.joblib",
  "accuracy": 0.7828,
  "precision": 0.6181,
  "recall": 0.4759,
  "f1_score": 0.5378,
  "roc_auc": 0.822
}
```

---

## 3. Inference Endpoint

### 3.1 Predict Customer Churn
Executes real-time machine learning inference for a single customer payload.

- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Success Response**: `200 OK`
- **Error Response**: `422 Unprocessable Entity` (validation error) / `503 Service Unavailable` (model not loaded)

#### Request Schema (`PredictionRequest` / `CustomerData`)

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `gender` | `string` | Yes | Customer gender (`"Female"`, `"Male"`) | `"Female"` |
| `SeniorCitizen` | `integer` | Yes | Senior citizen status (`0` or `1`) | `0` |
| `Partner` | `string` | Yes | Partner status (`"Yes"`, `"No"`) | `"Yes"` |
| `Dependents` | `string` | Yes | Dependents status (`"Yes"`, `"No"`) | `"No"` |
| `tenure` | `integer` | Yes | Months with company (`>= 0`) | `5` |
| `PhoneService` | `string` | Yes | Phone service (`"Yes"`, `"No"`) | `"Yes"` |
| `MultipleLines` | `string` | Yes | Multiple lines (`"Yes"`, `"No"`, `"No phone service"`) | `"No"` |
| `InternetService` | `string` | Yes | Internet provider (`"Fiber optic"`, `"DSL"`, `"No"`) | `"Fiber optic"` |
| `OnlineSecurity` | `string` | Yes | Online security (`"Yes"`, `"No"`, `"No internet service"`) | `"No"` |
| `OnlineBackup` | `string` | Yes | Online backup (`"Yes"`, `"No"`, `"No internet service"`) | `"Yes"` |
| `DeviceProtection` | `string` | Yes | Device protection (`"Yes"`, `"No"`, `"No internet service"`) | `"No"` |
| `TechSupport` | `string` | Yes | Tech support (`"Yes"`, `"No"`, `"No internet service"`) | `"No"` |
| `StreamingTV` | `string` | Yes | Streaming TV (`"Yes"`, `"No"`, `"No internet service"`) | `"Yes"` |
| `StreamingMovies` | `string` | Yes | Streaming movies (`"Yes"`, `"No"`, `"No internet service"`) | `"No"` |
| `Contract` | `string` | Yes | Contract term (`"Month-to-month"`, `"One year"`, `"Two year"`) | `"Month-to-month"` |
| `PaperlessBilling` | `string` | Yes | Paperless billing (`"Yes"`, `"No"`) | `"Yes"` |
| `PaymentMethod` | `string` | Yes | Payment method (`"Electronic check"`, `"Mailed check"`, etc.) | `"Electronic check"` |
| `MonthlyCharges` | `float` | Yes | Monthly bill amount in USD | `75.2` |
| `TotalCharges` | `float` | Yes | Total bill amount in USD | `375.5` |

#### Sample Request Body
```json
{
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
  "TotalCharges": 375.5
}
```

#### Sample Success Response (`200 OK`)
```json
{
  "prediction": "Yes",
  "prediction_label": "Churn",
  "probability": 0.82,
  "confidence": "82.00%"
}
```

#### Sample Validation Error Response (`422 Unprocessable Entity`)
```json
{
  "success": false,
  "error": "body -> Contract: Field required"
}
```
