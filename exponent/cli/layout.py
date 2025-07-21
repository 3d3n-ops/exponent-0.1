"""
Responsive layout manager for Exponent CLI TUI.
"""

import shutil
from typing import Dict, Any, Optional
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.text import Text

class ResponsiveLayout:
    """Manages responsive layouts based on terminal size."""
    
    def __init__(self):
        self.console = Console()
        self.terminal_width, self.terminal_height = shutil.get_terminal_size()
    
    def get_terminal_size(self) -> tuple:
        """Get current terminal dimensions."""
        return shutil.get_terminal_size()
    
    def get_layout_mode(self) -> str:
        """Determine layout mode based on terminal size."""
        width, height = self.get_terminal_size()
        
        if width < 80:
            return "compact"
        elif width < 120:
            return "standard"
        else:
            return "wide"
    
    def create_chat_layout(self) -> Layout:
        """Create a responsive chat layout."""
        layout = Layout()
        mode = self.get_layout_mode()
        
        if mode == "compact":
            # Single column layout for small terminals
            layout.split_column(
                Layout(name="header", size=2),
                Layout(name="chat_area", ratio=1),
                Layout(name="input_area", size=2)
            )
        elif mode == "standard":
            # Standard layout with sidebar
            layout.split_row(
                Layout(name="sidebar", ratio=1),
                Layout(name="main", ratio=3)
            )
            layout["main"].split_column(
                Layout(name="chat_area", ratio=1),
                Layout(name="input_area", size=2)
            )
        else:
            # Wide layout with multiple columns
            layout.split_row(
                Layout(name="sidebar", ratio=1),
                Layout(name="main", ratio=2),
                Layout(name="info", ratio=1)
            )
            layout["main"].split_column(
                Layout(name="chat_area", ratio=1),
                Layout(name="input_area", size=2)
            )
        
        return layout
    
    def create_dashboard_layout(self) -> Layout:
        """Create a responsive dashboard layout."""
        layout = Layout()
        mode = self.get_layout_mode()
        
        if mode == "compact":
            # Stacked layout for small terminals
            layout.split_column(
                Layout(name="header", size=2),
                Layout(name="stats", size=4),
                Layout(name="projects", ratio=1),
                Layout(name="actions", size=3)
            )
        else:
            # Grid layout for larger terminals
            layout.split_column(
                Layout(name="header", size=2),
                Layout(name="content", ratio=1)
            )
            layout["content"].split_row(
                Layout(name="stats", ratio=1),
                Layout(name="projects", ratio=2)
            )
        
        return layout
    
    def create_project_layout(self) -> Layout:
        """Create a responsive project management layout."""
        layout = Layout()
        mode = self.get_layout_mode()
        
        if mode == "compact":
            # Single column for small terminals
            layout.split_column(
                Layout(name="header", size=2),
                Layout(name="project_info", size=4),
                Layout(name="files", ratio=1),
                Layout(name="actions", size=3)
            )
        else:
            # Multi-column for larger terminals
            layout.split_row(
                Layout(name="sidebar", ratio=1),
                Layout(name="main", ratio=2)
            )
            layout["main"].split_column(
                Layout(name="project_info", size=4),
                Layout(name="files", ratio=1),
                Layout(name="actions", size=3)
            )
        
        return layout
    
    def create_header_panel(self, title: str = "Exponent CLI") -> Panel:
        """Create a responsive header panel."""
        width, height = self.get_terminal_size()
        
        if width < 80:
            # Compact header
            header_text = f"🤖 {title}"
        else:
            # Full header with logo
            header_text = f"""
🤖 {title} - Your AI-Powered ML Engineering Assistant
{'=' * (width - 10)}
            """
        
        return Panel(
            header_text,
            border_style="cyan",
            padding=(0, 1)
        )
    
    def create_sidebar_panel(self, content: str, title: str = "Quick Actions") -> Panel:
        """Create a responsive sidebar panel."""
        width, height = self.get_terminal_size()
        
        if width < 80:
            # Hide sidebar in compact mode
            return Panel("", border_style="cyan")
        
        return Panel(
            content,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            padding=(0, 1)
        )
    
    def create_chat_area_panel(self, messages: list) -> Panel:
        """Create a responsive chat area panel."""
        if not messages:
            content = "[dim]No messages yet. Start a conversation![/dim]"
        else:
            content = "\n".join(messages)
        
        return Panel(
            content,
            title="[bold cyan]Chat[/bold cyan]",
            border_style="green",
            padding=(0, 1)
        )
    
    def create_input_area_panel(self, prompt: str = "💬 You") -> Panel:
        """Create a responsive input area panel."""
        return Panel(
            f"{prompt}: ",
            title="[bold blue]Input[/bold blue]",
            border_style="blue",
            padding=(0, 1)
        )
    
    def create_stats_panel(self, stats: Dict[str, Any]) -> Panel:
        """Create a responsive stats panel."""
        table = Table(title="[bold cyan]Project Statistics[/bold cyan]")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        for metric, value in stats.items():
            table.add_row(metric, str(value))
        
        return Panel(table, border_style="cyan")
    
    def create_projects_panel(self, projects: list) -> Panel:
        """Create a responsive projects panel."""
        table = Table(title="[bold cyan]Recent Projects[/bold cyan]")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Updated", style="dim")
        
        for project in projects[:5]:  # Show only first 5
            table.add_row(
                project.get('name', 'Unknown'),
                project.get('status', 'Unknown'),
                project.get('updated', 'Unknown')
            )
        
        return Panel(table, border_style="cyan")
    
    def create_actions_panel(self, actions: list) -> Panel:
        """Create a responsive actions panel."""
        table = Table(title="[bold cyan]Quick Actions[/bold cyan]")
        table.add_column("Action", style="cyan")
        table.add_column("Shortcut", style="dim")
        
        for action, shortcut in actions:
            table.add_row(action, shortcut)
        
        return Panel(table, border_style="cyan")
    
    def adapt_content_to_width(self, content: str, max_width: int = None) -> str:
        """Adapt content to fit terminal width."""
        if max_width is None:
            width, _ = self.get_terminal_size()
            max_width = width - 4  # Account for borders and padding
        
        if len(content) <= max_width:
            return content
        
        # Truncate content to fit
        return content[:max_width-3] + "..."
    
    def create_progress_layout(self, title: str = "Progress") -> Layout:
        """Create a layout for progress displays."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=1),
            Layout(name="progress", size=3),
            Layout(name="details", ratio=1)
        )
        
        return layout
    
    def create_tool_execution_layout(self) -> Layout:
        """Create a layout for tool execution visualization."""
        layout = Layout()
        mode = self.get_layout_mode()
        
        if mode == "compact":
            layout.split_column(
                Layout(name="tool_info", size=3),
                Layout(name="progress", size=2),
                Layout(name="result", ratio=1)
            )
        else:
            layout.split_row(
                Layout(name="tool_info", ratio=1),
                Layout(name="main", ratio=2)
            )
            layout["main"].split_column(
                Layout(name="progress", size=2),
                Layout(name="result", ratio=1)
            )
        
        return layout

class LayoutManager:
    """High-level layout manager for different application modes."""
    
    def __init__(self):
        self.responsive_layout = ResponsiveLayout()
        self.console = Console()
    
    def create_chat_interface(self) -> Layout:
        """Create a complete chat interface layout."""
        layout = self.responsive_layout.create_chat_layout()
        
        # Add content to layout sections
        layout["header"].update(self.responsive_layout.create_header_panel())
        
        # Add sidebar if in wide mode
        if self.responsive_layout.get_layout_mode() != "compact":
            sidebar_content = """
📊 Quick Stats
• Projects: 3
• Models: 5
• Datasets: 2

🔧 Quick Actions
• New Project
• Analyze Data
• Train Model
• Deploy Model
            """
            layout["sidebar"].update(
                self.responsive_layout.create_sidebar_panel(sidebar_content)
            )
        
        # Add info panel if in wide mode
        if self.responsive_layout.get_layout_mode() == "wide":
            info_content = """
📋 Recent Activity
• Analyzed dataset.csv
• Created project "Churn"
• Trained model (15min ago)
• Deployed to GitHub
            """
            layout["info"].update(
                Panel(info_content, title="[bold cyan]Activity[/bold cyan]", border_style="cyan")
            )
        
        return layout
    
    def create_dashboard_interface(self) -> Layout:
        """Create a complete dashboard interface layout."""
        layout = self.responsive_layout.create_dashboard_layout()
        
        # Add header
        layout["header"].update(self.responsive_layout.create_header_panel("Dashboard"))
        
        # Add stats
        stats = {
            "Total Projects": 3,
            "Active Models": 2,
            "Datasets": 5,
            "Deployments": 1
        }
        layout["stats"].update(self.responsive_layout.create_stats_panel(stats))
        
        # Add projects
        projects = [
            {"name": "Customer Churn", "status": "✅ Complete", "updated": "2h ago"},
            {"name": "Sales Prediction", "status": "🔄 Training", "updated": "5m ago"},
            {"name": "Image Classifier", "status": "⏳ Pending", "updated": "1d ago"}
        ]
        layout["projects"].update(self.responsive_layout.create_projects_panel(projects))
        
        # Add actions
        actions = [
            ("New Project", "exponent init"),
            ("Analyze Data", "exponent analyze"),
            ("Train Model", "exponent train"),
            ("Deploy Model", "exponent deploy")
        ]
        layout["actions"].update(self.responsive_layout.create_actions_panel(actions))
        
        return layout
    
    def create_project_interface(self, project_name: str) -> Layout:
        """Create a project-specific interface layout."""
        layout = self.responsive_layout.create_project_layout()
        
        # Add header
        layout["header"].update(
            self.responsive_layout.create_header_panel(f"Project: {project_name}")
        )
        
        # Add project info
        project_info = f"""
📁 Project: {project_name}
📊 Dataset: netflix_customer_churn.csv
🧠 Model: Random Forest
📈 Status: Training Complete
        """
        layout["project_info"].update(
            Panel(project_info, title="[bold cyan]Project Info[/bold cyan]", border_style="cyan")
        )
        
        # Add files
        files_content = """
📄 Files:
• model.py
• train.py
• predict.py
• requirements.txt
• README.md
        """
        layout["files"].update(
            Panel(files_content, title="[bold cyan]Project Files[/bold cyan]", border_style="cyan")
        )
        
        # Add actions
        actions = [
            ("Train Model", "exponent train"),
            ("Deploy Model", "exponent deploy"),
            ("Analyze Results", "exponent analyze"),
            ("View Logs", "exponent logs")
        ]
        layout["actions"].update(self.responsive_layout.create_actions_panel(actions))
        
        return layout
    
    def print_layout(self, layout: Layout):
        """Print a layout to the console."""
        self.console.print(layout)
    
    def get_terminal_info(self) -> Dict[str, Any]:
        """Get information about the terminal."""
        width, height = self.responsive_layout.get_terminal_size()
        mode = self.responsive_layout.get_layout_mode()
        
        return {
            "width": width,
            "height": height,
            "mode": mode,
            "supports_color": self.console.color_system is not None,
            "supports_unicode": self.console.unicode_support
        } 