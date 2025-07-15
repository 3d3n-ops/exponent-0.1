#!/bin/bash

# Production deployment script

echo "🚀 Starting production deployment..."

# 1. Run all tests
echo "�� Running tests..."
pytest tests/ --cov=exponent --cov-report=html

# 2. Check code quality
echo "🔍 Checking code quality..."
black --check exponent/
isort --check-only exponent/
flake8 exponent/
mypy exponent/

# 3. Build package
echo "📦 Building package..."
python -m build

# 4. Check package
echo "✅ Checking package..."
twine check dist/*

# 5. Upload to PyPI (if on main branch)
if [[ "$GITHUB_REF" == "refs/heads/main" ]]; then
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
fi

echo "🎉 Deployment complete!" 