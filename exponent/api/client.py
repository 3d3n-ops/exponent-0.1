"""
Client library for Exponent API Backend
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

class ExponentAPIClient:
    """Client for communicating with Exponent API Backend"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Exponent-CLI/1.0.0'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    # Training endpoints
    def create_training_job(self, project_id: str, dataset_path: str, model_type: str, 
                           hyperparameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new training job"""
        data = {
            'project_id': project_id,
            'dataset_path': dataset_path,
            'model_type': model_type,
            'hyperparameters': hyperparameters or {}
        }
        
        return self._make_request('POST', '/api/v1/training/jobs', data)
    
    def get_training_job(self, job_id: str) -> Dict[str, Any]:
        """Get training job status"""
        return self._make_request('GET', f'/api/v1/training/jobs/{job_id}')
    
    def get_training_logs(self, job_id: str) -> Dict[str, Any]:
        """Get training job logs"""
        return self._make_request('GET', f'/api/v1/training/jobs/{job_id}/logs')
    
    def cancel_training_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a training job"""
        return self._make_request('POST', f'/api/v1/training/jobs/{job_id}/cancel')
    
    def list_training_jobs(self) -> Dict[str, Any]:
        """List all training jobs"""
        return self._make_request('GET', '/api/v1/training/jobs')
    
    # Deployment endpoints
    def create_deployment_job(self, project_id: str, model_path: str, deployment_type: str) -> Dict[str, Any]:
        """Create a new deployment job"""
        data = {
            'project_id': project_id,
            'model_path': model_path,
            'deployment_type': deployment_type
        }
        
        return self._make_request('POST', '/api/v1/deployment/jobs', data)
    
    def get_deployment_job(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment job status"""
        return self._make_request('GET', f'/api/v1/deployment/jobs/{deployment_id}')
    
    def cancel_deployment_job(self, deployment_id: str) -> Dict[str, Any]:
        """Cancel a deployment job"""
        return self._make_request('POST', f'/api/v1/deployment/jobs/{deployment_id}/cancel')
    
    def list_deployment_jobs(self) -> Dict[str, Any]:
        """List all deployment jobs"""
        return self._make_request('GET', '/api/v1/deployment/jobs')
    
    # Project endpoints
    def create_project(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new project"""
        data = {
            'name': name,
            'description': description
        }
        
        return self._make_request('POST', '/api/v1/projects/projects', data)
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details"""
        return self._make_request('GET', f'/api/v1/projects/projects/{project_id}')
    
    def update_project(self, project_id: str, name: str = None, description: str = None) -> Dict[str, Any]:
        """Update project details"""
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        
        return self._make_request('PUT', f'/api/v1/projects/projects/{project_id}', data)
    
    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project"""
        return self._make_request('DELETE', f'/api/v1/projects/projects/{project_id}')
    
    def list_projects(self) -> Dict[str, Any]:
        """List all projects"""
        return self._make_request('GET', '/api/v1/projects/projects')
    
    # Utility methods
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._make_request('GET', '/health')
    
    def wait_for_job_completion(self, job_id: str, job_type: str = 'training', 
                               timeout: int = 3600, check_interval: int = 5) -> Dict[str, Any]:
        """Wait for job completion with timeout"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if job_type == 'training':
                response = self.get_training_job(job_id)
            else:
                response = self.get_deployment_job(job_id)
            
            if response.get('success'):
                job = response.get('job', {})
                status = job.get('status')
                
                if status in ['completed', 'failed', 'cancelled']:
                    return response
                
                print(f"Job {job_id} status: {status}")
                time.sleep(check_interval)
            else:
                raise Exception(f"Failed to get job status: {response.get('error')}")
        
        raise Exception(f"Job {job_id} timed out after {timeout} seconds")
    
    def upload_dataset(self, file_path: str) -> str:
        """Upload dataset to API (placeholder for future implementation)"""
        # This would be implemented when we add file upload endpoints
        return file_path
    
    def download_model(self, model_path: str, local_path: str):
        """Download trained model (placeholder for future implementation)"""
        # This would be implemented when we add file download endpoints
        print(f"Model would be downloaded from {model_path} to {local_path}") 