"""
CLI script to test standalone inference using app.predictor module.
"""

import sys
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.predictor import load_model, predict, predict_proba
from app.logger import logger


def main():
    logger.info("Executing test_predictor.py script...")
    print("\nLoading model...")
    pipeline = load_model()
    print("Model loaded successfully.\n")

    # Sample realistic customer data payload (High churn risk customer)
    sample_customer = {
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

    prediction = predict(sample_customer, model=pipeline)
    probability = predict_proba(sample_customer, model=pipeline)

    print("==========================================")
    print(f"Prediction : {prediction}")
    print(f"Probability : {probability:.2f}")
    print("==========================================\n")


if __name__ == "__main__":
    main()
