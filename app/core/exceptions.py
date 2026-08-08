"""
Global Exception Handlers and Custom API Exception Classes.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.logger import logger


class ModelNotFoundException(Exception):
    """Raised when machine learning model artifact file is missing on disk."""
    pass


class InvalidInputException(Exception):
    """Raised when request payload is malformed or invalid."""
    pass


class ModelNotLoadedError(Exception):
    """Raised when machine learning model artifact is not loaded or missing."""
    pass


class PredictionError(Exception):
    """Raised when inference calculation fails."""
    pass


def register_exception_handlers(app):
    """Register custom exception handlers on FastAPI application instance."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error_details = []
        for error in exc.errors():
            loc = " -> ".join(str(l) for l in error.get("loc", []))
            msg = error.get("msg", "")
            error_details.append(f"{loc}: {msg}")

        error_msg = "; ".join(error_details) if error_details else "Invalid input request payload."
        logger.warning(f"Validation error on {request.url.path}: {error_msg}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"success": False, "error": error_msg},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP {exc.status_code} error on {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": str(exc.detail)},
        )

    @app.exception_handler(ModelNotFoundException)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundException):
        logger.error(f"Model not found on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"success": False, "error": f"Model error: {str(exc)}"},
        )

    @app.exception_handler(ModelNotLoadedError)
    async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
        logger.error(f"Model not loaded error on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"success": False, "error": f"Model error: {str(exc)}"},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled server error on {request.url.path}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": f"Internal Server Error: {str(exc)}"},
        )
