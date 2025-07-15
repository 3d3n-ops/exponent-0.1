#!/bin/bash

echo "🔧 Setting up Exponent-ML development environment..."

# Install pre-commit hooks
pre-commit install

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (for cloud features)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket_name_here
MODAL_TOKEN_ID=your_modal_token_id_here
MODAL_TOKEN_SECRET=your_modal_token_secret_here
GITHUB_TOKEN=your_github_token_here

# Authentication
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here
CLERK_SECRET_KEY=your_clerk_secret_key_here
EOF
    echo "⚠️  Please edit .env file with your actual API keys"
fi

echo "✅ Setup complete! Run 'source .venv/bin/activate' to activate the environment" 