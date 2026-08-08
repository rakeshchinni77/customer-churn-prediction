"""
Unit tests for pipeline construction, feature preparation, and ColumnTransformer integrity.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.model import (
    load_data,
    prepare_features_and_target,
    build_pipeline,
)


def test_prepare_features_and_target():
    """Verify feature matrix X and target y extraction."""
    df = load_data()
    X, y, num_cols, cat_cols = prepare_features_and_target(df)

    assert "customerID" not in X.columns
    assert "Churn" not in X.columns
    assert len(y) == len(X)
    assert set(y.unique()).issubset({0, 1})
    assert len(num_cols) + len(cat_cols) == X.shape[1]


def test_build_pipeline_structure():
    """Verify built pipeline structure contains preprocessor and classifier steps."""
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    cat_cols = ["gender", "Contract", "InternetService"]

    pipeline = build_pipeline(num_cols, cat_cols)

    assert isinstance(pipeline, Pipeline)
    assert len(pipeline.steps) == 2
    assert pipeline.steps[0][0] == "preprocessor"
    assert pipeline.steps[1][0] == "classifier"


def test_pipeline_fit_predict_on_synthetic_data():
    """Verify pipeline fits and predicts cleanly on synthetic sample data with missing values."""
    synthetic_data = pd.DataFrame({
        "tenure": [1, 12, None, 48, 72],
        "MonthlyCharges": [29.85, 56.95, 89.90, None, 105.50],
        "TotalCharges": [29.85, 684.75, None, 4300.00, 7500.00],
        "gender": ["Female", "Male", "Male", None, "Female"],
        "Contract": ["Month-to-month", "One year", "Two year", "Month-to-month", None],
        "InternetService": ["DSL", "Fiber optic", "No", "DSL", "Fiber optic"],
    })
    synthetic_target = pd.Series([0, 1, 0, 1, 0])

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    cat_cols = ["gender", "Contract", "InternetService"]

    pipeline = build_pipeline(num_cols, cat_cols)
    pipeline.fit(synthetic_data, synthetic_target)

    preds = pipeline.predict(synthetic_data)
    probas = pipeline.predict_proba(synthetic_data)

    assert len(preds) == 5
    assert probas.shape == (5, 2)
