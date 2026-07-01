from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class WorkspaceCreate(BaseModel):
    name: str

class DatasetCreate(BaseModel):
    workspace_id: UUID
    name: str
    description: Optional[str] = None
    file_path: str
    file_size_bytes: int

class JobCreate(BaseModel):
    workspace_id: UUID
    dataset_id: Optional[UUID] = None
    experiment_id: Optional[UUID] = None
    task_type: str
