from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class Workspace(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    id: UUID
    email: str
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

class Dataset(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    description: Optional[str] = None
    file_path: str  # Path in Supabase storage
    file_size_bytes: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    profile_data: Optional[Dict[str, Any]] = None # Pre-computed profiling metrics
    created_at: datetime
    updated_at: datetime

class JobStatus:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Job(BaseModel):
    id: UUID
    workspace_id: UUID
    dataset_id: Optional[UUID] = None
    experiment_id: Optional[UUID] = None
    status: str = Field(default=JobStatus.QUEUED)
    progress: float = Field(default=0.0)
    task_type: str  # e.g., "profiling", "pipeline_execution"
    logs: List[Dict[str, Any]] = Field(default_factory=list)
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

class Experiment(BaseModel):
    id: UUID
    workspace_id: UUID
    dataset_id: UUID
    job_id: UUID
    name: str
    task_type: str # "classification" or "regression"
    configuration: Dict[str, Any]
    metrics: Optional[Dict[str, Any]] = None
    best_model_name: Optional[str] = None
    runtime_seconds: Optional[float] = None
    created_at: datetime

class Artifact(BaseModel):
    id: UUID
    workspace_id: UUID
    experiment_id: UUID
    name: str
    artifact_type: str # "model", "explainability", "report", "cleaned_dataset"
    file_path: str # Path in Supabase storage
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
