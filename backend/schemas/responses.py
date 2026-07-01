from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DatasetResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    description: Optional[str] = None
    file_path: str
    file_size_bytes: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    profile_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    dataset_id: Optional[UUID] = None
    experiment_id: Optional[UUID] = None
    status: str
    progress: float
    task_type: str
    logs: List[Dict[str, Any]]
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
