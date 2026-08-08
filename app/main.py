"""
FastAPI Application Entry Point with Lifespan Startup Model Loading,
Custom OpenAPI Documentation, and Global Exception Handlers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logger import logger
from app.predictor import load_model
from app.api.routes import router as api_router
from app.core.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup model loading and shutdown tasks."""
    logger.info("Initializing API application startup...")
    try:
        pipeline = load_model()
        logger.info(f"Model pipeline initialized on startup with {len(pipeline.steps)} pipeline steps.")
    except Exception as e:
        logger.warning(f"Startup model load warning: {str(e)}")
    
    yield
    logger.info("Shutting down API application...")


app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description=(
        "Production-ready RESTful API for predicting customer churn risk in telecommunications. "
        "Built using FastAPI, Scikit-Learn RandomForest Pipeline, Pydantic v2, and Docker."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "System", "description": "API status and health monitoring endpoints"},
        {"name": "Model", "description": "Model metadata and evaluation performance metrics"},
        {"name": "Inference", "description": "Real-time customer churn prediction endpoints"},
    ],
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
register_exception_handlers(app)

# Include API Router
app.include_router(api_router)
