from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from repositories.sql_repositories import (
    WorkspaceRepository, UserRepository, DatasetRepository,
    JobRepository, ExperimentRepository, ArtifactRepository
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_workspace_repo(db: Session = Depends(get_db)) -> WorkspaceRepository:
    return WorkspaceRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_dataset_repo(db: Session = Depends(get_db)) -> DatasetRepository:
    return DatasetRepository(db)

def get_job_repo(db: Session = Depends(get_db)) -> JobRepository:
    return JobRepository(db)

def get_experiment_repo(db: Session = Depends(get_db)) -> ExperimentRepository:
    return ExperimentRepository(db)

def get_artifact_repo(db: Session = Depends(get_db)) -> ArtifactRepository:
    return ArtifactRepository(db)
