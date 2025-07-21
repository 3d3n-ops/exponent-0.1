import typer
import inquirer
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import json

class SetupWizard:
    """Setup wizard for Exponent-ML initial configuration."""
    
    def __init__(self):
        self.config_file = Path.home() / ".exponent" / "config.json"
        self.config_file.parent.mkdir(exist_ok=True)
    
    def show_welcome(self):
        """Display welcome message and introduction."""
        typer.echo("""
🧠 Welcome to Exponent-ML - Your AI-Powered ML Development Assistant!

Exponent-ML is a revolutionary CLI tool that helps you build, train, and deploy 
machine learning models using advanced AI agents. Here's what makes us special:

✨ Key Features:
• 🤖 AI-powered code generation with multiple coding agents
• 📊 Automatic dataset analysis and visualization
• 🚀 Cloud training with Modal integration
• 🌐 Easy deployment to GitHub/AWS
• 🔧 Intelligent error handling and recovery
• 🎯 Interactive project setup and management

🔧 How it works:
1. You describe your ML project in natural language
2. Our AI agents analyze your dataset and generate code
3. We train your model in the cloud with real-time monitoring
4. You deploy your model with one command

Ready to get started? Let's set up your AI coding agent! 🚀
""")
        
        # Wait for user to read
        typer.prompt("Press Enter to continue...")
    
    def setup_openrouter(self) -> bool:
        """Setup OpenRouter integration for AI coding agents."""
        typer.echo("\n🔑 Setting up your AI Coding Agent")
        typer.echo("=" * 50)
        typer.echo("""
Exponent-ML uses OpenRouter to connect you with the best AI coding agents.
OpenRouter provides access to multiple AI models including:
• Claude 3.5 Sonnet (Anthropic)
• GPT-4 Turbo (OpenAI)
• CodeLlama (Meta)
• And many more...

To get started, you'll need to:
1. Create a free account at https://openrouter.ai
2. Get your API key from the dashboard
3. Choose your preferred coding agent
""")
        
        # Get OpenRouter API key
        questions = [
            inquirer.Text('openrouter_key',
                         message="🔑 Enter your OpenRouter API key",
                         validate=lambda _, x: len(x) > 0),
            inquirer.List('agent_model',
                         message="🤖 Choose your preferred coding agent",
                         choices=[
                             ('Claude 3.5 Sonnet (Recommended)', 'claude-3.5-sonnet'),
                             ('GPT-4 Turbo', 'gpt-4-turbo'),
                             ('CodeLlama 70B', 'codellama/codellama-70b-instruct'),
                             ('Claude 3 Haiku', 'claude-3-haiku'),
                             ('GPT-4', 'gpt-4'),
                             ('Custom Model', 'custom')
                         ])
        ]
        
        answers = inquirer.prompt(questions)
        if not answers:
            return False
        
        openrouter_key = answers['openrouter_key']
        agent_model = answers['agent_model']
        
        # If custom model, get the model name
        if agent_model == 'custom':
            custom_model = typer.prompt("🔧 Enter your custom model name")
            agent_model = custom_model
        
        # Test the API key
        typer.echo("\n🔍 Testing your OpenRouter connection...")
        if self.test_openrouter_connection(openrouter_key, agent_model):
            typer.echo("✅ OpenRouter connection successful!")
            
            # Save configuration
            config = {
                'openrouter_api_key': openrouter_key,
                'agent_model': agent_model,
                'setup_completed': True
            }
            
            self.save_config(config)
            return True
        else:
            typer.echo("❌ Failed to connect to OpenRouter")
            typer.echo("💡 Please check your API key and try again")
            return False
    
    def test_openrouter_connection(self, api_key: str, model: str) -> bool:
        """Test OpenRouter API connection."""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://exponent-ml.com",
                "X-Title": "Exponent-ML"
            }
            
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Hello! This is a test message from Exponent-ML."}
                ],
                "max_tokens": 10
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
            )
            
            # Print debug info
            typer.echo(f"🔍 Response status: {response.status_code}")
            if response.status_code != 200:
                typer.echo(f"🔍 Response body: {response.text[:200]}")
            
            return response.status_code == 200
            
        except Exception as e:
            typer.echo(f"⚠️ Connection test error: {e}")
            return False
    
    def show_agent_warning(self):
        """Show warning about AI agent capabilities and limitations."""
        typer.echo("\n⚠️ Important Information About AI Agents")
        typer.echo("=" * 50)
        typer.echo("""
🤖 AI Agent Capabilities:
• Generate production-ready ML code
• Analyze datasets and create visualizations
• Handle complex ML workflows
• Provide intelligent error recovery
• Suggest improvements and optimizations

⚠️ Important Limitations:
• AI agents may occasionally make mistakes
• Generated code should always be reviewed
• Complex projects may require human oversight
• Always test your models before deployment
• Keep your API keys secure and private

🔒 Best Practices:
• Review all generated code before running
• Test your models on sample data first
• Monitor training progress and logs
• Keep backups of your datasets
• Use version control for your projects

✅ By continuing, you acknowledge that:
• You will review all generated code
• You understand AI agents have limitations
• You will test your models before deployment
• You are responsible for your project outcomes
""")
        
        # Get user confirmation
        confirm = typer.confirm(
            "🤔 Do you understand and accept these terms?",
            default=True
        )
        
        if not confirm:
            typer.echo("❌ Setup cancelled. You can run 'exponent' again when ready.")
            raise typer.Exit(1)
        
        typer.echo("✅ Thank you! Let's build some amazing ML models! 🚀")
    
    def show_commands_overview(self):
        """Show overview of available commands."""
        typer.echo("\n📚 Available Commands")
        typer.echo("=" * 30)
        typer.echo("""
🎯 Main Commands:
• exponent                    - Start interactive project wizard
• exponent analyze <dataset>  - Analyze datasets with AI
• exponent train             - Train your ML models
• exponent deploy            - Deploy to GitHub/AWS

🔧 Utility Commands:
• exponent status            - Check setup and authentication
• exponent help             - Show detailed help
• exponent version          - Show version information

💡 Quick Start Examples:
• exponent                  # Start interactive wizard
• exponent analyze data.csv # Analyze your dataset
• exponent train           # Train your model
• exponent deploy          # Deploy your project
""")
        
        typer.prompt("Press Enter to continue...")
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None
    
    def is_setup_complete(self) -> bool:
        """Check if setup is complete."""
        config = self.load_config()
        return config and config.get('setup_completed', False)
    
    def run_setup(self) -> bool:
        """Run the complete setup wizard."""
        try:
            # Check if already setup
            if self.is_setup_complete():
                typer.echo("✅ Exponent-ML is already configured!")
                return True
            
            # Show welcome
            self.show_welcome()
            
            # Setup OpenRouter
            if not self.setup_openrouter():
                return False
            
            # Show warning
            self.show_agent_warning()
            
            # Show commands overview
            self.show_commands_overview()
            
            typer.echo("\n🎉 Setup Complete!")
            typer.echo("🚀 You're ready to build amazing ML models!")
            typer.echo("💡 Run 'exponent' to start your first project!")
            
            return True
            
        except Exception as e:
            typer.echo(f"❌ Setup failed: {e}")
            return False

def run_setup_wizard() -> bool:
    """Run the setup wizard."""
    wizard = SetupWizard()
    return wizard.run_setup()

def check_setup() -> bool:
    """Check if setup is complete."""
    # Check if ANTHROPIC_API_KEY is set in environment
    import os
    if os.getenv("ANTHROPIC_API_KEY"):
        return True
    
    # Check if OpenRouter setup is complete
    wizard = SetupWizard()
    return wizard.is_setup_complete() 