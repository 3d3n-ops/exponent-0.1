import typer
from pathlib import Path
from exponent.api.client import ExponentAPIClient

app = typer.Typer()

def run_deployment(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    model_path: str = typer.Option(None, "--model-path", "-m", help="Path to trained model"),
    deployment_type: str = typer.Option("api", "--type", "-t", help="Deployment type (api, web, mobile)"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for deployment completion")
):
    """Deploy ML model using the Exponent API backend."""
    
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
        raise typer.Exit(1)
    
    if not model_path:
        # Try to find model in project directory
        home_dir = Path.home() / ".exponent" / project_id
        if home_dir.exists():
            model_path = str(home_dir / "models" / "model.pkl")
        else:
            typer.echo("❌ Model path is required")
            raise typer.Exit(1)
    
    # Create deployment job
    try:
        typer.echo(f"🚀 Creating deployment job for project: {project_id}")
        typer.echo(f"📁 Model path: {model_path}")
        typer.echo(f"🌐 Deployment type: {deployment_type}")
        
        response = client.create_deployment_job(
            project_id=project_id,
            model_path=model_path,
            deployment_type=deployment_type
        )
        
        if response.get('success'):
            job = response.get('job', {})
            deployment_id = job.get('deployment_id')
            typer.echo(f"✅ Deployment job created successfully!")
            typer.echo(f"📋 Deployment ID: {deployment_id}")
            typer.echo(f"📊 Status: {job.get('status')}")
            
            if wait:
                typer.echo("⏳ Waiting for deployment completion...")
                final_response = client.wait_for_job_completion(deployment_id, 'deployment')
                final_job = final_response.get('job', {})
                
                if final_job.get('status') == 'completed':
                    typer.echo("✅ Deployment completed successfully!")
                    endpoint_url = final_job.get('endpoint_url')
                    if endpoint_url:
                        typer.echo(f"🌐 Endpoint URL: {endpoint_url}")
                else:
                    typer.echo(f"❌ Deployment failed: {final_job.get('error_message')}")
                    raise typer.Exit(1)
            else:
                typer.echo("💡 Use 'exponent deploy status <deployment_id>' to check progress")
                
        else:
            typer.echo(f"❌ Failed to create deployment job: {response.get('error')}")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error creating deployment job: {e}")
        raise typer.Exit(1)

@app.callback()
def deploy_callback(
    ctx: typer.Context,
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    model_path: str = typer.Option(None, "--model-path", "-m", help="Path to trained model"),
    deployment_type: str = typer.Option("api", "--type", "-t", help="Deployment type (api, web, mobile)"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for deployment completion")
):
    """Deploy ML models using the Exponent API backend."""
    if ctx.invoked_subcommand is None:
        # No subcommand specified, run default deployment
        run_deployment(project_id, model_path, deployment_type, api_url, wait)

@app.command()
def run(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    model_path: str = typer.Option(None, "--model-path", "-m", help="Path to trained model"),
    deployment_type: str = typer.Option("api", "--type", "-t", help="Deployment type (api, web, mobile)"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for deployment completion")
):
    """Deploy ML model using the Exponent API backend."""
    run_deployment(project_id, model_path, deployment_type, api_url, wait)

@app.command()
def status(
    deployment_id: str = typer.Argument(..., help="Deployment job ID"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """Check status of a deployment job."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.get_deployment_job(deployment_id)
        if response.get('success'):
            job = response.get('job', {})
            typer.echo(f"📊 Deployment Status: {job.get('status')}")
            typer.echo(f"📋 Deployment ID: {job.get('deployment_id')}")
            typer.echo(f"📁 Project: {job.get('project_id')}")
            typer.echo(f"📁 Model Path: {job.get('model_path')}")
            typer.echo(f"🌐 Deployment Type: {job.get('deployment_type')}")
            
            if job.get('endpoint_url'):
                typer.echo(f"🌐 Endpoint URL: {job.get('endpoint_url')}")
        else:
            typer.echo(f"❌ Failed to get deployment status: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error getting deployment status: {e}")
        raise typer.Exit(1)

@app.command()
def cancel(
    deployment_id: str = typer.Argument(..., help="Deployment job ID"),
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """Cancel a deployment job."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.cancel_deployment_job(deployment_id)
        if response.get('success'):
            typer.echo(f"✅ Deployment {deployment_id} cancelled successfully")
        else:
            typer.echo(f"❌ Failed to cancel deployment: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error cancelling deployment: {e}")
        raise typer.Exit(1)

@app.command()
def list(
    api_url: str = typer.Option("http://localhost:5000", "--api-url", help="API server URL")
):
    """List all deployment jobs."""
    client = ExponentAPIClient(api_url)
    
    try:
        response = client.list_deployment_jobs()
        if response.get('success'):
            jobs = response.get('jobs', [])
            if jobs:
                typer.echo("📋 Deployment Jobs:")
                for job in jobs:
                    typer.echo(f"  - {job.get('deployment_id')}: {job.get('status')} ({job.get('deployment_type')})")
            else:
                typer.echo("📋 No deployment jobs found")
        else:
            typer.echo(f"❌ Failed to list deployments: {response.get('error')}")
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Error listing deployments: {e}")
        raise typer.Exit(1)
