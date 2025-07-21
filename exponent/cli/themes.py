"""
Theme manager for Exponent CLI TUI styling.
"""

from typing import Dict, Any
from rich.console import Console
from rich.theme import Theme

class ThemeManager:
    """Manages different color themes for the TUI."""
    
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": self._get_dark_theme(),
            "light": self._get_light_theme(),
            "high_contrast": self._get_high_contrast_theme(),
            "blue": self._get_blue_theme(),
            "green": self._get_green_theme()
        }
    
    def _get_dark_theme(self) -> Dict[str, str]:
        """Get dark theme colors."""
        return {
            'background': 'black',
            'text': 'white',
            'primary': 'cyan',
            'secondary': 'blue',
            'success': 'green',
            'warning': 'yellow',
            'error': 'red',
            'muted': 'bright_black',
            'code': 'bright_white on bright_black',
            'title': 'bold cyan',
            'subtitle': 'bold blue',
            'highlight': 'bold magenta',
            'info': 'white',
            'border': 'cyan'
        }
    
    def _get_light_theme(self) -> Dict[str, str]:
        """Get light theme colors."""
        return {
            'background': 'white',
            'text': 'black',
            'primary': 'blue',
            'secondary': 'cyan',
            'success': 'green',
            'warning': 'yellow',
            'error': 'red',
            'muted': 'bright_black',
            'code': 'black on bright_white',
            'title': 'bold blue',
            'subtitle': 'bold cyan',
            'highlight': 'bold magenta',
            'info': 'black',
            'border': 'blue'
        }
    
    def _get_high_contrast_theme(self) -> Dict[str, str]:
        """Get high contrast theme colors."""
        return {
            'background': 'bright_white',
            'text': 'black',
            'primary': 'bright_blue',
            'secondary': 'bright_cyan',
            'success': 'bright_green',
            'warning': 'bright_yellow',
            'error': 'bright_red',
            'muted': 'black',
            'code': 'black on bright_white',
            'title': 'bold bright_blue',
            'subtitle': 'bold bright_cyan',
            'highlight': 'bold bright_magenta',
            'info': 'black',
            'border': 'bright_blue'
        }
    
    def _get_blue_theme(self) -> Dict[str, str]:
        """Get blue theme colors."""
        return {
            'background': 'black',
            'text': 'white',
            'primary': 'bright_blue',
            'secondary': 'blue',
            'success': 'bright_green',
            'warning': 'bright_yellow',
            'error': 'bright_red',
            'muted': 'bright_black',
            'code': 'bright_white on bright_black',
            'title': 'bold bright_blue',
            'subtitle': 'bold blue',
            'highlight': 'bold bright_cyan',
            'info': 'white',
            'border': 'bright_blue'
        }
    
    def _get_green_theme(self) -> Dict[str, str]:
        """Get green theme colors."""
        return {
            'background': 'black',
            'text': 'white',
            'primary': 'bright_green',
            'secondary': 'green',
            'success': 'bright_green',
            'warning': 'bright_yellow',
            'error': 'bright_red',
            'muted': 'bright_black',
            'code': 'bright_white on bright_black',
            'title': 'bold bright_green',
            'subtitle': 'bold green',
            'highlight': 'bold bright_cyan',
            'info': 'white',
            'border': 'bright_green'
        }
    
    def get_theme(self, theme_name: str = None) -> Dict[str, str]:
        """Get theme colors."""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["dark"])
    
    def set_theme(self, theme_name: str):
        """Set the current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' not found. Available themes: {list(self.themes.keys())}")
    
    def get_available_themes(self) -> list:
        """Get list of available themes."""
        return list(self.themes.keys())
    
    def create_rich_theme(self, theme_name: str = None) -> Theme:
        """Create a Rich Theme object for the specified theme."""
        theme_colors = self.get_theme(theme_name)
        
        # Convert to Rich theme format
        rich_theme = Theme({
            "info": theme_colors['info'],
            "warning": theme_colors['warning'],
            "danger": theme_colors['error'],
            "success": theme_colors['success'],
            "primary": theme_colors['primary'],
            "secondary": theme_colors['secondary'],
            "muted": theme_colors['muted'],
            "title": theme_colors['title'],
            "subtitle": theme_colors['subtitle'],
            "highlight": theme_colors['highlight'],
            "code": theme_colors['code'],
            "border": theme_colors['border']
        })
        
        return rich_theme

class StyledConsole:
    """Console with theme-aware styling."""
    
    def __init__(self, theme_manager: ThemeManager = None):
        self.theme_manager = theme_manager or ThemeManager()
        self.console = Console(theme=self.theme_manager.create_rich_theme())
    
    def print_styled(self, text: str, style: str = 'info'):
        """Print text with theme-aware styling."""
        self.console.print(text, style=style)
    
    def print_title(self, text: str):
        """Print a styled title."""
        self.console.print(text, style="title")
    
    def print_subtitle(self, text: str):
        """Print a styled subtitle."""
        self.console.print(text, style="subtitle")
    
    def print_success(self, text: str):
        """Print success message."""
        self.console.print(text, style="success")
    
    def print_warning(self, text: str):
        """Print warning message."""
        self.console.print(text, style="warning")
    
    def print_error(self, text: str):
        """Print error message."""
        self.console.print(text, style="danger")
    
    def print_info(self, text: str):
        """Print info message."""
        self.console.print(text, style="info")
    
    def print_highlight(self, text: str):
        """Print highlighted text."""
        self.console.print(text, style="highlight")
    
    def print_code(self, text: str):
        """Print code with syntax highlighting."""
        self.console.print(text, style="code")
    
    def set_theme(self, theme_name: str):
        """Change the theme."""
        self.theme_manager.set_theme(theme_name)
        self.console = Console(theme=self.theme_manager.create_rich_theme())
    
    def get_console(self) -> Console:
        """Get the underlying console object."""
        return self.console

# Predefined styling functions
def create_styled_panel(content: str, title: str = None, border_style: str = "cyan", padding: tuple = (1, 2)):
    """Create a styled panel with consistent formatting."""
    from rich.panel import Panel
    return Panel(content, title=title, border_style=border_style, padding=padding)

def create_styled_table(title: str = None, show_header: bool = True):
    """Create a styled table with consistent formatting."""
    from rich.table import Table
    table = Table(title=title, show_header=show_header)
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    return table

def create_progress_bar(description: str, total: int = 100):
    """Create a styled progress bar."""
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        expand=True
    )

# Theme presets for common use cases
THEME_PRESETS = {
    "professional": "dark",
    "light_mode": "light",
    "accessible": "high_contrast",
    "modern": "blue",
    "nature": "green"
} 