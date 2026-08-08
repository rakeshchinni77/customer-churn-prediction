# Customer Churn Risk Predictor

Production-ready Machine Learning web application that predicts customer churn in telecommunications using a Random Forest classifier with a FastAPI RESTful backend and an interactive React frontend dashboard.

---

## Features

- ✔ **Customer Churn Prediction**: Real-time risk probability score and classification label.
- ✔ **Random Forest Classifier**: Trained on 7,043 Telco customer records using 19 engineered features.
- ✔ **High Model Performance**: 78.28% Accuracy, 82.20% ROC-AUC.
- ✔ **REST API with FastAPI**: Lifespan startup model loading, Pydantic v2 validation, and consistent JSON error formats.
- ✔ **Interactive React Dashboard**: React 19 + Vite dashboard with prefill sample buttons ("High Risk" / "Low Risk").
- ✔ **Risk Gauge Meter**: Semicircular SVG gauge with animated needle pointing to exact churn risk level.
- ✔ **Probability Breakdown Charts**: Recharts BarChart visualizing Retention vs Churn probabilities.
- ✔ **Model Information Card**: Live model metadata (RandomForest, v1.0, 19 Features, 7,043 Customers).
- ✔ **Explainable Input Factors**: Card highlighting submitted customer input attributes associated with churn.
- ✔ **Docker Support**: Single-command Docker Compose orchestration (FastAPI + Nginx React SPA).
- ✔ **Swagger & ReDoc Documentation**: Interactive OpenAPI testing interfaces.
- ✔ **Responsive UI**: Bootstrap 5 responsive layout for Desktop, Tablet, and Mobile devices.
- ✔ **Automated Tests**: 28 passing Pytest unit & integration tests.

---

## Tech Stack

### Frontend
- **React 19** (Vite build engine)
- **Bootstrap 5** (Responsive layout & grid system)
- **Recharts** (Data visualization charts)
- **Axios** (Async HTTP client)
- **React Hook Form** (Form validation & state)
- **React Toastify** (Notifications)
- **React CountUp** (Animated numerical counters)

### Backend
- **FastAPI** (ASGI web framework)
- **Scikit-Learn** (ColumnTransformer & RandomForestClassifier pipeline)
- **Pandas & NumPy** (Data manipulation)
- **Pydantic v2** (Data validation & schemas)
- **Joblib** (Model serialization)
- **Uvicorn** (ASGI server)

### DevOps & Infrastructure
- **Docker** (Containerization)
- **Docker Compose** (Multi-container orchestration)
- **Nginx Alpine** (Static SPA reverse proxy & gzip compression)
- **GitHub** (Version control & CI workflows)

### Testing
- **Pytest** (Automated test runner)
- **FastAPI TestClient & HTTPX** (API endpoint integration testing)

---

## Project Structure

```text
customer-churn-prediction/
│
├── app/                              # FastAPI Backend Application
│   ├── api/
│   │   └── routes.py                 # REST Endpoints (/, /health, /model-info, /predict)
│   ├── core/
│   │   ├── config.py                 # Configuration loader
│   │   ├── exceptions.py             # Custom exception handlers & status codes
│   │   └── logger.py                 # Centralized logging module
│   ├── schemas/
│   │   └── prediction.py             # Pydantic v2 Request/Response Schemas
│   ├── services/
│   │   └── predictor_service.py      # Inference service bridge
│   ├── config.py                     # Root config
│   ├── exceptions.py                 # Legacy exception exports
│   ├── logger.py                     # Root logger
│   ├── main.py                       # FastAPI Application entry point & lifespan
│   ├── model.py                      # Data loader & ML Pipeline training functions
│   ├── predictor.py                  # Standalone inference helper
│   ├── schemas.py                    # Legacy schema exports
│   └── utils.py                      # Data utility functions
│
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Telco Churn Dataset
│
├── docs/                             # Documentation Assets
│   ├── architecture.svg              # Architecture Diagram
│   ├── api.md                        # Complete API Reference Specification
│   └── screenshots/                  # Application Screenshots
│       ├── README.md                 # Screenshots index guide
│       ├── home.png
│       ├── prediction.png
│       ├── swagger.png
│       ├── docker.png
│       ├── mobile.png
│       └── high-risk.png
│
├── frontend/                         # React Frontend Application
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js                # Axios client functions
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── CustomerForm.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── RiskMeter.jsx
│   │   │   ├── ProbabilityBar.jsx
│   │   │   ├── PredictionChart.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   ├── Loader.jsx
│   │   │   └── Footer.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── styles/
│   │   │   └── app.css
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── constants.js
│   ├── .dockerignore
│   ├── Dockerfile                    # Multi-stage Node -> Nginx Dockerfile
│   ├── nginx.conf                    # Nginx SPA config
│   ├── package.json
│   └── vite.config.js
│
├── models/                           # Serialized Model Artifacts
│   ├── churn_pipeline.joblib         # Encapsulated ColumnTransformer + Classifier
│   └── metrics.json                  # Accuracy, Precision, Recall, F1, ROC-AUC
│
├── notebooks/
│   └── eda.ipynb                     # Exploratory Data Analysis Notebook
│
├── scripts/
│   ├── load_dataset.py               # Dataset inspection script
│   ├── train_model.py                # Pipeline training & serialization script
│   ├── evaluate_model.py             # Metrics validation script
│   └── test_predictor.py             # Standalone inference test script
│
├── tests/                            # Automated Pytest Suite
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_api_endpoints.py
│   ├── test_dataset.py
│   ├── test_model.py
│   ├── test_pipeline.py
│   ├── test_prediction.py
│   └── test_validation.py
│
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml                # Docker Compose Orchestration
├── Dockerfile                        # Backend Dockerfile
├── postman_collection.json           # Postman Collection v2.1
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # Main Documentation
```

---

## System Architecture

```text
                 User (Web Browser / Postman)
                              │
                              ▼
                React Frontend (Port 3000 / Nginx)
                              │
                    Axios HTTP POST /predict
                              │
                              ▼
                FastAPI Backend (Port 8000 / Uvicorn)
                              │
                     Input Validation (Pydantic)
                              │
              Scikit-Learn RandomForest Pipeline
             (ColumnTransformer: Imputer + Scaler + Encoder)
                              │
                    Probability Calculation
                              │
                              ▼
                   JSON Response Output
                 {"prediction": "Yes", "probability": 0.82}
                              │
                              ▼
        Dashboard Visualization (Risk Gauge + Recharts + Badges)
```

> Detailed SVG diagram saved at [`docs/architecture.svg`](docs/architecture.svg).

---

## Application Screenshots

Key views are documented inside [`docs/screenshots/`](docs/screenshots/):
- **Dashboard Overview**: `docs/screenshots/home.png`
- **Real-Time Prediction Card**: `docs/screenshots/prediction.png`
- **High Risk Alert**: `docs/screenshots/high-risk.png`
- **Swagger Documentation**: `docs/screenshots/swagger.png`
- **Docker Compose Execution**: `docs/screenshots/docker.png`
- **Mobile Viewport**: `docs/screenshots/mobile.png`

---

## Model Performance Metrics

Evaluation results calculated on a 20% stratified test set (1,409 customers):

| Metric | Score | Description |
| :--- | :--- | :--- |
| **Algorithm** | `RandomForest` | 200 balanced decision trees |
| **Accuracy** | `78.28%` | Overall correct prediction rate |
| **ROC-AUC** | `82.20%` | Area under ROC Curve |
| **Precision** | `61.81%` | True churners among positive predictions |
| **Recall** | `47.59%` | Actual churners correctly identified |
| **F1 Score** | `0.5378` | Harmonic mean of Precision and Recall |
| **Dataset** | `Telco Customer Churn` | 7,043 records, 19 feature attributes |

---

## Installation & Setup Guide (Local Development)

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/rakeshchinni77/customer-churn-prediction.git
cd customer-churn-prediction

python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Backend Dependencies & Train Model
```bash
pip install -r requirements.txt
python scripts/train_model.py
```

### 3. Run FastAPI Backend Server
```bash
uvicorn app.main:app --reload
```
*Backend runs at `http://127.0.0.1:8000`.*

### 4. Install & Run React Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs at `http://localhost:3000` (or Vite port `http://localhost:5173`).*

---

## Docker Deployment Guide (Phase 6)

Launch the entire stack (FastAPI + Nginx React SPA) with a single command:
```bash
docker compose up --build
```

### Access URLs
- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Docker Management Commands
```bash
# Stop containers
docker compose down

# View live container logs
docker compose logs -f

# Run tests inside running backend container
docker compose exec backend pytest
```

---

## Swagger API Guide

Access [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to test endpoints interactively using Swagger UI.

### Available Endpoints
- `GET /`: Service name, version, and running status.
- `GET /health`: Server health check and model load status.
- `GET /model-info`: Classifier metadata and stored evaluation metrics.
- `POST /predict`: Submit customer attributes JSON to calculate churn probability.

---

## Frontend Workflow Guide

1. Open `http://localhost:3000`.
2. Click **"🔥 Load High Risk Sample"** or **"🛡️ Load Low Risk Sample"** to instantly prefill customer features.
3. Click **"🚀 Predict Churn Risk"**.
4. View real-time outputs:
   - **Churn Prediction Label** (🟢 Customer Will Stay / 🔴 Customer Likely To Churn)
   - **Confidence Score & Badge** (🟢 High / 🟡 Moderate / 🟠 Low Confidence)
   - **Latency Timing** (`⏱️ Processed in 18 ms`)
   - **Semicircular Risk Gauge Meter**
   - **Probability Gauge Bar** (Safe Zone / Monitor Zone / Critical Zone)
   - **Recharts Probability Breakdown Chart**
   - **Key Customer Input Factors Card**
   - **Model Architecture Card**

---

## 🔌 API Reference & Payload Format

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | API status metadata |
| `/health` | `GET` | Health status and model load state |
| `/model-info` | `GET` | Model evaluation metrics |
| `/predict` | `POST` | Calculate customer churn prediction |

> Detailed endpoint specification available in [`docs/api.md`](docs/api.md).

### Sample Request (`POST /predict`)
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

### Sample Response (`200 OK`)
```json
{
  "prediction": "Yes",
  "prediction_label": "Churn",
  "probability": 0.82,
  "confidence": "82.00%"
}
```

---

## ⚙️ Environment Variables

### Backend Configuration (`.env`)
```ini
APP_NAME="Telco Customer Churn Prediction API"
APP_ENV="production"
HOST="0.0.0.0"
PORT=8000
MODEL_PATH="models/churn_pipeline.joblib"
METRICS_PATH="models/metrics.json"
DATA_PATH="data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
LOG_LEVEL="INFO"
```

### Frontend Configuration (`frontend/.env`)
```ini
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🧪 Testing

Run the automated test suite locally:
```bash
pytest
```
**Expected Result**:
```text
======================= 28 passed in 2.86s =======================
```

Run tests inside the active Docker container:
```bash
docker compose exec backend pytest
```

---

## Future Improvements & Roadmap

- [ ] **SHAP Explainability**: Integrate SHAP (SHapley Additive exPlanations) force plots for individual feature impact.
- [ ] **XGBoost & LightGBM Benchmarking**: Compare Random Forest against gradient boosting models.
- [ ] **User Authentication**: Add JWT authentication & user role management.
- [ ] **Prediction History Database**: Store historical predictions in PostgreSQL / MongoDB.
- [ ] **Batch CSV Predictions**: Allow users to upload bulk CSV files for batch inference.
- [ ] **Automated CI/CD Pipeline**: GitHub Actions workflow for building and pushing Docker images.
- [ ] **Cloud Deployment**: Deploy containerized stack on AWS ECS / GCP Cloud Run.

---

## 📄 License
Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
