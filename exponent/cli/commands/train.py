import typer
import time
from pathlib import Path
from exponent.api.client import ExponentAPIClient

app = typer.Typer()

def load_model_code(project_id: str) -> str:
    """Load the generated model code from the project directory."""
    # Try to find project in ~/.exponent
    home_dir = Path.home() / ".exponent" / project_id
    if home_dir.exists():
        # Look for model.py or train.py
        model_file = home_dir / "model.py"
        train_file = home_dir / "train.py"
        
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                return f.read()
        elif train_file.exists():
            with open(train_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"No model.py or train.py found in project {project_id}")
    else:
        # Try current directory
        current_dir = Path.cwd()
        model_file = current_dir / "model.py"
        train_file = current_dir / "train.py"
        
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                return f.read()
        elif train_file.exists():
            with open(train_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError("No model.py or train.py found in current directory")

@app.command()
def run(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to train"),
    dataset_path: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    task_description: str = typer.Option(None, "--task", "-t", help="Task description"),
    model_type: str = typer.Option("sentiment_analysis", "--model-type", "-m", help="Type of model to train"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for job completion")
):
    """Train an ML model using the Exponent API backend."""
    
    # Initialize API client
    client = ExponentAPIClient(api_url)
    
    # Check API health
    try:
        health = client.health_check()
        typer.echo("✅ API server is healthy")
    except Exception as e:
        typer.echo(f"❌ API server is not available: {e}")
        typer.echo("💡 Make sure the API server is running with: python -m exponent.api.server")
        raise typer.Exit(1)
    
    if not project_id:
        typer.echo("❌ Project ID is required")
        typer.echo("💡 Use 'exponent init' to create a new project first")
        raise typer.Exit(1)
    
    if not dataset_path:
        typer.echo("❌ Dataset path is required")
        raise typer.Exit(1)
    
    # Create training job
    try:
        typer.echo(f"🚀 Creating training job for project: {project_id}")
        typer.echo(f"📊 Dataset: {dataset_path}")
        typer.echo(f"🤖 Model type: {model_type}")
        
        response = client.create_training_job(
            project_id=project_id,
            dataset_path=dataset_path,
            model_type=model_type
        )
        
        if response.get('success'):
            job = response.get('job', {})
            job_id = job.get('job_id')
            typer.echo(f"✅ Training job created successfully!")
            typer.echo(f"📋 Job ID: {job_id}")
            typer.echo(f"📊 Status: {job.get('status')}")
            
            if wait:
                typer.echo("⏳ Waiting for job completion...")
                final_response = client.wait_for_job_completion(job_id)
                final_job = final_response.get('job', {})
                
                if final_job.get('status') == 'completed':
                    typer.echo("✅ Training completed successfully!")
                    metrics = final_job.get('metrics', {})
                    if metrics:
                        typer.echo("📊 Training Metrics:")
                        for metric, value in metrics.items():
                            typer.echo(f"  - {metric}: {value}")
                else:
                    typer.echo(f"❌ Training failed: {final_job.get('error_message')}")
                    raise typer.Exit(1)
            else:
                typer.echo("💡 Use 'exponent train status <job_id>' to check progress")
                
        else:
            typer.echo(f"❌ Failed to create training job: {response.get('error')}")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error creating training job: {e}")
        raise typer.Exit(1)

@app.command()
def status(
    job_id: str = typer.Argument(..., help="Training job ID"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """Check status of a training job."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.get_training_job(job_id)
        if response.get('success'):
            job = response.get('job', {})
            typer.echo(f"📊 Job Status: {job.get('status')}")
            typer.echo(f"📋 Job ID: {job.get('job_id')}")
            typer.echo(f"📁 Project: {job.get('project_id')}")
            typer.echo(f"📊 Dataset: {job.get('dataset_path')}")
            typer.echo(f"🤖 Model Type: {job.get('model_type')}")
            
            if job.get('metrics'):
                typer.echo("📈 Metrics:")
                for metric, value in job.get('metrics', {}).items():
                    typer.echo(f"  - {metric}: {value}")
            
            if job.get('logs'):
                typer.echo("📝 Recent Logs:")
                for log in job.get('logs', [])[-5:]:  # Show last 5 logs
                    typer.echo(f"  - {log}")
        else:
            typer.echo(f"❌ Failed to get job status: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error getting job status: {e}")
        raise typer.Exit(1)

@app.command()
def logs(
    job_id: str = typer.Argument(..., help="Training job ID"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """Get logs for a training job."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.get_training_logs(job_id)
        if response.get('success'):
            logs = response.get('logs', [])
            if logs:
                typer.echo(f"📝 Logs for job {job_id}:")
                for log in logs:
                    typer.echo(f"  - {log}")
            else:
                typer.echo("📝 No logs available")
        else:
            typer.echo(f"❌ Failed to get logs: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error getting logs: {e}")
        raise typer.Exit(1)

@app.command()
def cancel(
    job_id: str = typer.Argument(..., help="Training job ID"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """Cancel a training job."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.cancel_training_job(job_id)
        if response.get('success'):
            typer.echo(f"✅ Job {job_id} cancelled successfully")
        else:
            typer.echo(f"❌ Failed to cancel job: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error cancelling job: {e}")
        raise typer.Exit(1)

@app.command()
def list(
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """List all training jobs."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.list_training_jobs()
        if response.get('success'):
            jobs = response.get('jobs', [])
            if jobs:
                typer.echo("📋 Training Jobs:")
                for job in jobs:
                    typer.echo(f"  - {job.get('job_id')}: {job.get('status')} ({job.get('model_type')})")
            else:
                typer.echo("📋 No training jobs found")
        else:
            typer.echo(f"❌ Failed to list jobs: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error listing jobs: {e}")
        raise typer.Exit(1)
