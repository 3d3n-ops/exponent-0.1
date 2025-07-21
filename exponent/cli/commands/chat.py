import typer
import inquirer
from pathlib import Path
from exponent.core.agent import ExponentAgent

app = typer.Typer()

def welcome_message():
    """Display welcome message for the chat interface."""
    typer.echo("""
🤖 Welcome to Exponent - Your AI-Powered ML Engineering Assistant!

I'm here to help you with:
• 📊 Dataset analysis and preprocessing
• 🧠 Model training and evaluation  
• 🚀 Deployment strategies
• 🔧 Code analysis and improvement
• 📚 Best practices and troubleshooting

Just ask me anything about ML, code, or your project!
Type 'help' for commands, 'exit' to quit.
""")

def run_chat_interface():
    """Run the interactive chat interface."""
    # Try to use enhanced chat interface if available
    try:
        from exponent.cli.commands.enhanced_chat import run_enhanced_chat_interface
        run_enhanced_chat_interface()
    except ImportError:
        # Fallback to basic chat interface
        agent = ExponentAgent()
        welcome_message()
        
        # Index current codebase
        typer.echo("🔍 Indexing your codebase for context...")
        agent.index_codebase(".")
        typer.echo("✅ Ready! Ask me anything about your ML project.\n")
        
        while True:
            try:
                # Get user input
                user_input = typer.prompt("💬 You")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    typer.echo("👋 Goodbye! Thanks for using Exponent!")
                    break
                elif user_input.lower() == 'help':
                    show_help()
                    continue
                elif user_input.lower() == 'status':
                    typer.echo(agent.get_status())
                    continue
                elif user_input.lower() == 'clear':
                    agent.clear_memory()
                    typer.echo("🧹 Memory cleared!")
                    continue
                elif user_input.lower().startswith('analyze '):
                    # Handle analyze command
                    target = user_input[8:].strip()
                    if target:
                        typer.echo("🔍 Analyzing...")
                        result = agent.analyze(target)
                        typer.echo(f"🤖 Exponent: {result}")
                    else:
                        typer.echo("❌ Please specify what to analyze (e.g., 'analyze data.csv')")
                    continue
                elif user_input.lower().startswith('train '):
                    # Handle train command
                    parts = user_input[6:].strip().split()
                    if len(parts) >= 1:
                        dataset_path = parts[0]
                        task = " ".join(parts[1:]) if len(parts) > 1 else None
                        typer.echo("🚀 Starting training...")
                        result = agent.train(dataset_path=dataset_path, task=task)
                        typer.echo(f"🤖 Exponent: {result}")
                    else:
                        typer.echo("❌ Please specify dataset path (e.g., 'train data.csv')")
                    continue
                elif user_input.lower().startswith('deploy '):
                    # Handle deploy command
                    parts = user_input[8:].strip().split()
                    if len(parts) >= 1:
                        model_path = parts[0]
                        provider = parts[1] if len(parts) > 1 else "github"
                        typer.echo("🌐 Deploying...")
                        result = agent.deploy(model_path, provider)
                        typer.echo(f"🤖 Exponent: {result}")
                    else:
                        typer.echo("❌ Please specify model path (e.g., 'deploy model.pkl')")
                    continue
                else:
                    # General question
                    typer.echo("🤖 Thinking...")
                    response = agent.ask(user_input)
                    typer.echo(f"🤖 Exponent: {response}")
                    
            except KeyboardInterrupt:
                typer.echo("\n👋 Goodbye! Thanks for using Exponent!")
                break
            except Exception as e:
                typer.echo(f"❌ Error: {e}")

def show_help():
    """Show help information."""
    typer.echo("""
📚 Exponent Commands:
====================

💬 General Questions:
  Just ask anything about ML, code, or your project!

🔍 Analysis:
  analyze <file>     - Analyze dataset, model, or code file
  Examples:
    analyze data.csv
    analyze model.py
    analyze results.pkl

🚀 Training:
  train <dataset> [task]  - Train a model on dataset
  Examples:
    train data.csv
    train data.csv "classify customer churn"

🌐 Deployment:
  deploy <model> [provider]  - Deploy model to provider
  Examples:
    deploy model.pkl
    deploy model.pkl github

🔧 Utility:
  status              - Show agent status and memory
  clear               - Clear chat history
  help                - Show this help
  exit                - Exit chat

💡 Tips:
• I remember our conversations and project context
• I can analyze your codebase automatically
• I provide specific, actionable advice
• I can help with any ML task from data to deployment
""")

@app.command()
def start():
    """Start the interactive chat interface."""
    run_chat_interface()

@app.command()
def ask(
    question: str = typer.Argument(..., help="Your question for the agent"),
    project_path: str = typer.Option(".", "--path", "-p", help="Project path to analyze")
):
    """Ask the agent a specific question."""
    agent = ExponentAgent()
    response = agent.ask(question, project_path)
    typer.echo(response)

@app.command()
def analyze(
    target: str = typer.Argument(..., help="File to analyze (dataset, model, or code)"),
    analysis_type: str = typer.Option("auto", "--type", "-t", help="Analysis type")
):
    """Analyze a dataset, model, or code file."""
    agent = ExponentAgent()
    result = agent.analyze(target, analysis_type)
    typer.echo(result)

@app.command()
def train(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    task: str = typer.Option(None, "--task", "-t", help="Task description"),
    model_path: str = typer.Option(None, "--model", "-m", help="Path to save training script")
):
    """Train a model on the specified dataset."""
    agent = ExponentAgent()
    result = agent.train(model_path, dataset_path, task)
    typer.echo(result)

@app.command()
def deploy(
    model_path: str = typer.Argument(..., help="Path to model file"),
    provider: str = typer.Option("github", "--provider", "-p", help="Deployment provider")
):
    """Deploy a model to the specified provider."""
    agent = ExponentAgent()
    result = agent.deploy(model_path, provider)
    typer.echo(result)

@app.command()
def status():
    """Show agent status and memory."""
    agent = ExponentAgent()
    typer.echo(agent.get_status())

@app.command()
def clear():
    """Clear chat history and memory."""
    agent = ExponentAgent()
    result = agent.clear_memory()
    typer.echo(result) 