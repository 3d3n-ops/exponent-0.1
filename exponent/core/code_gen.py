import anthropic
import requests
import uuid
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from exponent.core.config import get_config
from exponent.core.s3_utils import analyze_dataset, create_dataset_summary

def make_ai_request(prompt: str, model: str = None) -> str:
    """Make AI request using either OpenRouter or Anthropic based on configuration."""
    config = get_config()
    
    # Use OpenRouter if configured
    if config.OPENROUTER_API_KEY and config.AGENT_MODEL:
        return make_openrouter_request(prompt, config.AGENT_MODEL, config.OPENROUTER_API_KEY)
    else:
        # Fall back to Anthropic
        return make_anthropic_request(prompt, config.ANTHROPIC_API_KEY)

def make_openrouter_request(prompt: str, model: str, api_key: str) -> str:
    """Make request to OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,  # Reduced from 4000 to stay within credit limit
        "temperature": 0.7
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

def make_anthropic_request(prompt: str, api_key: str) -> str:
    """Make request to Anthropic API."""
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,  # Reduced from 4000 to stay within credit limit
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def extract_code_blocks(content: str) -> Dict[str, str]:
    """Extract code blocks from markdown content."""
    code_blocks = {}
    
    # Pattern to match markdown code blocks with language labels
    pattern = r'```(\w+)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for lang, code in matches:
        # Clean up the code
        code = code.strip()
        if code:
            code_blocks[lang] = code
    
    # Also look for unlabeled code blocks
    unlabeled_pattern = r'```\n(.*?)```'
    unlabeled_matches = re.findall(unlabeled_pattern, content, re.DOTALL)
    
    for i, code in enumerate(unlabeled_matches):
        code = code.strip()
        if code:
            # Try to infer file type from content
            if 'import pandas' in code or 'pd.read_csv' in code:
                code_blocks[f'python_{i}'] = code
            elif 'def train' in code or 'model.fit' in code:
                code_blocks[f'train_{i}'] = code
            else:
                code_blocks[f'code_{i}'] = code
    
    return code_blocks

def save_code_files(code_blocks: Dict[str, str], output_path: Path) -> List[str]:
    """Save code blocks to files and return list of created files."""
    created_files = []
    
    # Map language labels to filenames
    file_mapping = {
        'python': 'train.py',
        'train': 'train.py',
        'visualize': 'visualize.py',
        'model': 'model.py',
        'requirements': 'requirements.txt',
        'txt': 'requirements.txt'
    }
    
    for lang, code in code_blocks.items():
        # Determine filename
        if lang in file_mapping:
            filename = file_mapping[lang]
        elif lang.startswith('python'):
            filename = 'train.py'
        elif lang.startswith('train'):
            filename = 'train.py'
        elif lang.startswith('visualize'):
            filename = 'visualize.py'
        elif lang.startswith('model'):
            filename = 'model.py'
        elif lang.startswith('requirements'):
            filename = 'requirements.txt'
        else:
            # Skip non-essential files
            continue
        
        # Save file
        file_path = output_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        created_files.append(str(file_path))
    
    return created_files

def generate_code_from_prompt(task_description: str, dataset_path: str = None) -> Tuple[str, List[str]]:
    """Generate ML code from prompt and optional dataset."""
    config = get_config()
    project_id = str(uuid.uuid4())
    out_path = Path.home() / ".exponent" / project_id
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Analyze dataset if provided
    dataset_summary = ""
    if dataset_path:
        try:
            dataset_info = analyze_dataset(dataset_path)
            dataset_summary = create_local_dataset_summary(dataset_info, dataset_path)
        except Exception as e:
            print(f"Warning: Could not analyze dataset: {e}")
    
    # Create comprehensive prompt
    full_prompt = f"""
You are an expert ML engineer. Generate production-ready Python code for the following machine learning task:

**Task**: {task_description}

{dataset_summary}

**Requirements:**
1. Generate clean, well-documented Python code
2. Include proper error handling and logging
3. Use modern ML libraries (scikit-learn, pandas, numpy)
4. Include data preprocessing and feature engineering
5. Add model evaluation metrics
6. Make code modular and reusable
7. Use local file paths for data loading (no cloud dependencies)

**Generate these files:**
1. `model.py` - Model definition and training pipeline
2. `train.py` - Training script with data loading and model training
3. `predict.py` - Prediction script for making predictions
4. `requirements.txt` - Python dependencies
5. `README.md` - Project documentation

Respond with markdown code blocks labeled with the filename (e.g., ```python for model.py, ```train for train.py, etc.).
"""

    # Call AI API (OpenRouter or Anthropic)
    content = make_ai_request(full_prompt)
    
    # Extract and save code blocks
    code_blocks = extract_code_blocks(content)
    created_files = save_code_files(code_blocks, out_path)
    
    # Copy dataset to project directory if provided
    if dataset_path:
        try:
            import shutil
            dataset_name = Path(dataset_path).name
            shutil.copy2(dataset_path, out_path / dataset_name)
            created_files.append(str(out_path / dataset_name))
        except Exception as e:
            print(f"Warning: Could not copy dataset to project directory: {e}")
    
    return project_id, created_files

def generate_code_with_dataset_analysis(task_description: str, dataset_path: str) -> Tuple[str, List[str], Dict[str, Any]]:
    """Generate focused, dataset-specific training code with visualization and logging."""
    config = get_config()
    project_id = str(uuid.uuid4())
    out_path = Path.home() / ".exponent" / project_id
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Analyze dataset
    dataset_info = analyze_dataset(dataset_path)
    dataset_name = Path(dataset_path).name
    
    # Create focused prompt for better code generation
    full_prompt = f"""
You are an expert ML engineer. Generate focused, production-ready Python code for this specific task and dataset.

**Task**: {task_description}
**Dataset**: {dataset_name}

**Dataset Analysis:**
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- Target column: {dataset_info.get('target_column', 'Last column')}
- File size: {dataset_info['file_size']} bytes

**Column Analysis:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        full_prompt += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            full_prompt += f"  Sample values: {col_info['sample_values']}\n"
    
    full_prompt += f"""

**Requirements:**
1. Generate ONLY these 4 essential files (no extra files):
   - `train.py` - Complete training script with real-time logging
   - `visualize.py` - Data visualization and EDA script
   - `model.py` - Model class and preprocessing pipeline
   - `requirements.txt` - Only necessary dependencies

2. Make the code dataset-specific:
   - Use the actual column names from the dataset
   - Handle the specific data types and null values
   - Target the correct target column
   - Use relative paths (dataset is in same directory)

3. Include real-time logging:
   - Log training progress with timestamps
   - Log model performance metrics
   - Log data preprocessing steps
   - Use proper logging levels (INFO, WARNING, ERROR)

4. Add comprehensive data visualization:
   - Distribution plots for all features
   - Correlation heatmap
   - Target variable analysis
   - Missing value visualization
   - Feature importance plots

5. Make code production-ready:
   - Proper error handling
   - Input validation
   - Modular design
   - Clear documentation

**Generate ONLY these files with proper code blocks:**

1. `train.py` - Main training script
2. `visualize.py` - Data visualization script  
3. `model.py` - Model class
4. `requirements.txt` - Dependencies

Use this exact format for each file:
```python
# train.py content here
```

```python
# visualize.py content here
```

```python
# model.py content here
```

```txt
# requirements.txt content here
```

Focus on creating clean, focused code that works specifically with this dataset.
"""

    # Call AI API
    content = make_ai_request(full_prompt)
    
    # Extract and save only the essential code blocks
    code_blocks = extract_code_blocks(content)
    
    # Debug: Print what was extracted
    print(f"Extracted code blocks: {list(code_blocks.keys())}")
    
    # Filter to only essential files
    essential_files = ['train.py', 'visualize.py', 'model.py', 'requirements.txt']
    filtered_blocks = {}
    
    for filename, code in code_blocks.items():
        # Clean up filename
        clean_filename = filename.lower().replace(' ', '_').replace('-', '_')
        if clean_filename in essential_files or any(essential in clean_filename for essential in essential_files):
            filtered_blocks[clean_filename] = code
            print(f"Keeping file: {clean_filename} (original: {filename})")
        else:
            print(f"Skipping file: {filename}")
    
    # If no essential files were found, create a basic training script
    if not filtered_blocks:
        print("No essential files found, creating basic training script...")
        filtered_blocks['train.py'] = f"""import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_data(data_path):
    \"\"\"Load dataset from path.\"\"\"
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Dataset loaded: {{df.shape[0]}} rows, {{df.shape[1]}} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {{e}}")
        return None

def preprocess_data(df):
    \"\"\"Preprocess the dataset.\"\"\"
    logger.info("Starting data preprocessing...")
    
    # Handle missing values
    df = df.fillna(df.median())
    logger.info("Handled missing values")
    
    # Convert categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = pd.Categorical(df[col]).codes
        logger.info(f"Encoded categorical column: {{col}}")
    
    return df

def train_model(X_train, y_train):
    \"\"\"Train the model.\"\"\"
    logger.info("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logger.info("Model training completed")
    return model

def evaluate_model(model, X_test, y_test):
    \"\"\"Evaluate the model.\"\"\"
    logger.info("Evaluating model...")
    y_pred = model.predict(X_test)
    
    # Print classification report
    report = classification_report(y_test, y_pred)
    logger.info(f"\\nClassification Report:\\n{{report}}")
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
    plt.title('Confusion Matrix')
    plt.savefig('logs/confusion_matrix.png')
    plt.close()
    logger.info("Confusion matrix saved to logs/confusion_matrix.png")

def main():
    \"\"\"Main training function.\"\"\"
    logger.info("Starting ML training pipeline...")
    
    # Load data
    data_path = "{dataset_name}"  # Dataset in same directory
    df = load_data(data_path)
    
    if df is None:
        logger.error("Failed to load data")
        return
    
    # Preprocess data
    df = preprocess_data(df)
    
    # Split features and target
    target_col = df.columns[-1]  # Assuming last column is target
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    logger.info(f"Target column: {{target_col}}")
    logger.info(f"Features: {{list(X.columns)}}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train set: {{X_train.shape[0]}} samples")
    logger.info(f"Test set: {{X_test.shape[0]}} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    logger.info("Features scaled")
    
    # Train model
    model = train_model(X_train_scaled, y_train)
    
    # Evaluate model
    evaluate_model(model, X_test_scaled, y_test)
    
    # Save model and scaler
    joblib.dump(model, 'models/model.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    logger.info("Model and scaler saved to models/")

if __name__ == "__main__":
    main()
"""
        
        filtered_blocks['visualize.py'] = f"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(data_path):
    \"\"\"Load dataset from path.\"\"\"
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Dataset loaded: {{df.shape[0]}} rows, {{df.shape[1]}} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {{e}}")
        return None

def create_visualizations(df):
    \"\"\"Create comprehensive data visualizations.\"\"\"
    logger.info("Creating data visualizations...")
    
    # Create output directory
    import os
    os.makedirs('logs', exist_ok=True)
    
    # 1. Distribution plots for all features
    plt.figure(figsize=(15, 10))
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for i, col in enumerate(numeric_cols[:9]):  # Limit to 9 plots
        plt.subplot(3, 3, i+1)
        df[col].hist(bins=30)
        plt.title(f'Distribution of {{col}}')
        plt.xlabel(col)
    plt.tight_layout()
    plt.savefig('logs/feature_distributions.png')
    plt.close()
    logger.info("Feature distributions saved")
    
    # 2. Correlation heatmap
    plt.figure(figsize=(12, 8))
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('logs/correlation_heatmap.png')
    plt.close()
    logger.info("Correlation heatmap saved")
    
    # 3. Target variable analysis
    target_col = df.columns[-1]
    plt.figure(figsize=(10, 6))
    df[target_col].value_counts().plot(kind='bar')
    plt.title(f'Target Variable Distribution: {{target_col}}')
    plt.xlabel(target_col)
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('logs/target_distribution.png')
    plt.close()
    logger.info("Target distribution saved")
    
    # 4. Missing value visualization
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        plt.figure(figsize=(10, 6))
        missing_data.plot(kind='bar')
        plt.title('Missing Values by Column')
        plt.xlabel('Columns')
        plt.ylabel('Missing Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('logs/missing_values.png')
        plt.close()
        logger.info("Missing values plot saved")
    
    logger.info("All visualizations completed!")

def main():
    \"\"\"Main visualization function.\"\"\"
    logger.info("Starting data visualization...")
    
    # Load data
    data_path = "{dataset_name}"
    df = load_data(data_path)
    
    if df is None:
        logger.error("Failed to load data")
        return
    
    # Create visualizations
    create_visualizations(df)
    logger.info("Visualization complete! Check the logs/ directory for plots.")

if __name__ == "__main__":
    main()
"""
        
        filtered_blocks['requirements.txt'] = """pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.1.0
matplotlib>=3.5.0
seaborn>=0.11.0
joblib>=1.1.0
"""
    
    # Save only essential files
    created_files = save_code_files(filtered_blocks, out_path)
    print(f"Created files: {created_files}")
    
    # Copy dataset to project directory
    try:
        import shutil
        dataset_name = Path(dataset_path).name
        shutil.copy2(dataset_path, out_path / dataset_name)
        created_files.append(str(out_path / dataset_name))
        print(f"Copied dataset: {dataset_name}")
    except Exception as e:
        print(f"Warning: Could not copy dataset to project directory: {e}")
    
    return project_id, created_files, dataset_info

def create_local_dataset_summary(dataset_info: Dict[str, Any], dataset_path: str) -> str:
    """Create a formatted summary of the dataset for local usage."""
    summary = f"""
**Dataset Information:**
- File: {dataset_info['file_path']}
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- Local path: {dataset_path}

**Columns:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        summary += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            summary += f"  Sample values: {col_info['sample_values']}\n"
    
    return summary
