# QuickerCleaner Elite Edition - Dockerfile
# Multi-stage build for development and production

# Use Python 3.11 slim image as base
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    build \
    wheel \
    twine

# Copy source code
COPY . .

# Install package in development mode
RUN pip install -e .

# Create non-root user for development
RUN useradd --create-home --shell /bin/bash developer
USER developer

# Set default command
CMD ["python", "-m", "quickercleaner.main", "--help"]

# Production stage
FROM base as production

# Copy source code
COPY . .

# Install package
RUN pip install .

# Create non-root user for production
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Set default command
CMD ["python", "-m", "quickercleaner.main", "--help"]

# Test stage
FROM development as test

# Set test environment
ENV QUICK_CLEANER_TEST_MODE=true \
    QUICK_CLEANER_DRY_RUN=true

# Run tests
CMD ["pytest", "--cov=quickercleaner", "--cov-report=term-missing"]

# Build stage for creating executables
FROM base as build

# Install build tools
RUN pip install --no-cache-dir \
    pyinstaller \
    build \
    wheel

# Copy source code
COPY . .

# Build executable
RUN pyinstaller --onefile --windowed --name QuickerCleaner_Elite quickercleaner/gui.py

# Final stage with executable
FROM python:3.11-slim as executable

# Copy executable from build stage
COPY --from=build /app/dist/QuickerCleaner_Elite /usr/local/bin/

# Set permissions
RUN chmod +x /usr/local/bin/QuickerCleaner_Elite

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Set default command
CMD ["QuickerCleaner_Elite"]

# Windows-specific stage (for reference)
FROM mcr.microsoft.com/windows/servercore:ltsc2019 as windows-base

# This stage is for reference only - Windows containers require different setup
# In practice, Windows executables should be built on Windows hosts

# Alpine stage for minimal footprint
FROM python:3.11-alpine as alpine

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    git

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install package
RUN pip install .

# Create non-root user
RUN adduser -D appuser
USER appuser

# Set default command
CMD ["python", "-m", "quickercleaner.main", "--help"] 