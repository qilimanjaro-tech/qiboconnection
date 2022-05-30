""" Job Typing """
from abc import ABC
from dataclasses import dataclass, field
from typing import List

from qiboconnection.config import logger
from qiboconnection.job_result import JobResult
from qiboconnection.typings.job import JobRequest, JobStatus, JobType


@dataclass
class ExecutionRequest(ABC):
    """Job Request

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        jobs (list[JobRequest]): Job input list
    """

    user_id: int
    device_id: int
    jobs: List[JobRequest] = field(default_factory=List)


@dataclass
class ExecutionJobResponse(ABC):
    """Job Response expected inside ExecutionResponse.jobs field.
    Attributes:
        job_id (int): Job identifier
        execution_id (int): linked execution identifier
        status (str | JobStatus): Status of the job
        job_type (str | JobType): Status of the job
        queue_position (int): Job queue position
        description (str): Description of the job
        number_shots (int): Number of Shots for that Job
        result (JobResult): Job result
    """

    job_id: int
    execution_id: int
    status: JobStatus
    job_type: JobType
    queue_position: int
    description: str
    number_shots: int
    result: JobResult


@dataclass
class ExecutionResponse(JobRequest):
    """Job Response

    Attributes:
        execution_id (int): linked execution identifier
        user_id (int): User identifier
        device_id (int): Device identifier
        jobs (list[ExecutionJobResponse): list of jobs to parse
    """

    execution_id: int
    user_id: int
    device_id: int
    jobs: list[ExecutionJobResponse]

    def log_status(self):
        """Logs a summary of the status of all the jobs issued in the execution."""
        pending, running, not_sent, error, completed = [], [], [], [], []

        for job in self.jobs:
            if job.status == JobStatus.PENDING:
                pending.append(job)
            if job.status == JobStatus.RUNNING:
                running.append(job)
            if job.status == JobStatus.NOT_SENT:
                not_sent.append(job)
            if job.status == JobStatus.ERROR:
                error.append(job)
            if job.status == JobStatus.COMPLETED:
                completed.append(job)

        if pending:
            logger.warning(
                f"Execution {self.execution_id} still has still {len(pending)} pending"
                f" job{'s' if len(pending) != 1 else ''}."
            )
        if running:
            logger.warning(
                f"Execution {self.execution_id} still has {len(running)} currently running"
                f" job{'s' if len(running) != 1 else ''}."
            )
        if not_sent:
            logger.warning(
                f"Execution {self.execution_id} still has {len(not_sent)} not sent"
                f" job{'s' if len(not_sent) != 1 else ''}."
            )
        if error:
            logger.error(
                f"Execution {self.execution_id} still has found errors in {len(error)}"
                f" job{'s' if len(error) != 1 else ''}."
            )
        logger.info(
            f"Execution {self.execution_id} still has completed {len(completed)} out of {len(self.jobs)}"
            f" job{'s' if len(completed) != 1 else ''}."
        )

    @property
    def results(self):
        """
        Gives back the results for the execution.
        Returns: A list with the results of the jobs in order. Non-completed results will be represented with a None.
        """

        return [job.result for job in self.jobs]
