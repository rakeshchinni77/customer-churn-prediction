"""
Unit and integration tests for ML model training, evaluation, and serialization.
"""

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.model import (
    load_data,
    prepare_features_and_target,
    train_and_save_model,
    evaluate_model,
)


def test_model_training_and_saving():
    """Verify train_and_save_model() fits pipeline and persists artifacts."""
    pipeline, metrics = train_and_save_model()

    assert isinstance(pipeline, Pipeline)
    assert isinstance(metrics, dict)
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics

    assert settings.MODEL_PATH.exists(), f"Joblib model missing at {settings.MODEL_PATH}"
    assert settings.METRICS_PATH.exists(), f"Metrics JSON missing at {settings.METRICS_PATH}"


def test_joblib_file_exists_and_loads():
    """Verify saved joblib pipeline artifact exists and can be loaded."""
    assert settings.MODEL_PATH.exists()
    loaded_pipeline = joblib.load(settings.MODEL_PATH)
    assert isinstance(loaded_pipeline, Pipeline)
    assert hasattr(loaded_pipeline, "predict")
    assert hasattr(loaded_pipeline, "predict_proba")


def test_metrics_json_file_validity():
    """Verify saved metrics.json file contains valid numerical metrics."""
    assert settings.METRICS_PATH.exists()
    with open(settings.METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    required_keys = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    for key in required_keys:
        assert key in metrics
        assert isinstance(metrics[key], (int, float))
        assert 0.0 <= metrics[key] <= 1.0


def test_model_predict_sample_dataframe():
    """Verify loaded pipeline predicts class and probability on raw sample dataframe."""
    df = load_data()
    X, y, num_cols, cat_cols = prepare_features_and_target(df)

    pipeline = joblib.load(settings.MODEL_PATH)

    # Take a 5-row sample
    sample_df = X.head(5)

    preds = pipeline.predict(sample_df)
    probas = pipeline.predict_proba(sample_df)

    assert len(preds) == 5
    assert all(pred in [0, 1] for pred in preds)
    assert probas.shape == (5, 2)
    assert (probas >= 0.0).all() and (probas <= 1.0).all()
