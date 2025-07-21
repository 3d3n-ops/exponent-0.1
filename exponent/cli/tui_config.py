"""
TUI Configuration for Exponent CLI

This module provides configuration options for customizing the TUI appearance
and behavior.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class TUISettings:
    """TUI configuration settings."""
    
    # Theme settings
    theme: str = "dark"
    enable_colors: bool = True
    enable_unicode: bool = True
    
    # Layout settings
    layout_mode: str = "auto"  # auto, compact, standard, wide
    show_sidebar: bool = True
    show_progress: bool = True
    show_typing_indicators: bool = True
    
    # Chat settings
    max_messages: int = 50
    message_timestamps: bool = True
    code_syntax_highlighting: bool = True
    markdown_rendering: bool = True
    
    # Animation settings
    enable_animations: bool = True
    animation_speed: float = 0.1
    spinner_type: str = "dots"
    
    # Accessibility settings
    high_contrast: bool = False
    large_text: bool = False
    screen_reader_friendly: bool = False
    
    # Custom colors (optional overrides)
    custom_colors: Optional[Dict[str, str]] = None

class TUIConfig:
    """Manages TUI configuration settings."""
    
    def __init__(self, config_file: Optional[Path] = None):
        if config_file is None:
            config_file = Path.home() / ".exponent" / "tui_config.json"
        
        self.config_file = config_file
        self.config_file.parent.mkdir(exist_ok=True)
        self.settings = self.load_settings()
    
    def load_settings(self) -> TUISettings:
        """Load settings from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return TUISettings(**data)
            except Exception as e:
                print(f"Warning: Could not load TUI config: {e}")
                return TUISettings()
        else:
            # Create default settings
            settings = TUISettings()
            self.save_settings(settings)
            return settings
    
    def save_settings(self, settings: TUISettings):
        """Save settings to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(asdict(settings), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save TUI config: {e}")
    
    def update_setting(self, key: str, value: Any):
        """Update a specific setting."""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save_settings(self.settings)
        else:
            raise ValueError(f"Unknown setting: {key}")
    
    def get_setting(self, key: str) -> Any:
        """Get a specific setting."""
        return getattr(self.settings, key, None)
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = TUISettings()
        self.save_settings(self.settings)
    
    def export_settings(self, file_path: Path):
        """Export settings to a file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(asdict(self.settings), f, indent=2)
        except Exception as e:
            print(f"Error exporting settings: {e}")
    
    def import_settings(self, file_path: Path):
        """Import settings from a file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.settings = TUISettings(**data)
                self.save_settings(self.settings)
        except Exception as e:
            print(f"Error importing settings: {e}")

# Predefined theme configurations
THEME_PRESETS = {
    "professional": {
        "theme": "dark",
        "enable_colors": True,
        "show_sidebar": True,
        "show_progress": True,
        "animation_speed": 0.1
    },
    "minimal": {
        "theme": "light",
        "enable_colors": True,
        "show_sidebar": False,
        "show_progress": False,
        "animation_speed": 0.05
    },
    "accessible": {
        "theme": "high_contrast",
        "enable_colors": True,
        "high_contrast": True,
        "large_text": True,
        "screen_reader_friendly": True
    },
    "developer": {
        "theme": "dark",
        "enable_colors": True,
        "show_sidebar": True,
        "code_syntax_highlighting": True,
        "markdown_rendering": True,
        "animation_speed": 0.05
    }
}

def apply_theme_preset(config: TUIConfig, preset_name: str):
    """Apply a predefined theme preset."""
    if preset_name in THEME_PRESETS:
        preset = THEME_PRESETS[preset_name]
        for key, value in preset.items():
            config.update_setting(key, value)
        return True
    else:
        raise ValueError(f"Unknown preset: {preset_name}. Available: {list(THEME_PRESETS.keys())}")

# Utility functions for TUI configuration
def detect_terminal_capabilities() -> Dict[str, bool]:
    """Detect terminal capabilities."""
    import shutil
    import os
    
    capabilities = {
        "supports_color": True,  # Assume True for modern terminals
        "supports_unicode": True,
        "is_interactive": os.stdout.isatty(),
        "has_gui": "DISPLAY" in os.environ or "TERM_PROGRAM" in os.environ
    }
    
    # Check terminal size
    try:
        width, height = shutil.get_terminal_size()
        capabilities["width"] = width
        capabilities["height"] = height
        capabilities["is_small_terminal"] = width < 80
    except:
        capabilities["width"] = 80
        capabilities["height"] = 24
        capabilities["is_small_terminal"] = True
    
    return capabilities

def auto_configure_tui(config: TUIConfig):
    """Automatically configure TUI based on terminal capabilities."""
    capabilities = detect_terminal_capabilities()
    
    # Auto-adjust settings based on terminal capabilities
    if capabilities.get("is_small_terminal", False):
        config.update_setting("layout_mode", "compact")
        config.update_setting("show_sidebar", False)
    
    if not capabilities.get("supports_color", True):
        config.update_setting("enable_colors", False)
    
    if not capabilities.get("supports_unicode", True):
        config.update_setting("enable_unicode", False)
        config.update_setting("spinner_type", "dots")

def create_tui_config_wizard():
    """Interactive wizard for configuring TUI settings."""
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    
    console = Console()
    config = TUIConfig()
    
    console.print("[bold cyan]🎨 Exponent CLI - TUI Configuration Wizard[/bold cyan]")
    console.print("=" * 60)
    
    # Show current settings
    console.print("\n[bold]Current Settings:[/bold]")
    table = Table()
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in asdict(config.settings).items():
        table.add_row(key, str(value))
    
    console.print(table)
    
    # Theme selection
    console.print("\n[bold]Theme Selection:[/bold]")
    themes = ["dark", "light", "high_contrast", "blue", "green"]
    for i, theme in enumerate(themes, 1):
        console.print(f"{i}. {theme}")
    
    theme_choice = Prompt.ask("Choose theme", choices=["1", "2", "3", "4", "5"])
    config.update_setting("theme", themes[int(theme_choice) - 1])
    
    # Layout preferences
    console.print("\n[bold]Layout Preferences:[/bold]")
    config.update_setting("show_sidebar", Confirm.ask("Show sidebar?"))
    config.update_setting("show_progress", Confirm.ask("Show progress indicators?"))
    config.update_setting("show_typing_indicators", Confirm.ask("Show typing indicators?"))
    
    # Animation preferences
    console.print("\n[bold]Animation Preferences:[/bold]")
    config.update_setting("enable_animations", Confirm.ask("Enable animations?"))
    
    if config.get_setting("enable_animations"):
        speed = Prompt.ask("Animation speed", choices=["fast", "normal", "slow"])
        speed_map = {"fast": 0.05, "normal": 0.1, "slow": 0.2}
        config.update_setting("animation_speed", speed_map[speed])
    
    # Accessibility options
    console.print("\n[bold]Accessibility Options:[/bold]")
    config.update_setting("high_contrast", Confirm.ask("Use high contrast?"))
    config.update_setting("large_text", Confirm.ask("Use large text?"))
    config.update_setting("screen_reader_friendly", Confirm.ask("Screen reader friendly?"))
    
    # Save settings
    config.save_settings(config.settings)
    console.print("\n[bold green]✅ TUI configuration saved![/bold green]")
    
    return config

if __name__ == "__main__":
    # Run configuration wizard
    create_tui_config_wizard() 