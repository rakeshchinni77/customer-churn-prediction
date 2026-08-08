# Production Backend Dockerfile for FastAPI ML API
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies first for layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application source code and models
COPY app/ ./app/
COPY data/ ./data/
COPY models/ ./models/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY .env .env.example ./

# Expose FastAPI port
EXPOSE 8000

# Run Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
