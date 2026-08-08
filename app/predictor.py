"""
Standalone Inference Predictor Module for Customer Churn Prediction.
Encapsulates model loading, feature DataFrame conversion, single-sample prediction,
and churn probability extraction.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from app.config import settings
from app.logger import logger
from app.exceptions import ModelNotFoundException, InvalidInputException

# Global cached model instance
_model_instance: Optional[Pipeline] = None


def load_model(model_path: Optional[Union[str, Path]] = None) -> Pipeline:
    """
    Load the trained Scikit-Learn model pipeline from disk using Joblib.
    Caches the loaded pipeline instance globally to avoid redundant disk reads.

    Parameters
    ----------
    model_path : Optional[Union[str, Path]], optional
        Filepath to the saved pipeline artifact. Defaults to settings.MODEL_PATH.

    Returns
    -------
    Pipeline
        Loaded Scikit-Learn pipeline instance.

    Raises
    ------
    ModelNotFoundException
        If the model artifact file does not exist on disk.
    RuntimeError
        If the model artifact cannot be deserialized.
    """
    global _model_instance

    if _model_instance is not None and model_path is None:
        return _model_instance

    path = Path(model_path) if model_path else Path(settings.MODEL_PATH)
    logger.info(f"Loading model pipeline from: {path}")

    if not path.exists():
        error_msg = f"Model pipeline artifact not found at path: {path}"
        logger.error(error_msg)
        raise ModelNotFoundException(error_msg)

    try:
        pipeline = joblib.load(path)
        if not hasattr(pipeline, "predict") or not hasattr(pipeline, "predict_proba"):
            raise ValueError("Loaded object is not a valid Scikit-Learn prediction pipeline.")

        logger.info("Model pipeline loaded successfully.")
        if model_path is None:
            _model_instance = pipeline
        return pipeline
    except Exception as e:
        error_msg = f"Failed to load model pipeline artifact: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


def _convert_dict_to_dataframe(customer_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert a customer data dictionary into a single-row Pandas DataFrame.

    Parameters
    ----------
    customer_data : Dict[str, Any]
        Dictionary of customer feature attributes.

    Returns
    -------
    pd.DataFrame
        One-row DataFrame ready for pipeline inference.

    Raises
    ------
    InvalidInputException
        If customer_data is empty or not a valid dictionary.
    """
    if not isinstance(customer_data, dict) or not customer_data:
        raise InvalidInputException("Customer data must be a non-empty dictionary.")

    try:
        df = pd.DataFrame([customer_data])
        # Clean numeric fields if necessary
        if "TotalCharges" in df.columns:
            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"].astype(str).str.strip(), errors="coerce"
            )
        return df
    except Exception as e:
        raise InvalidInputException(f"Failed to create DataFrame from input data: {str(e)}") from e


def predict(
    customer_data: Dict[str, Any], model: Optional[Pipeline] = None
) -> str:
    """
    Predict customer churn status ("Yes" or "No") for a single customer record.

    Parameters
    ----------
    customer_data : Dict[str, Any]
        Dictionary containing customer feature attributes.
    model : Optional[Pipeline], optional
        Optional pre-loaded pipeline instance. If None, uses load_model().

    Returns
    -------
    str
        "Yes" if predicted to churn, "No" otherwise.
    """
    pipeline = model if model is not None else load_model()
    df = _convert_dict_to_dataframe(customer_data)

    try:
        raw_pred = pipeline.predict(df)[0]
        prediction_label = "Yes" if raw_pred == 1 else "No"
        logger.info(f"Inference completed. Output label: '{prediction_label}'")
        return prediction_label
    except Exception as e:
        logger.error(f"Prediction execution failed: {str(e)}")
        raise RuntimeError(f"Prediction failed: {str(e)}") from e


def predict_proba(
    customer_data: Dict[str, Any], model: Optional[Pipeline] = None
) -> float:
    """
    Calculate positive-class churn probability for a single customer record.

    Parameters
    ----------
    customer_data : Dict[str, Any]
        Dictionary containing customer feature attributes.
    model : Optional[Pipeline], optional
        Optional pre-loaded pipeline instance. If None, uses load_model().

    Returns
    -------
    float
        Churn probability as a float between 0.0 and 1.0 (rounded to 4 decimals).
    """
    pipeline = model if model is not None else load_model()
    df = _convert_dict_to_dataframe(customer_data)

    try:
        probabilities = pipeline.predict_proba(df)
        churn_prob = float(round(probabilities[0][1], 4))
        logger.info(f"Inference completed. Calculated churn probability: {churn_prob}")
        return churn_prob
    except Exception as e:
        logger.error(f"Probability calculation failed: {str(e)}")
        raise RuntimeError(f"Probability prediction failed: {str(e)}") from e
