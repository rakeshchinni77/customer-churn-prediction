"""
Unit and integration tests for dataset loading and inspection functions.
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.model import (
    load_data,
    get_dataset_shape,
    get_column_names,
    get_missing_summary,
    get_target_distribution,
    get_feature_lists,
)


def test_dataset_file_exists():
    """Verify dataset CSV file exists at configured DATA_PATH."""
    assert settings.DATA_PATH.exists(), f"Dataset file missing at {settings.DATA_PATH}"


def test_load_data_returns_dataframe():
    """Verify load_data() loads a non-empty DataFrame."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) > 0


def test_churn_column_exists():
    """Verify Churn column exists in dataset."""
    df = load_data()
    assert "Churn" in df.columns


def test_total_charges_converted_to_numeric():
    """Verify TotalCharges is converted to float numeric type with NaNs for empty strings."""
    df = load_data()
    assert "TotalCharges" in df.columns
    assert pd.api.types.is_float_dtype(df["TotalCharges"])
    # Verify the 11 known missing blank values converted to NaN
    assert df["TotalCharges"].isnull().sum() == 11


def test_no_duplicate_column_names():
    """Verify no duplicate column names exist in loaded dataset."""
    df = load_data()
    columns = get_column_names(df)
    assert len(columns) == len(set(columns))


def test_dataset_shape_and_features():
    """Verify dataset shape and feature extraction logic."""
    df = load_data()
    rows, cols = get_dataset_shape(df)
    assert rows == 7043
    assert cols == 21

    cat_cols, num_cols = get_feature_lists(df)
    assert "gender" in cat_cols
    assert "Contract" in cat_cols
    assert "tenure" in num_cols
    assert "MonthlyCharges" in num_cols
    assert "TotalCharges" in num_cols


def test_target_distribution():
    """Verify target distribution contains expected class counts."""
    df = load_data()
    dist = get_target_distribution(df, target_col="Churn")
    assert "Yes" in dist
    assert "No" in dist
    assert dist["No"]["count"] == 5174
    assert dist["Yes"]["count"] == 1869
