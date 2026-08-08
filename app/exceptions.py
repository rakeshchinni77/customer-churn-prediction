"""
Legacy exceptions module forwarding to app.core.exceptions.
"""

from app.core.exceptions import (
    ModelNotFoundException,
    InvalidInputException,
    ModelNotLoadedError,
    PredictionError,
    register_exception_handlers,
)

__all__ = [
    "ModelNotFoundException",
    "InvalidInputException",
    "ModelNotLoadedError",
    "PredictionError",
    "register_exception_handlers",
]
