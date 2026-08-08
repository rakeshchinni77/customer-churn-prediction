"""
CLI script to train, evaluate, and serialize the Customer Churn prediction ML pipeline.
"""

import sys
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.model import train_and_save_model
from app.config import settings
from app.logger import logger


def main():
    logger.info("Executing train_model.py script...")
    print("\n==========================================")
    print("TELCO CHURN MODEL TRAINING PIPELINE")
    print("==========================================")

    try:
        pipeline, metrics = train_and_save_model()
    except Exception as e:
        print(f"\n[ERROR] Training failed with error: {str(e)}")
        sys.exit(1)

    print("✔ Dataset Loaded")
    print("✔ Training Started")
    print("✔ Training Completed")
    print(f"✔ Accuracy:  {metrics['accuracy']}")
    print(f"✔ Precision: {metrics['precision']}")
    print(f"✔ Recall:    {metrics['recall']}")
    print(f"✔ F1 Score:  {metrics['f1_score']}")
    print(f"✔ ROC AUC:   {metrics['roc_auc']}")
    print(f"✔ {settings.MODEL_PATH} created")
    print(f"✔ {settings.METRICS_PATH} created")
    print("==========================================\n")


if __name__ == "__main__":
    main()
