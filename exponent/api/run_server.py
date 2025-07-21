#!/usr/bin/env python3
"""
Server startup script for Exponent API Backend
"""

import sys
import argparse
from pathlib import Path

# Add the exponent package to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exponent.api.server import ExponentAPIServer

def main():
    """Main server startup function"""
    parser = argparse.ArgumentParser(description="Start Exponent API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("🚀 Starting Exponent API Server...")
    print(f"📊 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🐛 Debug: {args.debug}")
    
    server = ExponentAPIServer(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 