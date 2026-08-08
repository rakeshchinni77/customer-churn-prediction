import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Telco Customer Churn Prediction API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    MODEL_PATH: Path = BASE_DIR / os.getenv("MODEL_PATH", "models/churn_pipeline.joblib")
    METRICS_PATH: Path = BASE_DIR / os.getenv("METRICS_PATH", "models/metrics.json")
    DATA_PATH: Path = BASE_DIR / os.getenv("DATA_PATH", "data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
