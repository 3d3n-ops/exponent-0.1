import typer
from exponent.cli.commands import init, train, deploy
from exponent.cli.commands.analyze import run_analysis
from exponent.cli.commands.interactive import app as interactive_app
from exponent.cli.commands.chat import app as chat_app
from exponent.core.auth import auth_manager
from exponent.core.setup import run_setup_wizard, check_setup

app = typer.Typer(
    name="exponent",
    help="Exponent-ML: Your AI-Powered ML Engineering Assistant",
    add_completion=False,
    no_args_is_help=False  # Changed to False to allow default command
)

# Add commands
app.add_typer(init.app, name="init", help="Initialize new ML project")
app.add_typer(interactive_app, name="interactive", help="Interactive wizard for building ML models end-to-end")
app.add_typer(chat_app, name="chat", help="Chat with Exponent AI assistant")

# Default command - runs when no arguments are provided
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Exponent-ML: Your AI-Powered ML Engineering Assistant"""
    if ctx.invoked_subcommand is None:
        # Check if setup is complete or ANTHROPIC_API_KEY is set
        import os
        if not check_setup() and not os.getenv("ANTHROPIC_API_KEY"):
            typer.echo("🔧 First time setup detected!")
            typer.echo("💡 You can either:")
            typer.echo("   1. Run 'exponent setup' to configure OpenRouter")
            typer.echo("   2. Set ANTHROPIC_API_KEY environment variable to use Anthropic directly")
            typer.echo("   3. Run 'exponent ask \"question\"' to test with your API key")
            raise typer.Exit(1)
        
        # Start the chat interface
        from exponent.cli.commands.chat import run_chat_interface
        run_chat_interface()

# Add ask command
@app.command()
def ask(
    question: str = typer.Argument(..., help="Your question for the agent"),
    project_path: str = typer.Option(".", "--path", "-p", help="Project path to analyze")
):
    """Ask the agent a specific question."""
    from exponent.cli.commands.chat import ask as ask_command
    ask_command(question, project_path)

# Add analyze command with authentication
@app.command()
@auth_manager.require_auth()
def analyze(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    prompt: str = typer.Option(None, "--prompt", "-p", help="Analysis prompt for AI"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory for analysis")
):
    """Analyze datasets with AI-powered analysis and visualization."""
    run_analysis(dataset_path, prompt, output_dir)

# Add train command
@app.command()
def train(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to train"),
    dataset_path: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    task_description: str = typer.Option(None, "--task", "-t", help="Task description"),
    cloud: bool = typer.Option(False, "--cloud", "-c", help="Use cloud training (Modal)"),
    use_s3: bool = typer.Option(False, "--s3", help="Upload dataset to S3 for cloud training"),
    status: str = typer.Option(None, "--status", help="Check status of training job"),
    list_jobs: bool = typer.Option(False, "--list", help="List all training jobs")
):
    """Train ML models with Exponent-ML."""
    if status:
        # Check status of specific job
        from exponent.core.modal_runner import get_training_status
        try:
            status_info = get_training_status(status)
            typer.echo(f"📊 Job Status: {status_info}")
        except Exception as e:
            typer.echo(f"❌ Error getting job status: {e}")
            raise typer.Exit(1)
    elif list_jobs:
        # List all jobs
        from exponent.core.modal_runner import list_training_jobs
        try:
            jobs = list_training_jobs()
            if jobs:
                typer.echo("📋 Training Jobs:")
                for job in jobs:
                    typer.echo(f"  - {job}")
            else:
                typer.echo("📋 No training jobs found")
        except Exception as e:
            typer.echo(f"❌ Error listing jobs: {e}")
            raise typer.Exit(1)
    else:
        # Run default training - import and call the training function directly
        from exponent.cli.commands.train import run as train_run
        train_run(project_id, dataset_path, task_description, cloud, use_s3)

app.add_typer(deploy.app, name="deploy", help="Deploy projects to GitHub")

@app.command()
def setup():
    """Run the initial setup wizard for Exponent-ML."""
    run_setup_wizard()

@app.command()
def login(
    provider: str = typer.Option(None, "--provider", "-p", help="OAuth provider (google, github)")
):
    """Authenticate with Exponent-ML."""
    if auth_manager.authenticate_user(provider):
        typer.echo("✅ Login successful!")
    else:
        typer.echo("❌ Login failed!")
        raise typer.Exit(1)

@app.command()
def logout():
    """Logout from Exponent-ML."""
    auth_manager.clear_token()
    typer.echo("✅ Logged out successfully!")

@app.command()
def status():
    """Check authentication status and setup."""
    # Check setup status
    if check_setup():
        typer.echo("✅ Setup: Complete")
    else:
        typer.echo("❌ Setup: Incomplete - Run 'exponent setup' to configure")
    
    # Check authentication status
    if auth_manager.is_authenticated():
        user_info = auth_manager.get_user_info()
        typer.echo("✅ Authentication: Active")
        if user_info:
            typer.echo(f"👤 User: {user_info.get('name', 'Unknown')}")
            typer.echo(f"📧 Email: {user_info.get('email', 'Unknown')}")
            typer.echo(f"🔗 Provider: {user_info.get('provider', 'Unknown')}")
    else:
        typer.echo("❌ Authentication: Not authenticated")
        typer.echo("💡 Run 'exponent login' to authenticate")

@app.command()
def version():
    """Show version information."""
    typer.echo("Exponent-ML v0.1.0")

@app.command()
def help():
    """Show detailed help and examples."""
    typer.echo("""
🤖 Exponent-ML: Your AI-Powered ML Engineering Assistant

📋 Quick Start:
1. Run the setup: exponent setup
2. Start chatting: exponent
3. Ask questions: exponent ask "How do I improve my model?"
4. Analyze data: exponent analyze data.csv
5. Train models: exponent train data.csv "classify customer churn"

📚 Commands:

🎯 DEFAULT - AI Assistant Chat
  exponent                    # Start chat interface (default)
  exponent chat start        # Start interactive chat
  exponent ask "question"    # Ask a specific question

🔧 PROJECT MANAGEMENT
  exponent init quick "task description" --dataset data.csv
  exponent init run --task "classify emails" --dataset emails.csv

🎯 INTERACTIVE - Full agentic workflow
  exponent interactive wizard  # Complete ML pipeline

📊 ANALYSIS - AI-powered analysis
  exponent analyze data.csv
  exponent analyze model.py
  exponent analyze results.pkl

🚀 TRAINING - Train ML models
  exponent train data.csv "classify customer churn"
  exponent train --project-id abc123 --dataset data.csv --task "classify"
  exponent train --cloud  # Use cloud training
  exponent train --status <job_id>  # Check training status

🌐 DEPLOYMENT - Deploy models
  exponent deploy model.pkl github
  exponent deploy --project-id abc123
  exponent deploy list  # List GitHub repos

🎨 TUI CUSTOMIZATION
  exponent tui config       # Configure TUI appearance
  exponent tui demo         # Demo enhanced TUI features
  exponent tui themes       # List available themes

🔧 UTILITY
  exponent status            # Show agent status
  exponent setup            # First time setup

💡 Examples:

# Quick start (recommended)
exponent                    # Start AI assistant
exponent setup             # First time setup

# Chat with AI
exponent ask "How can I improve my model's accuracy?"
exponent ask "What preprocessing should I do for this dataset?"

# Analysis
exponent analyze data.csv
exponent analyze model.py

# Training
exponent train data.csv "predict customer churn"
exponent train --project-id my-project --dataset data.csv --task "predict sales" --cloud

# Deployment
exponent deploy model.pkl github

# TUI Customization
exponent tui config         # Configure interface appearance
exponent tui demo           # See enhanced features

📖 For more help on specific commands:
  exponent <command> --help
  exponent chat --help
  exponent ask --help
  exponent analyze --help
  exponent train --help
  exponent deploy --help
  exponent tui --help
""")

@app.command()
def tui(
    action: str = typer.Argument(..., help="TUI action (config, demo, themes)")
):
    """Manage TUI (Terminal User Interface) settings and features."""
    if action == "config":
        try:
            from exponent.cli.tui_config import create_tui_config_wizard
            create_tui_config_wizard()
        except ImportError:
            typer.echo("❌ TUI configuration not available. Install rich library.")
    elif action == "demo":
        try:
            import subprocess
            subprocess.run([sys.executable, "demo_enhanced_tui.py"])
        except FileNotFoundError:
            typer.echo("❌ TUI demo not found. Run 'python demo_enhanced_tui.py'")
    elif action == "themes":
        try:
            from exponent.cli.themes import ThemeManager
            theme_manager = ThemeManager()
            themes = theme_manager.get_available_themes()
            typer.echo("Available themes:")
            for theme in themes:
                typer.echo(f"• {theme}")
        except ImportError:
            typer.echo("❌ Theme management not available.")
    else:
        typer.echo(f"❌ Unknown TUI action: {action}")
        typer.echo("Available actions: config, demo, themes")

if __name__ == "__main__":
    app()