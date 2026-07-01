from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from datetime import datetime
import uuid
from api.deps import get_dataset_repo, get_workspace_repo
from repositories.sql_repositories import DatasetRepository, WorkspaceRepository
from schemas.requests import DatasetCreate
from schemas.responses import DatasetResponse
from domain.entities import Dataset

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/", response_model=DatasetResponse)
def create_dataset(
    request: DatasetCreate,
    repo: DatasetRepository = Depends(get_dataset_repo),
    ws_repo: WorkspaceRepository = Depends(get_workspace_repo)
):
    ws = ws_repo.get_by_id(request.workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    now = datetime.utcnow()
    dataset = Dataset(
        id=uuid.uuid4(),
        workspace_id=request.workspace_id,
        name=request.name,
        description=request.description,
        file_path=request.file_path,
        file_size_bytes=request.file_size_bytes,
        created_at=now,
        updated_at=now
    )
    created = repo.create(dataset)
    return created

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: UUID,
    repo: DatasetRepository = Depends(get_dataset_repo)
):
    dataset = repo.get_by_id(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset
    
@router.get("/workspace/{workspace_id}", response_model=List[DatasetResponse])
def list_datasets(
    workspace_id: UUID,
    repo: DatasetRepository = Depends(get_dataset_repo)
):
    return repo.list_by_workspace(workspace_id)
