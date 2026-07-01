from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from domain.entities import Workspace, User, Dataset, Job, Experiment, Artifact
from domain.interfaces import (
    IWorkspaceRepository, IUserRepository, IDatasetRepository, 
    IJobRepository, IExperimentRepository, IArtifactRepository
)
from models.all_models import (
    WorkspaceModel, UserModel, DatasetModel, JobModel, ExperimentModel, ArtifactModel
)

class WorkspaceRepository(IWorkspaceRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, workspace: Workspace) -> Workspace:
        model = WorkspaceModel(**workspace.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return workspace

    def get_by_id(self, id: UUID) -> Optional[Workspace]:
        model = self.db.query(WorkspaceModel).filter(WorkspaceModel.id == id).first()
        if not model:
            return None
        return Workspace(**{k: getattr(model, k) for k in Workspace.model_fields.keys()})

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        model = UserModel(**user.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return user
        
    def get_by_id(self, id: UUID) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not model:
            return None
        return User(**{k: getattr(model, k) for k in User.model_fields.keys()})

class DatasetRepository(IDatasetRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, dataset: Dataset) -> Dataset:
        model = DatasetModel(**dataset.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return dataset
        
    def get_by_id(self, id: UUID) -> Optional[Dataset]:
        model = self.db.query(DatasetModel).filter(DatasetModel.id == id).first()
        if not model:
            return None
        return Dataset(**{k: getattr(model, k) for k in Dataset.model_fields.keys()})

    def update(self, dataset: Dataset) -> Dataset:
        model = self.db.query(DatasetModel).filter(DatasetModel.id == dataset.id).first()
        if model:
            for key in Dataset.model_fields.keys():
                setattr(model, key, getattr(dataset, key))
            self.db.commit()
            self.db.refresh(model)
        return dataset

    def list_by_workspace(self, workspace_id: UUID) -> List[Dataset]:
        models = self.db.query(DatasetModel).filter(DatasetModel.workspace_id == workspace_id).all()
        return [Dataset(**{k: getattr(m, k) for k in Dataset.model_fields.keys()}) for m in models]

class JobRepository(IJobRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job) -> Job:
        model = JobModel(**job.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return job
        
    def get_by_id(self, id: UUID) -> Optional[Job]:
        model = self.db.query(JobModel).filter(JobModel.id == id).first()
        if not model:
            return None
        return Job(**{k: getattr(model, k) for k in Job.model_fields.keys()})
        
    def update(self, job: Job) -> Job:
        model = self.db.query(JobModel).filter(JobModel.id == job.id).first()
        if model:
            for key in Job.model_fields.keys():
                setattr(model, key, getattr(job, key))
            self.db.commit()
            self.db.refresh(model)
        return job

    def list_by_workspace(self, workspace_id: UUID) -> List[Job]:
        models = self.db.query(JobModel).filter(JobModel.workspace_id == workspace_id).all()
        return [Job(**{k: getattr(m, k) for k in Job.model_fields.keys()}) for m in models]

class ExperimentRepository(IExperimentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, experiment: Experiment) -> Experiment:
        model = ExperimentModel(**experiment.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return experiment
        
    def get_by_id(self, id: UUID) -> Optional[Experiment]:
        model = self.db.query(ExperimentModel).filter(ExperimentModel.id == id).first()
        if not model:
            return None
        return Experiment(**{k: getattr(model, k) for k in Experiment.model_fields.keys()})
        
    def list_by_dataset(self, dataset_id: UUID) -> List[Experiment]:
        models = self.db.query(ExperimentModel).filter(ExperimentModel.dataset_id == dataset_id).all()
        return [Experiment(**{k: getattr(m, k) for k in Experiment.model_fields.keys()}) for m in models]

class ArtifactRepository(IArtifactRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, artifact: Artifact) -> Artifact:
        # Pydantic field is 'metadata' but SQLAlchemy field is 'metadata_json'
        dump = artifact.model_dump()
        metadata_json = dump.pop("metadata", None)
        model = ArtifactModel(**dump, metadata_json=metadata_json)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return artifact
        
    def get_by_id(self, id: UUID) -> Optional[Artifact]:
        model = self.db.query(ArtifactModel).filter(ArtifactModel.id == id).first()
        if not model:
            return None
        dump = {k: getattr(model, k) for k in Artifact.model_fields.keys() if k != "metadata"}
        dump["metadata"] = model.metadata_json
        return Artifact(**dump)
        
    def list_by_experiment(self, experiment_id: UUID) -> List[Artifact]:
        models = self.db.query(ArtifactModel).filter(ArtifactModel.experiment_id == experiment_id).all()
        result = []
        for model in models:
            dump = {k: getattr(model, k) for k in Artifact.model_fields.keys() if k != "metadata"}
            dump["metadata"] = model.metadata_json
            result.append(Artifact(**dump))
        return result
