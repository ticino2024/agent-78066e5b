#!/bin/bash

# Script to run tests

echo "Running tests..."

# Run pytest with coverage
pytest tests/ \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    -v

echo "Tests completed!"
echo "Coverage report available in htmlcov/index.html"
