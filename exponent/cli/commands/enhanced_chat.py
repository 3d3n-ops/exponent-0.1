import typer
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt, Confirm
# from rich.scroll import Scroll  # Not available in older rich versions
from rich.console import Group

from exponent.core.agent import ExponentAgent

console = Console()

class EnhancedChatInterface:
    """Enhanced chat interface with rich TUI styling."""
    
    def __init__(self):
        self.agent = ExponentAgent()
        self.messages = []
        self.console = Console()
        
    def print_logo(self):
        """Display Exponent logo in ASCII art."""
        logo = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ███████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗████████╗  ║
║  ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝╚██╗██╔╝╚══██╔══╝  ║
║  ╚█████╗  ╚███╔╝ ██████╔╝██║   ██║██╔██╗ ██║█████╗  ╚███╔╝    ██║     ║
║   ╚═══██╗ ██╔██╗ ██╔═══╝ ██║   ██║██║╚██╗██║██╔══╝  ██╔██╗    ██║     ║
║  ██████╔╝██╔╝ ██╗██║     ╚██████╔╝██║ ╚████║███████╗██╔╝ ██╗   ██║     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝     ║
║                                                          ║
║                    E X P O N E N T                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        self.console.print(logo, style="bold cyan")
    
    def enhanced_welcome(self):
        """Display enhanced welcome message with rich formatting."""
        welcome_text = Text()
        welcome_text.append("🤖 ", style="bold blue")
        welcome_text.append("Welcome to ", style="bold white")
        welcome_text.append("Exponent", style="bold cyan")
        welcome_text.append(" - Your AI-Powered ML Engineering Assistant!", style="bold white")
        
        panel = Panel(
            welcome_text,
            title="[bold cyan]Exponent CLI[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)
        
        # Show capabilities
        capabilities = """
✨ I can help you with:
• 📊 Dataset analysis and preprocessing
• 🧠 Model training and evaluation  
• 🚀 Deployment strategies
• 🔧 Code analysis and improvement
• 📚 Best practices and troubleshooting
• 🛠️ Automatic tool execution

💡 Just ask me anything about ML, code, or your project!
Type 'help' for commands, 'exit' to quit.
        """
        
        self.console.print(Panel(
            capabilities,
            border_style="blue",
            padding=(1, 2)
        ))
    
    def create_message_bubble(self, sender: str, content: str, timestamp: str = None):
        """Create a styled message bubble."""
        if sender == "user":
            return Panel(
                f"{content}\n[dim]{timestamp or 'now'}[/dim]",
                border_style="blue",
                padding=(0, 1),
                title="[bold blue]You[/bold blue]"
            )
        else:
            return Panel(
                f"{content}\n[dim]{timestamp or 'now'}[/dim]",
                border_style="green",
                padding=(0, 1),
                title="[bold green]Exponent[/bold green]"
            )
    
    def format_code_response(self, code: str, language: str = "python"):
        """Format code blocks with syntax highlighting."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        return Panel(syntax, title=f"[bold]Code ({language})[/bold]", border_style="cyan")
    
    def format_markdown_response(self, content: str):
        """Render markdown content with rich formatting."""
        markdown = Markdown(content)
        return Panel(markdown, border_style="green", padding=(1, 2))
    
    def format_structured_response(self, title: str, content: str, response_type: str = "info"):
        """Format responses with consistent structure."""
        colors = {
            "info": "blue",
            "success": "green", 
            "warning": "yellow",
            "error": "red"
        }
        
        panel = Panel(
            content,
            title=f"[bold {colors[response_type]}]{title}[/bold {colors[response_type]}]",
            border_style=colors[response_type],
            padding=(1, 2)
        )
        return panel
    
    def show_typing_indicator(self):
        """Show typing indicator while AI is thinking."""
        with self.console.status("[bold green]Exponent is thinking...", spinner="dots"):
            # Simulate AI processing
            time.sleep(1)
    
    def show_progress_bar(self, description: str, total: int = 100):
        """Show progress bar for long-running operations."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(description, total=total)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.02)
    
    def create_main_menu(self):
        """Create an interactive main menu."""
        table = Table(title="[bold cyan]Exponent CLI - Main Menu[/bold cyan]")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Shortcut", style="dim")
        
        options = [
            ("1", "Ask Exponent a question", "exponent ask"),
            ("2", "Analyze a dataset", "exponent analyze"),
            ("3", "Create a new project", "exponent init"),
            ("4", "Train a model", "exponent train"),
            ("5", "Deploy a model", "exponent deploy"),
            ("6", "View project status", "exponent status"),
            ("7", "Exit", "exit")
        ]
        
        for option, description, shortcut in options:
            table.add_row(option, description, shortcut)
        
        self.console.print(table)
        return Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])
    
    def visualize_tool_execution(self, tool_name: str, params: dict, result: dict):
        """Visualize tool execution with rich formatting."""
        self.console.print(f"\n[bold cyan]🔧 Executing: {tool_name}[/bold cyan]")
        
        # Show parameters
        param_table = Table(title="Parameters")
        param_table.add_column("Parameter", style="cyan")
        param_table.add_column("Value", style="white")
        
        for key, value in params.items():
            param_table.add_row(key, str(value))
        
        self.console.print(param_table)
        
        # Show result
        if result.get('success'):
            self.console.print(f"[bold green]✅ {tool_name} completed successfully![/bold green]")
        else:
            self.console.print(f"[bold red]❌ {tool_name} failed: {result.get('error', 'Unknown error')}[/bold red]")
    
    def show_help(self):
        """Show enhanced help information."""
        help_text = """
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
• I automatically detect and execute tools when needed
        """
        
        self.console.print(Panel(
            help_text,
            title="[bold cyan]Help[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
    
    def show_status(self):
        """Show enhanced agent status."""
        status = self.agent.get_status()
        self.console.print(Panel(
            status,
            title="[bold cyan]Agent Status[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
    
    def run_enhanced_chat(self):
        """Run the enhanced chat interface."""
        # Print logo and welcome
        self.print_logo()
        self.enhanced_welcome()
        
        # Index current codebase
        self.console.print("🔍 Indexing your codebase for context...")
        self.agent.index_codebase(".")
        self.console.print("✅ Ready! Ask me anything about your ML project.\n")
        
        while True:
            try:
                # Get user input with enhanced styling
                user_input = Prompt.ask(
                    "\n[bold blue]💬 You[/bold blue]",
                    default=""
                )
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.console.print("[bold green]👋 Goodbye! Thanks for using Exponent![/bold green]")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'status':
                    self.show_status()
                    continue
                elif user_input.lower() == 'clear':
                    self.agent.clear_memory()
                    self.console.print("[bold green]🧹 Memory cleared![/bold green]")
                    continue
                elif user_input.lower() == 'menu':
                    choice = self.create_main_menu()
                    # Handle menu choices
                    if choice == "7":
                        self.console.print("[bold green]👋 Goodbye![/bold green]")
                        break
                    continue
                elif user_input.lower().startswith('analyze '):
                    # Handle analyze command
                    target = user_input[8:].strip()
                    if target:
                        self.console.print("[bold yellow]🔍 Analyzing...[/bold yellow]")
                        with self.console.status("[bold green]Processing...", spinner="dots"):
                            result = self.agent.analyze(target)
                        self.console.print(self.format_structured_response("Analysis Result", result, "info"))
                    else:
                        self.console.print("[bold red]❌ Please specify what to analyze (e.g., 'analyze data.csv')[/bold red]")
                    continue
                elif user_input.lower().startswith('train '):
                    # Handle train command
                    parts = user_input[6:].strip().split()
                    if len(parts) >= 1:
                        dataset_path = parts[0]
                        task = " ".join(parts[1:]) if len(parts) > 1 else None
                        self.console.print("[bold yellow]🚀 Starting training...[/bold yellow]")
                        with self.console.status("[bold green]Training...", spinner="dots"):
                            result = self.agent.train(dataset_path=dataset_path, task=task)
                        self.console.print(self.format_structured_response("Training Result", result, "success"))
                    else:
                        self.console.print("[bold red]❌ Please specify dataset path (e.g., 'train data.csv')[/bold red]")
                    continue
                elif user_input.lower().startswith('deploy '):
                    # Handle deploy command
                    parts = user_input[8:].strip().split()
                    if len(parts) >= 1:
                        model_path = parts[0]
                        provider = parts[1] if len(parts) > 1 else "github"
                        self.console.print("[bold yellow]🌐 Deploying...[/bold yellow]")
                        with self.console.status("[bold green]Deploying...", spinner="dots"):
                            result = self.agent.deploy(model_path, provider)
                        self.console.print(self.format_structured_response("Deployment Result", result, "success"))
                    else:
                        self.console.print("[bold red]❌ Please specify model path (e.g., 'deploy model.pkl')[/bold red]")
                    continue
                else:
                    # General question with enhanced formatting
                    self.show_typing_indicator()
                    response = self.agent.ask(user_input)
                    
                    # Format response based on content
                    if "```" in response:
                        # Contains code blocks
                        formatted_response = self.format_markdown_response(response)
                    else:
                        # Regular text response
                        formatted_response = self.format_structured_response("Exponent Response", response, "info")
                    
                    self.console.print(formatted_response)
                    
            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]👋 Goodbye![/bold yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]❌ Error: {e}[/bold red]")

def run_enhanced_chat_interface():
    """Run the enhanced chat interface."""
    chat_interface = EnhancedChatInterface()
    chat_interface.run_enhanced_chat()

if __name__ == "__main__":
    run_enhanced_chat_interface() 