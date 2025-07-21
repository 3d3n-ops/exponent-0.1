"""
Data models for Exponent API Backend
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
import uuid

class JobStatus(Enum):
    """Job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ModelType(Enum):
    """Model type enumeration"""
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    IMAGE_CLASSIFICATION = "image_classification"
    TEXT_GENERATION = "text_generation"

@dataclass
class TrainingJob:
    """Training job model"""
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    dataset_path: str = ""
    model_type: ModelType = ModelType.SENTIMENT_ANALYSIS
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    logs: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    model_path: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_id": self.job_id,
            "project_id": self.project_id,
            "dataset_path": self.dataset_path,
            "model_type": self.model_type.value,
            "hyperparameters": self.hyperparameters,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "logs": self.logs,
            "metrics": self.metrics,
            "model_path": self.model_path,
            "error_message": self.error_message
        }

@dataclass
class DeploymentJob:
    """Deployment job model"""
    deployment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    model_path: str = ""
    deployment_type: str = "api"  # api, web, mobile
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    endpoint_url: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "deployment_id": self.deployment_id,
            "project_id": self.project_id,
            "model_path": self.model_path,
            "deployment_type": self.deployment_type,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "endpoint_url": self.endpoint_url,
            "error_message": self.error_message
        }

@dataclass
class Project:
    """Project model"""
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    datasets: List[str] = field(default_factory=list)
    models: List[str] = field(default_factory=list)
    deployments: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "datasets": self.datasets,
            "models": self.models,
            "deployments": self.deployments
        } 