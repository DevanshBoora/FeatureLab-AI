import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, JSON, Uuid
from core.database import Base

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("UserModel", back_populates="workspace")
    datasets = relationship("DatasetModel", back_populates="workspace")
    jobs = relationship("JobModel", back_populates="workspace")
    experiments = relationship("ExperimentModel", back_populates="workspace")
    artifacts = relationship("ArtifactModel", back_populates="workspace")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="users")


class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    profile_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="datasets")
    experiments = relationship("ExperimentModel", back_populates="dataset")
    jobs = relationship("JobModel", back_populates="dataset")


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    dataset_id = Column(Uuid(as_uuid=True), ForeignKey("datasets.id"), nullable=True)
    experiment_id = Column(Uuid(as_uuid=True), ForeignKey("experiments.id"), nullable=True)
    status = Column(String, default="QUEUED", nullable=False)
    progress = Column(Float, default=0.0)
    task_type = Column(String, nullable=False)
    logs = Column(JSON, default=list)
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="jobs")
    dataset = relationship("DatasetModel", back_populates="jobs")
    experiment = relationship("ExperimentModel", back_populates="jobs", foreign_keys="[JobModel.experiment_id]")


class ExperimentModel(Base):
    __tablename__ = "experiments"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    dataset_id = Column(Uuid(as_uuid=True), ForeignKey("datasets.id"), nullable=False)
    job_id = Column(Uuid(as_uuid=True), ForeignKey("jobs.id"), nullable=True)
    name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    configuration = Column(JSON, nullable=False)
    metrics = Column(JSON, nullable=True)
    best_model_name = Column(String, nullable=True)
    runtime_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="experiments")
    dataset = relationship("DatasetModel", back_populates="experiments")
    jobs = relationship("JobModel", back_populates="experiment", foreign_keys="[JobModel.experiment_id]")
    artifacts = relationship("ArtifactModel", back_populates="experiment")


class ArtifactModel(Base):
    __tablename__ = "artifacts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    experiment_id = Column(Uuid(as_uuid=True), ForeignKey("experiments.id"), nullable=False)
    name = Column(String, nullable=False)
    artifact_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="artifacts")
    experiment = relationship("ExperimentModel", back_populates="artifacts")
