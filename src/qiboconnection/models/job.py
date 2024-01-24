# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Job Typing """
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List

from qibo.models.circuit import Circuit
from typeguard import typechecked

from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.requests import JobRequest
from qiboconnection.typings.responses.job_response import JobResponse
from qiboconnection.util import jsonify_dict_and_base64_encode, jsonify_list_with_str_and_base64_encode

from .algorithm import ProgramDefinition
from .devices.device import Device
from .job_result import JobResult
from .user import User


@dataclass
class Job(ABC):  # pylint: disable=too-many-instance-attributes
    """Job class to manage the job experiment to be remotely sent"""

    user: User
    device: Device
    program: ProgramDefinition | None = field(default=None)
    circuit: list[Circuit] | None = None
    qprogram: dict | None = None
    nshots: int = 10
    job_status: JobStatus = JobStatus.NOT_SENT
    job_result: JobResult | None = None
    id: int = 0  # pylint: disable=invalid-name

    def __post_init__(self):
        if self.qprogram is not None and self.circuit is not None:
            raise ValueError("Both circuit and qprogram were provided, but execute() only takes one of them.")
        if self.qprogram is None and self.circuit is None:
            raise ValueError("Neither of circuit or qprogram were provided.")

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
            raise ValueError("Job does not contain an algorithm Program")

        return [algorithm.__dict__ for algorithm in self.program.algorithms]

    @property
    def job_request(self) -> JobRequest:
        """Returns a Job Request with the Job instance info

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
        if self.qprogram is None and self.circuit is not None:
            return JobType.CIRCUIT
        if self.qprogram is not None and self.circuit is None:
            return JobType.QPROGRAM
        raise ValueError("Could not determine JobType")

    def _get_job_description(self) -> str:
        """Serialize either circuit or qprogram to obtain job description"""

        if self.qprogram is not None:
            return jsonify_dict_and_base64_encode(object_to_encode=self.qprogram)

        if self.circuit is not None:
            return jsonify_list_with_str_and_base64_encode(object_to_encode=[c.to_qasm() for c in self.circuit])

        raise ValueError("No suitable information found for building description.")

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
