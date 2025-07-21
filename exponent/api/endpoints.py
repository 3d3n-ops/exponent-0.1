"""
API Endpoints for Exponent Backend
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import json
import os
from pathlib import Path

from .models import TrainingJob, DeploymentJob, Project, JobStatus, ModelType
from .services import TrainingService, DeploymentService, ProjectService

# Create blueprints
training_endpoints = Blueprint('training', __name__, url_prefix='/api/v1/training')
deployment_endpoints = Blueprint('deployment', __name__, url_prefix='/api/v1/deployment')
project_endpoints = Blueprint('projects', __name__, url_prefix='/api/v1/projects')

# Initialize services
training_service = TrainingService()
deployment_service = DeploymentService()
project_service = ProjectService()

# Training Endpoints
@training_endpoints.route('/jobs', methods=['POST'])
def create_training_job():
    """Create a new training job"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'dataset_path', 'model_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create training job
        job = training_service.create_job(
            project_id=data['project_id'],
            dataset_path=data['dataset_path'],
            model_type=ModelType(data['model_type']),
            hyperparameters=data.get('hyperparameters', {})
        )
        
        return jsonify({
            'success': True,
            'job': job.to_dict(),
            'message': 'Training job created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_endpoints.route('/jobs/<job_id>', methods=['GET'])
def get_training_job(job_id: str):
    """Get training job status"""
    try:
        job = training_service.get_job(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'success': True,
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_endpoints.route('/jobs/<job_id>/logs', methods=['GET'])
def get_training_logs(job_id: str):
    """Get training job logs"""
    try:
        logs = training_service.get_job_logs(job_id)
        if logs is None:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'success': True,
            'logs': logs
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_endpoints.route('/jobs/<job_id>/cancel', methods=['POST'])
def cancel_training_job(job_id: str):
    """Cancel a training job"""
    try:
        success = training_service.cancel_job(job_id)
        if not success:
            return jsonify({'error': 'Job not found or cannot be cancelled'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Training job cancelled successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_endpoints.route('/jobs', methods=['GET'])
def list_training_jobs():
    """List all training jobs"""
    try:
        jobs = training_service.list_jobs()
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Deployment Endpoints
@deployment_endpoints.route('/jobs', methods=['POST'])
def create_deployment_job():
    """Create a new deployment job"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'model_path', 'deployment_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create deployment job
        job = deployment_service.create_job(
            project_id=data['project_id'],
            model_path=data['model_path'],
            deployment_type=data['deployment_type']
        )
        
        return jsonify({
            'success': True,
            'job': job.to_dict(),
            'message': 'Deployment job created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deployment_endpoints.route('/jobs/<deployment_id>', methods=['GET'])
def get_deployment_job(deployment_id: str):
    """Get deployment job status"""
    try:
        job = deployment_service.get_job(deployment_id)
        if not job:
            return jsonify({'error': 'Deployment job not found'}), 404
        
        return jsonify({
            'success': True,
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deployment_endpoints.route('/jobs/<deployment_id>/cancel', methods=['POST'])
def cancel_deployment_job(deployment_id: str):
    """Cancel a deployment job"""
    try:
        success = deployment_service.cancel_job(deployment_id)
        if not success:
            return jsonify({'error': 'Deployment job not found or cannot be cancelled'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Deployment job cancelled successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deployment_endpoints.route('/jobs', methods=['GET'])
def list_deployment_jobs():
    """List all deployment jobs"""
    try:
        jobs = deployment_service.list_jobs()
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Project Endpoints
@project_endpoints.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data:
            return jsonify({'error': 'Missing required field: name'}), 400
        
        # Create project
        project = project_service.create_project(
            name=data['name'],
            description=data.get('description', '')
        )
        
        return jsonify({
            'success': True,
            'project': project.to_dict(),
            'message': 'Project created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_endpoints.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id: str):
    """Get project details"""
    try:
        project = project_service.get_project(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_endpoints.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id: str):
    """Update project details"""
    try:
        data = request.get_json()
        
        project = project_service.update_project(
            project_id=project_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'success': True,
            'project': project.to_dict(),
            'message': 'Project updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_endpoints.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id: str):
    """Delete a project"""
    try:
        success = project_service.delete_project(project_id)
        if not success:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_endpoints.route('/projects', methods=['GET'])
def list_projects():
    """List all projects"""
    try:
        projects = project_service.list_projects()
        return jsonify({
            'success': True,
            'projects': [project.to_dict() for project in projects]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health Check Endpoint
@training_endpoints.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'exponent-training-api'
    }), 200 