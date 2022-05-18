""" Job class """
import base64
import io
import json
import pickle  # nosec - temporary bandit ignore
from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Any, List, cast

from qibo.models.circuit import Circuit
from typeguard import typechecked

from qiboconnection.devices.device import Device
from qiboconnection.job import Job
from qiboconnection.job_result import JobResult
from qiboconnection.typings.algorithm import ProgramDefinition
from qiboconnection.typings.execution import ExecutionRequest
from qiboconnection.typings.experiment import Experiment
from qiboconnection.typings.job import JobRequest, JobResponse, JobStatus, JobType
from qiboconnection.user import User
from qiboconnection.util import base64url_encode


@dataclass
class Execution(ABC):
    """Execution class to manage the experiment to be remotely sent"""

    user: User
    device: Device
    jobs: List[Job] = field(default_factory=List)
    id: int = 0  # pylint: disable=invalid-name

    @property
    def user_id(self) -> int:
        """User identifier

        Returns:
            int: User identifier
        """
        return self.user.user_id

    @property
    def device_id(self) -> int:
        """Device identifier

        Returns:
            int: Device identifier
        """
        return self.device.id

    @property
    def execution_request(self) -> ExecutionRequest:
        """Returns a Job Request

        Returns:
            JobRequest: Job Request object
        """
        return ExecutionRequest(
            user_id=self.user.user_id,
            device_id=self.device.id,
            jobs=[job.job_request for job in self.jobs],
        )

    @property
    def execution_id(self) -> int:
        """Returns Job identifier

        Returns:
            int: Job identifier
        """
        return self.id

    @execution_id.setter
    def execution_id(self, execution_id: int) -> None:
        """
        Modifies internal Job identifier, accessed via job_id property
        Args:
            job_id: new job_id value
        """
        self.id = execution_id

    @property
    def result(self) -> Any:
        """Return the result of the job

        Raises:
            ValueError: Job result still not completed

        Returns:
            Any: Job Result data
        """
        return [job.job_result.data for job in self.jobs]

    def get_job(self, job_id: int):
        """Gets the job from the internal job list that matches the provided job_id"""
        job = next((job for job in self.jobs if job.job_id == job_id), None)
        if job is None:
            raise ValueError(
                f"qiboconnection could not found any job with id {job_id} inside" f"execution {self.execution_id}."
            )
        return job

    @typechecked
    def update_with_job_response(self, job_id: int, job_response: JobResponse) -> None:
        """Updates the current job with the given job response

        Args:
            job_id (int): Job to update with response
            job_response (JobResponse): Job response

        Raises:
            ValueError: Job response does not belong to the user.
            ValueError: Job response does not belong to the device.
        """
        if self.user.user_id != job_response.user_id:
            raise ValueError("Job response does not belong to the user.")
        if self.device.id != job_response.device_id:
            raise ValueError("Job response does not belong to the device.")
        job = self.get_job(job_id=job_id)
        job.job_id = job_response.job_id
        job.job_status = (
            job_response.status if isinstance(job_response.status, JobStatus) else JobStatus(job_response.status)
        )
        job.job_result = JobResult(job_id=self.id, http_response=job_response.result)


def _jsonify_dict_and_base64_encode(object_to_encode: dict):
    """
    Jsonifies a given dict, encodes it to bytes assuming utf-8, and encodes that byte obj to an url-save base64 str
    """
    return str(base64.urlsafe_b64encode(json.dumps(object_to_encode).encode("utf-8")), "utf-8")


def _jsonify_str_and_base64_encode(object_to_encode: str):
    """Encodes a given string to bytes assuming utf-8, and encodes that byte-array to a nurl-save base64 str"""
    return str(base64.urlsafe_b64encode(object_to_encode.encode("utf-8")), "utf-8")
