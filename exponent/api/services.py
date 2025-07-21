"""
Service layer for Exponent API Backend
"""

import os
import json
import threading
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid

from .models import TrainingJob, DeploymentJob, Project, JobStatus, ModelType

class TrainingService:
    """Service for managing training jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, TrainingJob] = {}
        self.job_threads: Dict[str, threading.Thread] = {}
    
    def create_job(self, project_id: str, dataset_path: str, model_type: ModelType, 
                   hyperparameters: Dict[str, Any] = None) -> TrainingJob:
        """Create a new training job"""
        job = TrainingJob(
            project_id=project_id,
            dataset_path=dataset_path,
            model_type=model_type,
            hyperparameters=hyperparameters or {}
        )
        
        self.jobs[job.job_id] = job
        
        # Start training in background thread
        thread = threading.Thread(target=self._run_training_job, args=(job.job_id,))
        thread.daemon = True
        thread.start()
        self.job_threads[job.job_id] = thread
        
        return job
    
    def get_job(self, job_id: str) -> Optional[TrainingJob]:
        """Get a training job by ID"""
        return self.jobs.get(job_id)
    
    def get_job_logs(self, job_id: str) -> Optional[List[str]]:
        """Get logs for a training job"""
        job = self.get_job(job_id)
        return job.logs if job else None
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a training job"""
        job = self.get_job(job_id)
        if job and job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
            job.status = JobStatus.CANCELLED
            return True
        return False
    
    def list_jobs(self) -> List[TrainingJob]:
        """List all training jobs"""
        return list(self.jobs.values())
    
    def _run_training_job(self, job_id: str):
        """Run a training job in background"""
        job = self.get_job(job_id)
        if not job:
            return
        
        try:
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            job.logs.append(f"Starting training job {job_id}")
            
            # Simulate training process
            self._simulate_training(job)
            
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.logs.append(f"Training completed successfully")
            job.model_path = f"models/{job_id}/model.pkl"
            job.metrics = {
                "accuracy": 0.85,
                "precision": 0.83,
                "recall": 0.87,
                "f1_score": 0.85
            }
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.logs.append(f"Training failed: {str(e)}")
    
    def _simulate_training(self, job: TrainingJob):
        """Simulate training process"""
        steps = [
            "Loading dataset...",
            "Preprocessing data...",
            "Initializing model...",
            "Training model...",
            "Evaluating model...",
            "Saving model..."
        ]
        
        for i, step in enumerate(steps):
            time.sleep(2)  # Simulate processing time
            job.logs.append(f"Step {i+1}: {step}")
            
            # Update progress
            progress = (i + 1) / len(steps)
            job.metrics["progress"] = progress

class DeploymentService:
    """Service for managing deployment jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, DeploymentJob] = {}
        self.job_threads: Dict[str, threading.Thread] = {}
    
    def create_job(self, project_id: str, model_path: str, deployment_type: str) -> DeploymentJob:
        """Create a new deployment job"""
        job = DeploymentJob(
            project_id=project_id,
            model_path=model_path,
            deployment_type=deployment_type
        )
        
        self.jobs[job.deployment_id] = job
        
        # Start deployment in background thread
        thread = threading.Thread(target=self._run_deployment_job, args=(job.deployment_id,))
        thread.daemon = True
        thread.start()
        self.job_threads[job.deployment_id] = thread
        
        return job
    
    def get_job(self, deployment_id: str) -> Optional[DeploymentJob]:
        """Get a deployment job by ID"""
        return self.jobs.get(deployment_id)
    
    def cancel_job(self, deployment_id: str) -> bool:
        """Cancel a deployment job"""
        job = self.get_job(deployment_id)
        if job and job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
            job.status = JobStatus.CANCELLED
            return True
        return False
    
    def list_jobs(self) -> List[DeploymentJob]:
        """List all deployment jobs"""
        return list(self.jobs.values())
    
    def _run_deployment_job(self, deployment_id: str):
        """Run a deployment job in background"""
        job = self.get_job(deployment_id)
        if not job:
            return
        
        try:
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            
            # Simulate deployment process
            time.sleep(3)  # Simulate processing time
            
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.endpoint_url = f"https://api.exponent.ai/models/{deployment_id}"
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)

class ProjectService:
    """Service for managing projects"""
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self._load_projects()
    
    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            description=description
        )
        
        self.projects[project.project_id] = project
        self._save_projects()
        
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID"""
        return self.projects.get(project_id)
    
    def update_project(self, project_id: str, name: str = None, description: str = None) -> Optional[Project]:
        """Update a project"""
        project = self.get_project(project_id)
        if not project:
            return None
        
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        
        self._save_projects()
        return project
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id in self.projects:
            del self.projects[project_id]
            self._save_projects()
            return True
        return False
    
    def list_projects(self) -> List[Project]:
        """List all projects"""
        return list(self.projects.values())
    
    def _load_projects(self):
        """Load projects from storage"""
        storage_file = Path.home() / ".exponent" / "projects.json"
        if storage_file.exists():
            try:
                with open(storage_file, 'r') as f:
                    data = json.load(f)
                    for project_data in data:
                        project = Project(
                            project_id=project_data['project_id'],
                            name=project_data['name'],
                            description=project_data['description'],
                            created_at=datetime.fromisoformat(project_data['created_at']),
                            datasets=project_data.get('datasets', []),
                            models=project_data.get('models', []),
                            deployments=project_data.get('deployments', [])
                        )
                        self.projects[project.project_id] = project
            except Exception as e:
                print(f"Error loading projects: {e}")
    
    def _save_projects(self):
        """Save projects to storage"""
        storage_file = Path.home() / ".exponent" / "projects.json"
        storage_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(storage_file, 'w') as f:
                json.dump([project.to_dict() for project in self.projects.values()], f, indent=2)
        except Exception as e:
            print(f"Error saving projects: {e}") 