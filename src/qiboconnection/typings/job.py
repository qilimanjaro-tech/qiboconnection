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
import enum
from abc import ABC
from dataclasses import dataclass, field

from qibo.models.circuit import Circuit


class JobType(str, enum.Enum):
    """Job Type

    Args:
        enum (str): Accepted values are:
            * "circuit"
            * "experiment"
    """

    CIRCUIT = "circuit"
    PROGRAM = "program"
    EXPERIMENT = "experiment"


class JobStatus(str, enum.Enum):
    """Job Status

    Args:
        enum (str): Accepted values are:
            * "not sent"
            * "pending"
            * "running"
            * "completed"
            * "error"
    """

    NOT_SENT = "not sent"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class JobRequest(ABC):
    """Job Request

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        job_type (str | JobType): Type of the job
        number_shots (int): number of times the job is to be executed
    """

    user_id: int | None
    device_id: int
    number_shots: int
    job_type: str | JobType
    description: str


@dataclass
class JobResponse(JobRequest):
    """Full Job Response. Includes job results which may
    be weight a few GB.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        job_id (int): Job identifier
        queue_position (int): Job queue position
        status (str): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    result: str
    status: str


@dataclass(slots=True)
class ListingJobResponse:
    """Job Response without the results. Includes all jobs metadata so that
    the user can identify the id from the job he is interested to retrieve the results.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier

        id (int): Job identifier
        queue_position (int): Job queue position
        status (str): Status of the job
    """

    status: str
    user_id: int
    device_id: int
    job_type: str | JobType
    number_shots: int
    id: int | None = field(default=None)


@dataclass(slots=True)
class JobData:  # pylint: disable=too-many-instance-attributes
    """Data shown to the user when get_job() method is used. It includes job human-readable results and
    metadata.
    """

    status: str
    queue_position: int
    user_id: int | None
    device_id: int
    job_id: int
    job_type: str
    number_shots: int
    description: Circuit | dict
    result: dict | None
