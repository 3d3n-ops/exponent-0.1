# Exponent-ML Documentation

**Build ML models from the CLI using LLMs and Modal**

Exponent-ML is a powerful command-line tool that enables anyone to create, train, and deploy machine learning models by simply describing their task and uploading a dataset. The tool uses Large Language Models (LLMs) to generate production-ready Python code based on your specific requirements and dataset structure.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication)
4. [Core Commands](#core-commands)
5. [Advanced Usage](#advanced-usage)
6. [Configuration](#configuration)
7. [FAQ](#faq)
8. [Troubleshooting](#troubleshooting)
9. [Examples](#examples)

## Installation

### From PyPI (Recommended)
```bash
pip install exponent-ml
```

### From Source
```bash
git clone https://github.com/yourusername/exponent-ml.git
cd exponent-ml
pip install -e .
```

### Verify Installation
```bash
exponent --help
```

## Quick Start

### 1. Set Up Environment Variables
Create a `.env` file in your project directory:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Authentication (OAuth)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Optional (for cloud features)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket_name
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
GITHUB_TOKEN=your_github_token
```

### 2. Authenticate
```bash
# Login with Google OAuth
exponent login --provider google

# Or login with GitHub OAuth
exponent login --provider github
```

### 3. Create Your First Model
```bash
# Quick start with a spam classifier
exponent init quick "Create a spam email classifier" --dataset emails.csv

# Train the model
exponent train

# Deploy to GitHub
exponent deploy
```

## Authentication

Exponent-ML supports OAuth authentication with Google and GitHub.

### Setting Up OAuth Credentials

#### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Set redirect URI to `http://localhost:8080`
6. Add credentials to your `.env` file

#### GitHub OAuth Setup
1. Go to [GitHub OAuth Apps](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set callback URL to `http://localhost:8080`
4. Add credentials to your `.env` file

### Authentication Commands
```bash
# Login with specific provider
exponent login --provider google
exponent login --provider github

# Check authentication status
exponent status

# Logout
exponent logout
```

## Core Commands

### `exponent init` - Initialize ML Projects

Creates a new ML project with interactive wizard or quick setup.

#### Interactive Mode
```bash
exponent init
```
Follow the prompts to:
- Describe your ML task
- Upload your dataset
- Configure training parameters

#### Quick Mode
```bash
exponent init quick "Predict customer churn" --dataset customers.csv
```

#### Options
- `--task, -t`: ML task description
- `--dataset, -d`: Path to dataset file
- `--interactive, -i`: Run in interactive mode (default: True)

### `exponent train` - Train ML Models

Trains models locally or in the cloud using Modal.

#### Basic Training
```bash
# Train in current directory
exponent train

# Train with specific project
exponent train --project-id my-project --dataset data.csv --task "classify images"
```

#### Cloud Training
```bash
# Use cloud training with Modal
exponent train --cloud

# Upload dataset to S3 for cloud training
exponent train --cloud --s3
```

#### Training Status
```bash
# Check training job status
exponent train --status job_12345

# List all training jobs
exponent train --list
```

#### Options
- `--project-id, -p`: Project ID to train
- `--dataset, -d`: Path to dataset file
- `--task, -t`: Task description
- `--cloud, -c`: Use cloud training (Modal)
- `--s3`: Upload dataset to S3 for cloud training

### `exponent analyze` - Dataset Analysis

Analyze datasets with AI-powered analysis and visualization.

```bash
# Basic analysis
exponent analyze data.csv

# Custom analysis prompt
exponent analyze data.csv --prompt "Show customer churn patterns and feature importance"

# Save analysis to specific directory
exponent analyze data.csv --output my_analysis
```

#### Options
- `--prompt, -p`: Analysis prompt for AI
- `--output, -o`: Output directory for analysis

### `exponent deploy` - Deploy to GitHub

Deploy projects to GitHub with automated workflows.

```bash
# Deploy current project
exponent deploy

# Deploy specific project
exponent deploy --project-id my-project

# Deploy with custom repository name
exponent deploy --name my-awesome-model
```

#### Options
- `--project-id, -p`: Project ID to deploy
- `--name, -n`: GitHub repository name
- `--path`: Path to project directory

### `exponent interactive` - Interactive Wizard

Complete ML pipeline with guided workflow.

```bash
# Start interactive wizard
exponent interactive wizard
```

Follow the wizard to:
1. Describe your ML task
2. Upload and analyze your dataset
3. Configure model parameters
4. Train the model
5. Deploy to GitHub

## Advanced Usage

### Custom Training Pipelines

Exponent-ML generates custom training code based on your task and dataset. The generated code includes:

- **Data preprocessing**: Automatic handling of missing values, encoding, scaling
- **Model selection**: Best model for your task and data type
- **Hyperparameter tuning**: Automatic optimization
- **Evaluation metrics**: Task-appropriate metrics
- **Model persistence**: Save/load trained models

### Cloud Training with Modal

For large datasets or complex models, use cloud training:

```bash
# Train in cloud with S3 dataset
exponent train --cloud --s3 --dataset large_dataset.csv

# Monitor cloud training
exponent train --status <job_id>
```

### Custom Analysis Prompts

Use custom prompts for dataset analysis:

```bash
# Analyze customer behavior
exponent analyze customers.csv --prompt "Identify customer segments and predict lifetime value"

# Analyze time series data
exponent analyze sales.csv --prompt "Detect seasonal patterns and forecast future sales"

# Analyze text data
exponent analyze reviews.csv --prompt "Perform sentiment analysis and extract key topics"
```

## Configuration

### Environment Variables

#### Required
- `ANTHROPIC_API_KEY`: Your Anthropic API key for code generation

#### Authentication
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `GITHUB_CLIENT_ID`: GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET`: GitHub OAuth client secret

#### Cloud Features (Optional)
- `AWS_ACCESS_KEY_ID`: AWS access key for S3 uploads
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for S3 uploads
- `AWS_REGION`: AWS region (default: us-east-1)
- `S3_BUCKET`: S3 bucket name for dataset storage
- `MODAL_TOKEN_ID`: Modal token for cloud training
- `MODAL_TOKEN_SECRET`: Modal token secret for cloud training
- `GITHUB_TOKEN`: GitHub token for repository creation

### Project Structure

Generated projects follow this structure:
```
~/.exponent/<project-id>/
├── model.py          # Model definition and training pipeline
├── train.py          # Training script with data loading
├── predict.py        # Prediction script for making predictions
├── requirements.txt  # Python dependencies
└── README.md        # Project documentation
```

## FAQ

### General Questions

**Q: What types of ML tasks does Exponent-ML support?**
A: Exponent-ML supports a wide range of tasks including:
- Classification (binary and multi-class)
- Regression
- Time series forecasting
- Text classification and sentiment analysis
- Image classification
- Anomaly detection

**Q: What file formats are supported for datasets?**
A: Exponent-ML supports:
- CSV files (.csv)
- Excel files (.xlsx, .xls)
- JSON files (.json)
- Parquet files (.parquet)

**Q: How does Exponent-ML choose the best model for my task?**
A: The tool analyzes your dataset structure (column types, missing values, target variable) and task description to select the most appropriate algorithm. It considers factors like data size, feature types, and performance requirements.

**Q: Can I use my own custom models?**
A: Currently, Exponent-ML generates models automatically. However, you can modify the generated code in the project directory to use custom models or add additional preprocessing steps.

### Authentication

**Q: Why do I need to authenticate?**
A: Authentication is required to:
- Track your projects and training jobs
- Deploy models to GitHub
- Use cloud training features
- Access advanced features

**Q: Can I use Exponent-ML without OAuth?**
A: Basic features work without authentication, but you'll need OAuth for cloud training, GitHub deployment, and project management.

**Q: How do I change my authentication provider?**
A: Use `exponent logout` to clear current credentials, then `exponent login --provider <new_provider>` to authenticate with a different provider.

### Training and Deployment

**Q: How long does training take?**
A: Training time depends on:
- Dataset size and complexity
- Model type and hyperparameters
- Hardware (local vs cloud)
- Typically 5-30 minutes for most datasets

**Q: Can I stop training early?**
A: Yes, you can interrupt training with Ctrl+C. The model will be saved at the current checkpoint.

**Q: How do I monitor training progress?**
A: Use `exponent train --status <job_id>` to check training status and view metrics.

**Q: What happens if training fails?**
A: The tool will show error messages and suggestions. Common issues include:
- Insufficient memory
- Invalid data format
- Missing dependencies
- Network issues (for cloud training)

**Q: Can I deploy to platforms other than GitHub?**
A: Currently, GitHub deployment is supported. Future versions may include other platforms like AWS, Google Cloud, or Azure.

### Data and Analysis

**Q: How does Exponent-ML handle missing values?**
A: The tool automatically detects and handles missing values using appropriate strategies:
- Numerical data: Mean/median imputation
- Categorical data: Mode imputation
- Advanced: KNN imputation for complex cases

**Q: What if my dataset is too large for local training?**
A: Use cloud training with `exponent train --cloud`. The tool will upload your dataset to S3 and train in Modal's cloud infrastructure.

**Q: Can I analyze datasets without training a model?**
A: Yes! Use `exponent analyze data.csv` to get insights about your dataset without training.

**Q: How accurate are the generated models?**
A: Model accuracy depends on your data quality and task complexity. The tool uses cross-validation and multiple algorithms to find the best model for your specific case.

## Troubleshooting

### Common Issues

**Authentication Problems**
```bash
# Error: "No OAuth providers configured"
# Solution: Set up OAuth credentials in .env file
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

**Training Failures**
```bash
# Error: "Out of memory"
# Solution: Use cloud training
exponent train --cloud

# Error: "Invalid data format"
# Solution: Check your CSV file format
# Ensure proper headers and data types
```

**Deployment Issues**
```bash
# Error: "GitHub repository already exists"
# Solution: Use different repository name
exponent deploy --name unique-repo-name
```

**API Key Issues**
```bash
# Error: "Invalid API key"
# Solution: Check your Anthropic API key
# Ensure it's valid and has sufficient credits
```

### Getting Help

1. **Check the logs**: Look for error messages in the terminal output
2. **Verify configuration**: Ensure all environment variables are set correctly
3. **Test with sample data**: Try with a small, clean dataset first
4. **Check dependencies**: Ensure all required packages are installed

## Examples

### Example 1: Customer Churn Prediction

```bash
# 1. Prepare your dataset (customers.csv with features and 'churn' target)
# 2. Initialize project
exponent init quick "Predict customer churn" --dataset customers.csv

# 3. Train model
exponent train

# 4. Deploy to GitHub
exponent deploy --name customer-churn-predictor
```

### Example 2: Image Classification

```bash
# 1. Prepare image dataset with labels
# 2. Initialize project
exponent init quick "Classify plant diseases from images" --dataset plant_images.csv

# 3. Train with cloud resources
exponent train --cloud

# 4. Deploy
exponent deploy --name plant-disease-classifier
```

### Example 3: Time Series Forecasting

```bash
# 1. Prepare time series data
# 2. Initialize project
exponent init quick "Forecast sales for next 30 days" --dataset sales_data.csv

# 3. Train model
exponent train

# 4. Deploy
exponent deploy --name sales-forecaster
```

### Example 4: Text Sentiment Analysis

```bash
# 1. Prepare text dataset with sentiment labels
# 2. Initialize project
exponent init quick "Analyze sentiment of customer reviews" --dataset reviews.csv

# 3. Train model
exponent train

# 4. Deploy
exponent deploy --name sentiment-analyzer
```

### Example 5: Interactive Workflow

```bash
# Start interactive wizard
exponent interactive wizard

# Follow the prompts:
# 1. Describe your task: "Create a model to predict house prices"
# 2. Upload dataset: house_data.csv
# 3. Review analysis and confirm
# 4. Train model
# 5. Deploy to GitHub
```

### Example 6: Dataset Analysis Only

```bash
# Analyze dataset without training
exponent analyze customer_data.csv --prompt "Show customer segmentation and key insights"

# Save analysis to specific directory
exponent analyze sales_data.csv --output sales_analysis --prompt "Identify seasonal patterns and trends"
```

## Support and Community

- **GitHub Issues**: Report bugs and request features
- **Documentation**: This file and README.md
- **Examples**: Check the `examples/` directory for sample projects
- **Community**: Join our Discord/Slack for discussions

## Version History

- **v0.1.0**: Initial release with CLI interface, authentication, dataset analysis, model training, and GitHub deployment

---

**Happy ML modeling with Exponent-ML! 🚀** 