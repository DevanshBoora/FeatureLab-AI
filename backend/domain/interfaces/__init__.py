from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities import Workspace, User, Dataset, Job, Experiment, Artifact

class IWorkspaceRepository(ABC):
    @abstractmethod
    def create(self, workspace: Workspace) -> Workspace:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Workspace]:
        pass

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass
        
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[User]:
        pass

class IDatasetRepository(ABC):
    @abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        pass
        
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Dataset]:
        pass

    @abstractmethod
    def update(self, dataset: Dataset) -> Dataset:
        pass

    @abstractmethod
    def list_by_workspace(self, workspace_id: UUID) -> List[Dataset]:
        pass

class IJobRepository(ABC):
    @abstractmethod
    def create(self, job: Job) -> Job:
        pass
        
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Job]:
        pass
        
    @abstractmethod
    def update(self, job: Job) -> Job:
        pass

    @abstractmethod
    def list_by_workspace(self, workspace_id: UUID) -> List[Job]:
        pass

class IExperimentRepository(ABC):
    @abstractmethod
    def create(self, experiment: Experiment) -> Experiment:
        pass
        
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Experiment]:
        pass
        
    @abstractmethod
    def list_by_dataset(self, dataset_id: UUID) -> List[Experiment]:
        pass

class IArtifactRepository(ABC):
    @abstractmethod
    def create(self, artifact: Artifact) -> Artifact:
        pass
        
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Artifact]:
        pass
        
    @abstractmethod
    def list_by_experiment(self, experiment_id: UUID) -> List[Artifact]:
        pass
