from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from uuid import UUID
from datetime import datetime
import uuid
from api.deps import get_job_repo, get_dataset_repo, get_workspace_repo
from repositories.sql_repositories import JobRepository, DatasetRepository, WorkspaceRepository
from schemas.requests import JobCreate
from schemas.responses import JobResponse
from domain.entities import Job
from services.jobs import JobManager

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse)
def submit_job(
    request: JobCreate,
    background_tasks: BackgroundTasks,
    job_repo: JobRepository = Depends(get_job_repo),
    dataset_repo: DatasetRepository = Depends(get_dataset_repo),
    ws_repo: WorkspaceRepository = Depends(get_workspace_repo)
):
    ws = ws_repo.get_by_id(request.workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    if request.dataset_id:
        ds = dataset_repo.get_by_id(request.dataset_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
    now = datetime.utcnow()
    job = Job(
        id=uuid.uuid4(),
        workspace_id=request.workspace_id,
        dataset_id=request.dataset_id,
        experiment_id=request.experiment_id,
        task_type=request.task_type,
        created_at=now
    )
    created_job = job_repo.create(job)
    
    # We need to run the ML task in the background.
    # To pass a db session, we can write a tiny wrapper that creates one.
    target_column = request.configuration.get("target_column") if hasattr(request, "configuration") else None
    user_config = request.configuration if hasattr(request, "configuration") else {}
    
    # If this is a training task, trigger the pipeline
    if request.task_type == "training" and target_column:
        manager = JobManager(job_repo, background_tasks)
        
        async def task_wrapper(job_id, ds_id, ws_id, target, config):
            from core.database import SessionLocal
            db = SessionLocal()
            try:
                from ml_engine.manager import ml_pipeline_task
                await ml_pipeline_task(job_id, ds_id, ws_id, target, config, db)
            finally:
                db.close()
                
        manager.execute_job(
            created_job.id, 
            task_wrapper, 
            request.dataset_id, 
            request.workspace_id, 
            target_column, 
            user_config
        )
    
    return created_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(
    job_id: UUID,
    job_repo: JobRepository = Depends(get_job_repo)
):
    job = job_repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/workspace/{workspace_id}", response_model=list[JobResponse])
def list_jobs_by_workspace(
    workspace_id: UUID,
    job_repo: JobRepository = Depends(get_job_repo)
):
    jobs = job_repo.list_by_workspace(workspace_id)
    return jobs
