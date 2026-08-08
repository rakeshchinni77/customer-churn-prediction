"""
CLI script to inspect saved model pipeline and stored evaluation metrics.
"""

import json
import sys
from pathlib import Path
import joblib

# Ensure project root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.logger import logger


def main():
    logger.info("Executing evaluate_model.py script...")
    print("\n==========================================")
    print("SAVED MODEL METRICS & PIPELINE SUMMARY")
    print("==========================================")

    if not settings.MODEL_PATH.exists():
        print(f"❌ Model artifact not found at {settings.MODEL_PATH}. Please run scripts/train_model.py first.")
        sys.exit(1)

    if not settings.METRICS_PATH.exists():
        print(f"❌ Metrics artifact not found at {settings.METRICS_PATH}. Please run scripts/train_model.py first.")
        sys.exit(1)

    pipeline = joblib.load(settings.MODEL_PATH)
    with open(settings.METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    print(f"Loaded Pipeline Steps: {[step[0] for step in pipeline.steps]}")
    print("\nModel Performance Metrics:")
    for k, v in metrics.items():
        print(f"  {k.upper()}: {v}")
    print("==========================================\n")


if __name__ == "__main__":
    main()
