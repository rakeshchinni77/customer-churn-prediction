"""
Data Loading, Inspection, Machine Learning Pipeline Building, Training,
Evaluation, and Model Serialization for Customer Churn Prediction.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.config import settings
from app.logger import logger


def load_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Load the Telco Customer Churn dataset from a CSV file.

    Parameters
    ----------
    filepath : Optional[Union[str, Path]], optional
        Path to the CSV file. If None, uses settings.DATA_PATH.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame with cleaned column names and numeric TotalCharges.

    Raises
    ------
    FileNotFoundError
        If the specified filepath does not exist on disk.
    """
    path = Path(filepath) if filepath else Path(settings.DATA_PATH)
    logger.info(f"Attempting to load dataset from: {path}")

    if not path.exists():
        error_msg = f"Dataset file not found at path: {path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        df = pd.read_csv(path)
    except Exception as e:
        logger.error(f"Failed to parse CSV file at {path}: {str(e)}")
        raise ValueError(f"Invalid CSV file format: {str(e)}") from e

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Convert TotalCharges space strings to numeric (NaN for empty/spaces)
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"].astype(str).str.strip(), errors="coerce"
        )

    logger.info(f"Dataset successfully loaded. Shape: {df.shape}")
    return df


# -----------------------------------------------------------------------------
# Data Inspection Helpers (Phase 1 Compatibility)
# -----------------------------------------------------------------------------

def get_dataset_shape(df: pd.DataFrame) -> Tuple[int, int]:
    """Return dataset shape as (rows, columns)."""
    return df.shape


def get_column_names(df: pd.DataFrame) -> List[str]:
    """Return list of column names."""
    return list(df.columns)


def get_data_types(df: pd.DataFrame) -> pd.Series:
    """Return data types of each column."""
    return df.dtypes


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive summary statistics for numerical columns."""
    return df.describe(include="all")


def get_duplicate_count(df: pd.DataFrame) -> int:
    """Return count of duplicate rows in DataFrame."""
    return int(df.duplicated().sum())


def get_unique_counts(df: pd.DataFrame) -> pd.Series:
    """Return count of unique values per column."""
    return df.nunique()


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing values summary per column."""
    total = df.isnull().sum()
    percent = (total / len(df)) * 100
    missing_df = pd.DataFrame(
        {"missing_count": total, "missing_percentage": percent.round(2)}
    )
    return missing_df[missing_df["missing_count"] > 0]


def get_target_distribution(
    df: pd.DataFrame, target_col: str = "Churn"
) -> Dict[str, Dict[str, float]]:
    """Calculate class distribution and percentages for target column."""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")

    counts = df[target_col].value_counts().to_dict()
    percentages = (df[target_col].value_counts(normalize=True) * 100).to_dict()

    distribution = {
        class_name: {
            "count": int(counts[class_name]),
            "percentage": float(round(percentages[class_name], 2)),
        }
        for class_name in counts
    }
    logger.info(f"Target variable ('{target_col}') distribution: {distribution}")
    return distribution


def get_feature_lists(
    df: pd.DataFrame, target_col: str = "Churn", id_col: str = "customerID"
) -> Tuple[List[str], List[str]]:
    """Identify and return lists of categorical and numerical features."""
    feature_cols = [c for c in df.columns if c not in [target_col, id_col]]

    categorical_features = [
        col for col in feature_cols if df[col].dtype == "object"
    ]
    numerical_features = [
        col for col in feature_cols if df[col].dtype in ["int64", "float64"]
    ]

    logger.info(
        f"Features identified: {len(categorical_features)} categorical, "
        f"{len(numerical_features)} numerical."
    )
    return categorical_features, numerical_features


# -----------------------------------------------------------------------------
# Phase 2 ML Pipeline & Model Functions
# -----------------------------------------------------------------------------

def prepare_features_and_target(
    df: pd.DataFrame, target_col: str = "Churn", id_col: str = "customerID"
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
    """
    Prepare feature matrix X and target vector y from dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset DataFrame.
    target_col : str
        Target column name ('Churn').
    id_col : str
        Identifier column name ('customerID').

    Returns
    -------
    Tuple[pd.DataFrame, pd.Series, List[str], List[str]]
        (X, y, numerical_cols, categorical_cols)
    """
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' missing from DataFrame.")

    # Copy DataFrame to avoid modifying original
    df_clean = df.copy()

    # Drop identifier column if present
    if id_col in df_clean.columns:
        df_clean = df_clean.drop(columns=[id_col])

    # Encode binary target: Yes -> 1, No -> 0
    if df_clean[target_col].dtype == "object":
        target_map = {"Yes": 1, "No": 0}
        y = df_clean[target_col].map(target_map)
        if y.isnull().any():
            raise ValueError("Target column contains unexpected non-binary values.")
    else:
        y = df_clean[target_col]

    X = df_clean.drop(columns=[target_col])

    # Automatically identify feature types
    categorical_cols = [
        col for col in X.columns if X[col].dtype == "object"
    ]
    numerical_cols = [
        col for col in X.columns if X[col].dtype in ["int64", "float64"]
    ]

    logger.info(
        f"Prepared X matrix with {X.shape[1]} features ({len(numerical_cols)} numerical, "
        f"{len(categorical_cols)} categorical) and target vector y."
    )
    return X, y, numerical_cols, categorical_cols


def build_pipeline(
    numerical_cols: List[str], categorical_cols: List[str]
) -> Pipeline:
    """
    Construct a unified Scikit-Learn Pipeline with ColumnTransformer preprocessing
    and RandomForestClassifier.

    Parameters
    ----------
    numerical_cols : List[str]
        List of numerical feature names.
    categorical_cols : List[str]
        List of categorical feature names.

    Returns
    -------
    Pipeline
        Encapsulated Pipeline ready for training.
    """
    # Preprocessing for numerical variables
    num_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # Preprocessing for categorical variables
    cat_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    # Combine transformers in ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, numerical_cols),
            ("cat", cat_transformer, categorical_cols),
        ]
    )

    # Full unified Pipeline with RandomForest Classifier
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    logger.info("Built unified Scikit-Learn pipeline (ColumnTransformer + RandomForestClassifier).")
    return pipeline


def evaluate_model(
    pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> Dict[str, float]:
    """
    Evaluate trained pipeline on test set and return performance metrics.

    Parameters
    ----------
    pipeline : Pipeline
        Fitted Scikit-Learn pipeline.
    X_test : pd.DataFrame
        Test feature matrix.
    y_test : pd.Series
        True test target labels.

    Returns
    -------
    Dict[str, float]
        Dictionary of metrics (accuracy, precision, recall, f1_score, roc_auc).
    """
    logger.info("Evaluating model pipeline on test data...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(round(accuracy_score(y_test, y_pred), 4)),
        "precision": float(round(precision_score(y_test, y_pred, zero_division=0), 4)),
        "recall": float(round(recall_score(y_test, y_pred, zero_division=0), 4)),
        "f1_score": float(round(f1_score(y_test, y_pred, zero_division=0), 4)),
        "roc_auc": float(round(roc_auc_score(y_test, y_proba), 4)),
    }

    logger.info(f"Evaluation Metrics: {metrics}")
    print("\n==========================================")
    print("CLASSIFICATION REPORT")
    print("==========================================")
    print(classification_report(y_test, y_pred, target_names=["No Churn (0)", "Churn (1)"]))
    print("==========================================")
    print("CONFUSION MATRIX")
    print("==========================================")
    print(confusion_matrix(y_test, y_pred))
    print("==========================================\n")

    return metrics


def save_pipeline(
    pipeline: Pipeline, filepath: Optional[Union[str, Path]] = None
) -> Path:
    """
    Serialize and save fitted pipeline artifact to disk using joblib.

    Parameters
    ----------
    pipeline : Pipeline
        Fitted pipeline.
    filepath : Optional[Union[str, Path]], optional
        Destination filepath. Defaults to settings.MODEL_PATH.

    Returns
    -------
    Path
        Absolute path to saved model artifact file.
    """
    save_path = Path(filepath) if filepath else Path(settings.MODEL_PATH)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        joblib.dump(pipeline, save_path)
        logger.info(f"Pipeline successfully saved to {save_path}")
    except Exception as e:
        logger.error(f"Failed to save pipeline to {save_path}: {str(e)}")
        raise RuntimeError(f"Pipeline saving failed: {str(e)}") from e

    return save_path


def save_metrics(
    metrics: Dict[str, float], filepath: Optional[Union[str, Path]] = None
) -> Path:
    """
    Save evaluation metrics to JSON file.

    Parameters
    ----------
    metrics : Dict[str, float]
        Metrics dictionary.
    filepath : Optional[Union[str, Path]], optional
        Destination filepath. Defaults to settings.METRICS_PATH.

    Returns
    -------
    Path
        Path to saved JSON metrics file.
    """
    save_path = Path(filepath) if filepath else Path(settings.METRICS_PATH)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Metrics successfully saved to {save_path}")
    except Exception as e:
        logger.error(f"Failed to save metrics to {save_path}: {str(e)}")
        raise RuntimeError(f"Metrics saving failed: {str(e)}") from e

    return save_path


def train_and_save_model(
    data_filepath: Optional[Union[str, Path]] = None,
) -> Tuple[Pipeline, Dict[str, float]]:
    """
    End-to-end model training execution:
    1. Load Data
    2. Prepare Features & Target
    3. Stratified Train-Test Split (80/20)
    4. Build Pipeline
    5. Fit Pipeline
    6. Evaluate Metrics
    7. Persist Pipeline and Metrics to Disk

    Returns
    -------
    Tuple[Pipeline, Dict[str, float]]
        Fitted pipeline object and metrics dictionary.
    """
    logger.info("Starting model training pipeline...")
    df = load_data(data_filepath)

    X, y, numerical_cols, categorical_cols = prepare_features_and_target(df)

    logger.info("Splitting dataset into train (80%) and test (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    pipeline = build_pipeline(numerical_cols, categorical_cols)

    logger.info("Fitting Scikit-Learn pipeline on training set...")
    try:
        pipeline.fit(X_train, y_train)
        logger.info("Model fitting completed successfully.")
    except Exception as e:
        logger.error(f"Model fitting failed: {str(e)}")
        raise RuntimeError(f"Training failed: {str(e)}") from e

    metrics = evaluate_model(pipeline, X_test, y_test)

    save_pipeline(pipeline)
    save_metrics(metrics)

    return pipeline, metrics
