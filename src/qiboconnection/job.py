# job.py
from abc import ABC
from typing import Any, List, Optional, Union
from qiboconnection.typings.algorithm import ProgramDefinition
from qiboconnection.user import User
from qiboconnection.devices.device import Device
from qiboconnection.typings.job import JobRequest, JobResponse, JobStatus
from qiboconnection.job_result import JobResult
from qiboconnection.util import base64url_encode
from typeguard import typechecked
from qibo.core.circuit import Circuit
import json
import pickle
import io
import base64
from qiboconnection.config import logger


class Job(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    @typechecked
    def __init__(
        self,
        user: User,
        device: Device,
        program: Optional[ProgramDefinition] = None,
        circuit: Optional[Circuit] = None,
        job_status: Optional[JobStatus] = JobStatus.not_sent,
        job_result: Optional[JobResult] = None,
        id: Optional[int] = 0,
    ):
        self._id = id
        self._program = program
        self._circuit = circuit
        self._status: JobStatus = job_status
        self._user: User = user
        self._device: Device = device
        self._result: Union[JobResult, None] = job_result

        if self._program is None and self._circuit is None:
            raise ValueError("Job requires either a program or a circuit")

    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user.id

    @property
    def device_id(self) -> int:
        return self._device.id

    @property
    def algorithms(self) -> List[dict]:
        return [algorithm.__dict__ for algorithm in self._program.algorithms]

    @property
    def job_request(self) -> JobRequest:
        return JobRequest(
            {
                "user_id": self._user.id,
                "device_id": self._device.id,
                "description": self._get_job_description(),
            }
        )

    @id.setter
    def id(self, job_id: int) -> None:
        self._id = job_id

    def _get_job_description(self) -> str:
        if self._program is None and self._circuit is None:
            raise ValueError("Job requires either a program or a circuit")

        if self._program is not None:
            return base64url_encode(json.dumps(self.algorithms))
        if self._circuit is not None:
            circuitBuffer = io.BytesIO()
            pickle.dump(self._circuit, circuitBuffer)
            return str(base64.urlsafe_b64encode(circuitBuffer.getvalue()), "utf-8")

    @property
    def result(self) -> Any:
        if self._result is None:
            raise ValueError("Job result still not completed")
        return self._result.data

    @typechecked
    def update_with_job_response(self, job_response: JobResponse) -> None:
        if self._user.id != job_response["user_id"]:
            raise ValueError("Job response does not belong to the user.")
        if self._device.id != job_response["device_id"]:
            raise ValueError("Job response does not belong to the device.")
        self._id = job_response["job_id"]
        self._status = (
            job_response["status"]
            if isinstance(job_response["status"], JobStatus)
            else JobStatus(job_response["status"])
        )
        self._result = JobResult(http_response=job_response["result"])
