import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    ANTHROPIC_API_KEY: str
    OPENROUTER_API_KEY: Optional[str] = None
    AGENT_MODEL: Optional[str] = None
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    CLERK_SECRET_KEY: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: Optional[str] = None
    MODAL_TOKEN_ID: Optional[str] = None
    MODAL_TOKEN_SECRET: Optional[str] = None
    # Production settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

def get_config() -> Config:
    """Load configuration from environment variables, .env file, and setup config."""
    # Load from .env file if it exists
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    # Load setup configuration
    setup_config = load_setup_config()
    
    # Get required API key (prefer OpenRouter if available)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openrouter_key = setup_config.get('openrouter_api_key') if setup_config else None
    agent_model = setup_config.get('agent_model') if setup_config else None
    
    # Production settings
    debug = os.getenv("DEBUG", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO")
    api_timeout = int(os.getenv("API_TIMEOUT", "30"))
    max_retries = int(os.getenv("MAX_RETRIES", "3"))
    
    # If OpenRouter is configured, use it as primary
    if openrouter_key and agent_model:
        return Config(
            ANTHROPIC_API_KEY=anthropic_key or "not_used",  # Keep for backward compatibility
            OPENROUTER_API_KEY=openrouter_key,
            AGENT_MODEL=agent_model,
            CLERK_PUBLISHABLE_KEY=os.getenv("CLERK_PUBLISHABLE_KEY"),
            CLERK_SECRET_KEY=os.getenv("CLERK_SECRET_KEY"),
            AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID"),
            AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY"),
            AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
            S3_BUCKET=os.getenv("S3_BUCKET"),
            MODAL_TOKEN_ID=os.getenv("MODAL_TOKEN_ID"),
            MODAL_TOKEN_SECRET=os.getenv("MODAL_TOKEN_SECRET"),
            DEBUG=debug,
            LOG_LEVEL=log_level,
            API_TIMEOUT=api_timeout,
            MAX_RETRIES=max_retries,
        )
    else:
        # Fall back to Anthropic if no OpenRouter setup
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required (or run 'exponent setup' to configure OpenRouter)")
        
        return Config(
            ANTHROPIC_API_KEY=anthropic_key,
            CLERK_PUBLISHABLE_KEY=os.getenv("CLERK_PUBLISHABLE_KEY"),
            CLERK_SECRET_KEY=os.getenv("CLERK_SECRET_KEY"),
            AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID"),
            AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY"),
            AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
            S3_BUCKET=os.getenv("S3_BUCKET"),
            MODAL_TOKEN_ID=os.getenv("MODAL_TOKEN_ID"),
            MODAL_TOKEN_SECRET=os.getenv("MODAL_TOKEN_SECRET"),
            DEBUG=debug,
            LOG_LEVEL=log_level,
            API_TIMEOUT=api_timeout,
            MAX_RETRIES=max_retries,
        )

def load_setup_config() -> Optional[dict]:
    """Load setup configuration from file."""
    config_file = Path.home() / ".exponent" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    return None

def check_optional_services() -> dict:
    """Check which optional services are configured."""
    config = get_config()
    setup_config = load_setup_config()
    
    services = {
        "openrouter": bool(config.OPENROUTER_API_KEY and config.AGENT_MODEL),
        "anthropic": bool(config.ANTHROPIC_API_KEY and config.ANTHROPIC_API_KEY != "not_used"),
        "s3": bool(config.AWS_ACCESS_KEY_ID and config.AWS_SECRET_ACCESS_KEY and config.S3_BUCKET),
        "modal": bool(config.MODAL_TOKEN_ID and config.MODAL_TOKEN_SECRET),
        "github": bool(os.getenv("GITHUB_TOKEN")),
        "setup_complete": bool(setup_config and setup_config.get('setup_completed', False))
    }
    
    return services
