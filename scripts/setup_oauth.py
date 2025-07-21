#!/usr/bin/env python3
"""
OAuth Setup Script for Exponent-ML

This script helps you set up OAuth credentials for Google and GitHub authentication.
"""

import os
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def google():
    """Set up Google OAuth credentials"""
    typer.echo("🔧 Setting up Google OAuth credentials...")
    typer.echo("\n📋 Steps to get Google OAuth credentials:")
    typer.echo("1. Go to https://console.developers.google.com/")
    typer.echo("2. Create a new project or select an existing one")
    typer.echo("3. Enable the Google+ API")
    typer.echo("4. Go to 'Credentials' and create an OAuth 2.0 Client ID")
    typer.echo("5. Set the redirect URI to: http://localhost:8080")
    typer.echo("6. Copy the Client ID and Client Secret")
    
    client_id = typer.prompt("Enter your Google Client ID")
    client_secret = typer.prompt("Enter your Google Client Secret", hide_input=True)
    
    # Add to .env file
    env_file = Path.cwd() / ".env"
    env_content = ""
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Remove existing Google credentials if they exist
    lines = env_content.split('\n')
    lines = [line for line in lines if not line.startswith('GOOGLE_CLIENT_ID=') and not line.startswith('GOOGLE_CLIENT_SECRET=')]
    
    # Add new credentials
    lines.extend([
        f"GOOGLE_CLIENT_ID={client_id}",
        f"GOOGLE_CLIENT_SECRET={client_secret}"
    ])
    
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))
    
    typer.echo("✅ Google OAuth credentials saved to .env file!")

@app.command()
def github():
    """Set up GitHub OAuth credentials"""
    typer.echo("🔧 Setting up GitHub OAuth credentials...")
    typer.echo("\n📋 Steps to get GitHub OAuth credentials:")
    typer.echo("1. Go to https://github.com/settings/developers")
    typer.echo("2. Click 'New OAuth App'")
    typer.echo("3. Fill in the application details:")
    typer.echo("   - Application name: Exponent-ML")
    typer.echo("   - Homepage URL: https://github.com/yourusername/exponent-ml")
    typer.echo("   - Authorization callback URL: http://localhost:8080")
    typer.echo("4. Copy the Client ID and Client Secret")
    
    client_id = typer.prompt("Enter your GitHub Client ID")
    client_secret = typer.prompt("Enter your GitHub Client Secret", hide_input=True)
    
    # Add to .env file
    env_file = Path.cwd() / ".env"
    env_content = ""
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Remove existing GitHub credentials if they exist
    lines = env_content.split('\n')
    lines = [line for line in lines if not line.startswith('GITHUB_CLIENT_ID=') and not line.startswith('GITHUB_CLIENT_SECRET=')]
    
    # Add new credentials
    lines.extend([
        f"GITHUB_CLIENT_ID={client_id}",
        f"GITHUB_CLIENT_SECRET={client_secret}"
    ])
    
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))
    
    typer.echo("✅ GitHub OAuth credentials saved to .env file!")

@app.command()
def check():
    """Check current OAuth configuration"""
    typer.echo("🔍 Checking OAuth configuration...")
    
    google_id = os.getenv("GOOGLE_CLIENT_ID")
    google_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    github_id = os.getenv("GITHUB_CLIENT_ID")
    github_secret = os.getenv("GITHUB_CLIENT_SECRET")
    
    if google_id and google_secret:
        typer.echo("✅ Google OAuth configured")
    else:
        typer.echo("❌ Google OAuth not configured")
    
    if github_id and github_secret:
        typer.echo("✅ GitHub OAuth configured")
    else:
        typer.echo("❌ GitHub OAuth not configured")
    
    if not (google_id or github_id):
        typer.echo("\n💡 No OAuth providers configured!")
        typer.echo("Run 'python scripts/setup_oauth.py google' or 'python scripts/setup_oauth.py github' to set up authentication.")

if __name__ == "__main__":
    app() 