import os
import json
import uuid
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from exponent.core.s3_utils import analyze_dataset, create_local_dataset_summary
from exponent.core.code_gen import generate_code_with_dataset_analysis, extract_code_blocks, save_code_files
from exponent.core.modal_runner import submit_local_training_job, get_training_status
from exponent.core.github_utils import deploy_to_github

class ToolServices:
    """Service class for all agent tool calls."""
    
    def __init__(self):
        self.base_path = Path.home() / '.exponent'
        self.base_path.mkdir(exist_ok=True)
    
    def process_dataset(self, dataset_path: str) -> Dict[str, Any]:
        """Process and analyze a dataset."""
        try:
            # Handle both relative and absolute paths
            dataset_path = Path(dataset_path)
            
            # If it's a relative path, try to resolve it
            if not dataset_path.is_absolute():
                # Try current directory first
                current_dir_path = Path.cwd() / dataset_path
                if current_dir_path.exists():
                    dataset_path = current_dir_path
                else:
                    # Try .exponent directory
                    exponent_path = Path.home() / ".exponent" / dataset_path.name
                    if exponent_path.exists():
                        dataset_path = exponent_path
                    else:
                        # Try searching in .exponent subdirectories
                        exponent_dir = Path.home() / ".exponent"
                        if exponent_dir.exists():
                            for subdir in exponent_dir.iterdir():
                                if subdir.is_dir():
                                    potential_path = subdir / dataset_path.name
                                    if potential_path.exists():
                                        dataset_path = potential_path
                                        break
            
            if not dataset_path.exists():
                return {
                    "success": False,
                    "error": f"Dataset not found: {dataset_path}. Searched in current directory and ~/.exponent"
                }
            
            # Analyze dataset
            dataset_info = analyze_dataset(str(dataset_path))
            summary = create_local_dataset_summary(dataset_info, str(dataset_path))
            
            return {
                "success": True,
                "dataset_info": dataset_info,
                "summary": summary,
                "file_path": str(dataset_path),
                "shape": dataset_info['shape'],
                "columns": dataset_info['columns'],
                "target_column": dataset_info.get('target_column')
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_project(self, project_name: str, description: str = None) -> Dict[str, Any]:
        """Create a new ML project with focused folder structure."""
        try:
            project_id = str(uuid.uuid4())
            project_path = self.base_path / project_id
            project_path.mkdir(exist_ok=True)
            
            # Create focused project structure
            folders = ['data', 'models', 'logs']
            for folder in folders:
                (project_path / folder).mkdir(exist_ok=True)
            
            # Create essential files only
            files_to_create = {
                'README.md': f"""# {project_name}

{description or 'ML project created by Exponent Agent'}

## Project Structure
- `data/` - Dataset files
- `models/` - Trained models
- `logs/` - Training logs and outputs

## Getting Started
1. Place your dataset in the `data/` folder
2. Run training: `python train.py`
3. View visualizations: `python visualize.py`

## Files
- `train.py` - Main training script with real-time logging
- `visualize.py` - Data visualization and EDA
- `model.py` - Model class and preprocessing pipeline
- `requirements.txt` - Python dependencies
""",
                'requirements.txt': """pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.1.0
matplotlib>=3.5.0
seaborn>=0.11.0
joblib>=1.1.0
""",
                '.gitignore': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# Environment
.env
.venv
env/
venv/
ENV/

# ML specific
*.joblib
*.pkl
*.h5
*.pth
logs/
models/
data/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
            }
            
            # Create files
            for filename, content in files_to_create.items():
                file_path = project_path / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return {
                "success": True,
                "project_id": project_id,
                "project_path": str(project_path),
                "project_name": project_name,
                "description": description,
                "folders_created": folders,
                "files_created": list(files_to_create.keys())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_training_code(self, task_description: str, dataset_path: str = None, 
                             project_path: str = None) -> Dict[str, Any]:
        """Generate focused, dataset-specific training code with visualization and logging."""
        try:
            if dataset_path:
                # Generate code with dataset analysis
                project_id, created_files, dataset_info = generate_code_with_dataset_analysis(
                    task_description, dataset_path
                )
                
                # If project_path is provided, move files there
                if project_path:
                    project_path = Path(project_path)
                    project_path.mkdir(exist_ok=True)
                    
                    # Move generated files to project
                    moved_files = []
                    for file_path in created_files:
                        file_path = Path(file_path)
                        if file_path.exists():
                            dest_path = project_path / file_path.name
                            shutil.move(str(file_path), str(dest_path))
                            moved_files.append(str(dest_path))
                    
                    # Also copy dataset to project data folder
                    if dataset_path:
                        dataset_name = Path(dataset_path).name
                        data_folder = project_path / 'data'
                        data_folder.mkdir(exist_ok=True)
                        shutil.copy2(dataset_path, data_folder / dataset_name)
                        moved_files.append(str(data_folder / dataset_name))
                    
                    created_files = moved_files
            else:
                # Generate basic project structure without dataset
                project_id = str(uuid.uuid4())
                out_path = self.base_path / project_id
                out_path.mkdir(exist_ok=True)
                
                # Create minimal training template
                training_code = """import pandas as pd
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
        logger.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
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
        logger.info(f"Encoded categorical column: {col}")
    
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
    logger.info(f"\\nClassification Report:\\n{report}")
    
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
    data_path = "data/dataset.csv"  # Update this path
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
    
    logger.info(f"Target column: {target_col}")
    logger.info(f"Features: {list(X.columns)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train set: {X_train.shape[0]} samples")
    logger.info(f"Test set: {X_test.shape[0]} samples")
    
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
                
                # Save training script
                train_file = out_path / 'train.py'
                with open(train_file, 'w') as f:
                    f.write(training_code)
                
                created_files = [str(train_file)]
            
            return {
                "success": True,
                "project_id": project_id,
                "created_files": created_files,
                "task_description": task_description,
                "dataset_path": dataset_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_training_job(self, project_id: str, dataset_path: str, 
                        task_description: str, model_code: str) -> Dict[str, Any]:
        """Run a training job using Modal."""
        try:
            # Submit training job to Modal
            result = submit_local_training_job(
                project_id=project_id,
                dataset_path=dataset_path,
                task_description=task_description,
                model_code=model_code
            )
            
            return {
                "success": True,
                "job_id": project_id,
                "result": result,
                "status": "submitted"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_training_status(self, job_id: str) -> Dict[str, Any]:
        """Check the status of a training job."""
        try:
            status = get_training_status(job_id)
            return {
                "success": True,
                "job_id": job_id,
                "status": status
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def deploy_model(self, project_path: str, project_name: str = None) -> Dict[str, Any]:
        """Deploy a trained model to GitHub."""
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                return {
                    "success": False,
                    "error": f"Project path does not exist: {project_path}"
                }
            
            # Generate project name if not provided
            if not project_name:
                project_name = f"ml-project-{project_path.name}"
            
            # Deploy to GitHub
            result = deploy_to_github(
                project_id=project_path.name,
                project_path=project_path,
                project_name=project_name
            )
            
            return {
                "success": result.get("deployment_successful", False),
                "project_id": project_path.name,
                "github_url": result.get("github_url"),
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects in the base directory."""
        try:
            projects = []
            for project_dir in self.base_path.iterdir():
                if project_dir.is_dir() and project_dir.name != '__pycache__':
                    # Try to read README for project info
                    readme_path = project_dir / 'README.md'
                    project_info = {
                        "project_id": project_dir.name,
                        "path": str(project_dir),
                        "created_at": datetime.fromtimestamp(project_dir.stat().st_ctime).isoformat()
                    }
                    
                    if readme_path.exists():
                        with open(readme_path, 'r') as f:
                            content = f.read()
                            # Extract project name from first line
                            lines = content.split('\n')
                            if lines and lines[0].startswith('# '):
                                project_info["name"] = lines[0][2:].strip()
                    
                    projects.append(project_info)
            
            return projects
            
        except Exception as e:
            return []
    
    def get_project_info(self, project_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific project."""
        try:
            project_path = self.base_path / project_id
            if not project_path.exists():
                return {
                    "success": False,
                    "error": f"Project not found: {project_id}"
                }
            
            # Get project structure
            files = []
            for file_path in project_path.rglob("*"):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(project_path)))
            
            # Check for model files
            model_files = [f for f in files if f.endswith(('.joblib', '.pkl', '.h5'))]
            data_files = [f for f in files if f.endswith(('.csv', '.json', '.parquet'))]
            
            return {
                "success": True,
                "project_id": project_id,
                "path": str(project_path),
                "files": files,
                "model_files": model_files,
                "data_files": data_files,
                "created_at": datetime.fromtimestamp(project_path.stat().st_ctime).isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 