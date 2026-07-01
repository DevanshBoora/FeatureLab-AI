from fastapi import BackgroundTasks
from uuid import UUID
from datetime import datetime
from domain.entities import Job, JobStatus
from repositories.sql_repositories import JobRepository
from utils.logger import logger
import traceback

class JobManager:
    def __init__(self, job_repo: JobRepository, background_tasks: BackgroundTasks):
        self.job_repo = job_repo
        self.background_tasks = background_tasks

    def execute_job(self, job_id: UUID, task_func, *args, **kwargs):
        """
        Transitions the job to RUNNING and adds it to FastAPI background tasks.
        """
        job = self.job_repo.get_by_id(job_id)
        if not job:
            logger.error(f"Job {job_id} not found.")
            return

        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        self.job_repo.update(job)

        self.background_tasks.add_task(self._run_wrapper, job_id, task_func, *args, **kwargs)

    async def _run_wrapper(self, job_id: UUID, task_func, *args, **kwargs):
        job = self.job_repo.get_by_id(job_id)
        try:
            # Execute the actual ML logic
            result = await task_func(job_id, *args, **kwargs)
            
            # Job finished successfully
            job = self.job_repo.get_by_id(job_id) # reload
            job.status = JobStatus.COMPLETED
            job.progress = 100.0
            job.completed_at = datetime.utcnow()
            self.job_repo.update(job)
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}")
            logger.error(traceback.format_exc())
            job = self.job_repo.get_by_id(job_id) # reload
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.job_repo.update(job)
