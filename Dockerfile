# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # HuggingFace model cache directory
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    HF_HOME=/app/.cache/huggingface \
    # Default port
    PORT=8080 \
    # Use China mirror for acceleration (optional)
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/.cache/huggingface

# Create non-root user (optional, Railway may need root)
# RUN useradd -m -u 1000 appuser && \
#     chown -R appuser:appuser /app
# USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start command - directly use port 8080
CMD uvicorn api:app --host 0.0.0.0 --port 8080
