from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from typing import List
from uuid import UUID
from datetime import datetime
import uuid
from api.deps import get_dataset_repo, get_workspace_repo
from repositories.sql_repositories import DatasetRepository, WorkspaceRepository
from schemas.responses import DatasetResponse
from domain.entities import Dataset
from services.storage import StorageService
from ml_engine.profiler import DatasetProfiler

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/", response_model=DatasetResponse)
async def upload_dataset(
    workspace_id: UUID = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    repo: DatasetRepository = Depends(get_dataset_repo),
    ws_repo: WorkspaceRepository = Depends(get_workspace_repo)
):
    ws = ws_repo.get_by_id(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    file_bytes = await file.read()
    file_size_bytes = len(file_bytes)
    
    # Profile dataset
    try:
        profile_data = DatasetProfiler.profile(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to profile CSV: {str(e)}")
        
    dataset_id = uuid.uuid4()
    file_path = f"{workspace_id}/{dataset_id}_{file.filename}"
    
    # Upload to storage
    storage = StorageService()
    storage.upload_file(file_path, file_bytes)
        
    now = datetime.utcnow()
    dataset = Dataset(
        id=dataset_id,
        workspace_id=workspace_id,
        name=name,
        description=description,
        file_path=file_path,
        file_size_bytes=file_size_bytes,
        row_count=profile_data["row_count"],
        column_count=profile_data["column_count"],
        profile_data=profile_data,
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
