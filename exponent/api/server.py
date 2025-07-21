"""
Flask server for Exponent API Backend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from pathlib import Path

from .endpoints import training_endpoints, deployment_endpoints, project_endpoints

class ExponentAPIServer:
    """Flask server for Exponent API Backend"""
    
    def __init__(self, host='0.0.0.0', port=5000, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.app = self._create_app()
    
    def _create_app(self) -> Flask:
        """Create and configure Flask app"""
        app = Flask(__name__)
        
        # Enable CORS
        CORS(app)
        
        # Register blueprints
        app.register_blueprint(training_endpoints)
        app.register_blueprint(deployment_endpoints)
        app.register_blueprint(project_endpoints)
        
        # Root endpoint
        @app.route('/')
        def root():
            return jsonify({
                'success': True,
                'message': 'Exponent API Backend',
                'version': '1.0.0',
                'endpoints': {
                    'training': '/api/v1/training',
                    'deployment': '/api/v1/deployment',
                    'projects': '/api/v1/projects'
                }
            })
        
        # Health check endpoint
        @app.route('/health')
        def health():
            return jsonify({
                'success': True,
                'status': 'healthy',
                'service': 'exponent-api'
            })
        
        # Error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Endpoint not found'}), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500
        
        return app
    
    def run(self):
        """Run the Flask server"""
        print(f"🚀 Starting Exponent API Server on {self.host}:{self.port}")
        print(f"📊 API Documentation: http://{self.host}:{self.port}/")
        print(f"🏥 Health Check: http://{self.host}:{self.port}/health")
        
        self.app.run(
            host=self.host,
            port=self.port,
            debug=self.debug
        )

def create_app():
    """Factory function to create Flask app"""
    server = ExponentAPIServer()
    return server.app

if __name__ == '__main__':
    server = ExponentAPIServer()
    server.run() 