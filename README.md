# Exponent-ML

**Prompt + Dataset → Trained + Deployed ML Models in One Line**

Exponent-ML is a CLI tool that lets anyone create, train, and deploy machine learning models by describing their task and uploading a dataset. The tool uses AI agents to generate runnable training pipelines based on both user intent and real dataset structure, with optional deployment to GitHub or cloud platforms.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/exponent-ml.git
cd exponent-ml

# Install dependencies
pip install -r requirements.txt

# Run the setup wizard
exponent setup
```

### First-Time Setup

When you first run Exponent-ML, you'll be guided through a setup wizard:

```bash
# Run the interactive setup wizard
exponent setup
```

The setup wizard will:
1. **Welcome you** to Exponent-ML and explain its capabilities
2. **Configure your AI coding agent** via OpenRouter (supports Claude, GPT-4, CodeLlama, and more)
3. **Test your configuration** to ensure everything works
4. **Explain the commands** and show you how to use the tool
5. **Warn about AI limitations** and best practices

### AI Agent Configuration

Exponent-ML uses OpenRouter to connect you with the best AI coding agents:

**Supported Models:**
- Claude 3.5 Sonnet (Anthropic) - *Recommended*
- GPT-4 Turbo (OpenAI)
- CodeLlama 70B (Meta)
- Claude 3 Haiku (Anthropic)
- Custom models

**Setup Process:**
1. Create a free account at [OpenRouter.ai](https://openrouter.ai)
2. Get your API key from the dashboard
3. Choose your preferred coding agent
4. Test the connection

### Basic Usage

```bash
# Start the interactive wizard (recommended)
exponent

# Run setup if needed
exponent setup

# Check your configuration
exponent status

# Analyze a dataset
exponent analyze data.csv

# Train a model
exponent train

# Deploy to GitHub
exponent deploy
```

## 📋 Commands

### `exponent` (Default Command)

Start the interactive wizard for building ML models:

```bash
exponent
```

This will guide you through:
1. Project description
2. Dataset upload
3. AI-powered code generation
4. Interactive code improvement
5. Cloud training with Modal
6. Deployment to GitHub/AWS

### `exponent setup`

Run the initial setup wizard:

```bash
exponent setup
```

**What it does:**
- Welcome message and tool introduction
- OpenRouter API key configuration
- AI agent selection and testing
- Command overview and best practices
- Warning about AI limitations

### `exponent analyze`

Analyze datasets with AI-powered analysis:

```bash
exponent analyze data.csv
exponent analyze data.csv --prompt "Show customer churn patterns"
exponent analyze data.csv --output my_analysis
```

**Options:**
- `--prompt, -p`: Custom analysis prompt
- `--output, -o`: Output directory for analysis

### `exponent train`

Train ML models with cloud integration:

```bash
exponent train
exponent train --project-id abc123 --dataset data.csv --task "classify"
exponent train --cloud  # Use cloud training
exponent train --status <job_id>  # Check training status
exponent train --list  # List all jobs
```

**Options:**
- `--project-id, -p`: Project ID to train
- `--dataset, -d`: Path to dataset file
- `--task, -t`: Task description
- `--cloud, -c`: Use cloud training (Modal)
- `--status`: Check training job status
- `--list`: List all training jobs

### `exponent deploy`

Deploy projects to GitHub:

```bash
exponent deploy
exponent deploy --project-id abc123
exponent deploy list  # List GitHub repos
```

**Options:**
- `--project-id, -p`: Project ID to deploy
- `--name, -n`: GitHub repository name

### `exponent status`

Check your setup and authentication status:

```bash
exponent status
```

Shows:
- Setup completion status
- OpenRouter configuration
- Authentication status
- Available services

### `exponent init` (Legacy)

Traditional project initialization:

```bash
exponent init quick "make a spam classifier" --dataset spam.csv
exponent init run --task "classify emails" --dataset emails.csv
```

## 🧠 How It Works

1. **AI Agent Setup**: Configure your preferred AI coding agent via OpenRouter
2. **Task Description**: Describe your ML task in natural language
3. **Dataset Analysis**: AI analyzes your dataset structure (columns, types, etc.)
4. **Code Generation**: Your AI agent generates production-ready Python code
5. **Interactive Improvement**: Review and improve the generated code
6. **Cloud Training**: Execute training in Modal's cloud infrastructure
7. **Deployment**: Deploy to GitHub with automated workflows

**No hard-coded templates** - every model is generated specifically for your task and dataset by your chosen AI agent!

## 📁 Generated Project Structure

```
~/.exponent/<project-id>/
├── model.py          # Model definition and training pipeline
├── train.py          # Training script with data loading
├── predict.py        # Prediction script for making predictions
├── requirements.txt  # Python dependencies
├── train_modal.py    # Cloud training script
└── README.md        # Project documentation
```

## 🔧 Configuration

### Required Setup

The only required setup is configuring your AI agent:

1. **OpenRouter Account**: Free account at [OpenRouter.ai](https://openrouter.ai)
2. **API Key**: Get from OpenRouter dashboard
3. **Agent Selection**: Choose your preferred AI model

### Optional Environment Variables

For advanced features, you can set these environment variables:

```bash
# Authentication (OAuth)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Cloud Services (Optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket_name
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
GITHUB_TOKEN=your_github_token
```

## ⚠️ Important Notes

### AI Agent Limitations

- **Review Code**: Always review generated code before running
- **Test Models**: Test your models on sample data first
- **Monitor Training**: Keep an eye on training progress and logs
- **Backup Data**: Keep backups of your datasets
- **Version Control**: Use version control for your projects

### Best Practices

1. **Start Simple**: Begin with small datasets and simple tasks
2. **Iterate**: Use the interactive improvement features
3. **Validate**: Always test your models before deployment
4. **Monitor**: Check training logs and metrics
5. **Secure**: Keep your API keys private and secure

## 🆘 Troubleshooting

### Common Issues

**Setup Problems:**
```bash
# Re-run setup
exponent setup

# Check status
exponent status

# Test configuration
python test_setup.py
```

**Training Issues:**
```bash
# Check training status
exponent train --status <job_id>

# List all jobs
exponent train --list

# Re-run with error handling
exponent train --cloud
```

**Deployment Issues:**
```bash
# Check authentication
exponent status

# Re-authenticate
exponent login --provider github
```

## 🎯 Examples

### Quick Start Examples

```bash
# Complete workflow
exponent                    # Start interactive wizard
exponent analyze data.csv   # Analyze your dataset
exponent train             # Train your model
exponent deploy            # Deploy to GitHub

# Traditional workflow
exponent init quick "make a plant disease classifier" --dataset plant_data.csv
exponent train
exponent deploy
```

### Dataset Analysis

```bash
# Basic analysis
exponent analyze data.csv

# Custom analysis
exponent analyze data.csv --prompt "Show customer churn patterns"

# Save to specific directory
exponent analyze data.csv --output my_analysis
```

### Cloud Training

```bash
# Train with cloud resources
exponent train --cloud

# Check training status
exponent train --status job_12345

# List all training jobs
exponent train --list
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the docs/ folder
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in GitHub Discussions
- **Setup Help**: Run `exponent setup` for guided configuration 