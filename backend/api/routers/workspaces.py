from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from datetime import datetime
import uuid
from api.deps import get_workspace_repo
from repositories.sql_repositories import WorkspaceRepository
from schemas.requests import WorkspaceCreate
from schemas.responses import WorkspaceResponse
from domain.entities import Workspace

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("/", response_model=WorkspaceResponse)
def create_workspace(
    request: WorkspaceCreate,
    repo: WorkspaceRepository = Depends(get_workspace_repo)
):
    now = datetime.utcnow()
    workspace = Workspace(
        id=uuid.uuid4(),
        name=request.name,
        created_at=now,
        updated_at=now
    )
    created = repo.create(workspace)
    return created

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: UUID,
    repo: WorkspaceRepository = Depends(get_workspace_repo)
):
    workspace = repo.get_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace
