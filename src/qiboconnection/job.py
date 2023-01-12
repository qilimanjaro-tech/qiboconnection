""" Job class """
import base64
import json
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List

from qibo.models.circuit import Circuit
from typeguard import typechecked

from qiboconnection.devices.device import Device
from qiboconnection.job_result import JobResult
from qiboconnection.typings.algorithm import ProgramDefinition
from qiboconnection.typings.job import JobRequest, JobResponse, JobStatus, JobType
from qiboconnection.user import User
from qiboconnection.util import (
    jsonify_dict_and_base64_encode,
    jsonify_str_and_base64_encode,
)


@dataclass
class Job(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    user: User
    device: Device
    program: ProgramDefinition | None = field(default=None)
    circuit: Circuit | None = None
    experiment: dict | None = None
    nshots: int = 10
    job_status: JobStatus = JobStatus.NOT_SENT
    job_result: JobResult | None = None
    id: int = 0  # pylint: disable=invalid-name

    def __post_init__(self):
        if self.experiment is not None and self.circuit is not None:
            raise ValueError("Both circuit and experiment were provided, but execute() only takes at most of them.")
        if self.experiment is None and self.circuit is None:
            raise ValueError("Neither of experiment or circuit were provided,")

    @property
    def user_id(self) -> int | None:
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
    def algorithms(self) -> List[dict]:
        """Get all algorithms described

        Returns:
            List[dict]: a list of all algorithms as a dictionary
        """
        if self.program is None:
            raise ValueError("Job does not contains an algorithm Program")
        return [algorithm.__dict__ for algorithm in self.program.algorithms]

    @property
    def job_request(self) -> JobRequest:
        """Returns a Job Request

        Returns:
            JobRequest: Job Request object
        """
        return JobRequest(
            user_id=self.user.user_id,
            device_id=self.device.id,
            number_shots=self.nshots,
            job_type=self.job_type,
            description=self._get_job_description(),
        )

    @property
    def job_id(self) -> int:
        """Returns Job identifier

        Returns:
            int: Job identifier
        """
        return self.id

    @job_id.setter
    def job_id(self, job_id: int) -> None:
        """
        Modifies internal Job identifier, accessed via job_id property
        Args:
            job_id: new job_id value
        """
        self.id = job_id

    @property
    def job_type(self):
        """Get the type of the job, checking whether the user has defined circuit or experiment."""
        if self.experiment is None and self.circuit is not None:
            return JobType.CIRCUIT
        if self.experiment is not None and self.circuit is None:
            return JobType.EXPERIMENT
        raise ValueError("Could not determine JobType")

    def _get_job_description(self) -> str:
        if self.experiment is None and self.circuit is None:
            raise ValueError("Job requires either a program or a circuit")
        if self.experiment is not None and self.circuit is not None:
            raise ValueError("Job cannot allow to have both circuit and experiment")

        if self.experiment is not None:
            return jsonify_dict_and_base64_encode(object_to_encode=self.experiment)
        if self.circuit is not None:
            return jsonify_str_and_base64_encode(object_to_encode=self.circuit.to_qasm())

        raise ValueError("Something failed.")

    @property
    def result(self) -> Any:
        """Return the result of the job

        Raises:
            ValueError: Job result still not completed

        Returns:
            Any: Job Result data
        """
        if self.job_result is None:
            raise ValueError("Job result still not completed")
        return self.job_result.data

    @typechecked
    def update_with_job_response(self, job_response: JobResponse) -> None:
        """Updates the current job with the given job response

        Args:
            job_response (JobResponse): Job response

        Raises:
            ValueError: Job response does not belong to the user.
            ValueError: Job response does not belong to the device.
        """
        if self.user.user_id != job_response.user_id:
            raise ValueError("Job response does not belong to the user.")
        if self.device.id != job_response.device_id:
            raise ValueError("Job response does not belong to the device.")
        self.job_id = job_response.job_id
        self.job_status = (
            job_response.status if isinstance(job_response.status, JobStatus) else JobStatus(job_response.status)
        )
        self.job_result = JobResult(job_id=self.id, job_type=job_response.job_type, http_response=job_response.result)
