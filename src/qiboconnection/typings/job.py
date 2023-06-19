""" Job Typing """
import enum
from abc import ABC
from dataclasses import dataclass, field
from typing import Any

import numpy


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
        status (str | JobStatus): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    result: str
    status: str | JobStatus


@dataclass(slots=True)
class ListingJobResponse:
    """Job Response without the results. Includes all jobs metadata so that
    the user can identify the id from the job he is interested to retrieve the results.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier

        id (int): Job identifier
        queue_position (int): Job queue position
        status (str | JobStatus): Status of the job
    """

    status: str | JobStatus
    user_id: int
    device_id: int
    job_type: str | JobType
    number_shots: int
    id: int | None = field(default=None)


@dataclass(slots=True)
class JobFullData:
    """Data shown to the user when get_job() method is used. It includes job human-readable results and
    metadata.
    """

    status: str | JobStatus
    queue_position: int
    user_id: int | None
    device_id: int
    job_id: int
    job_type: str | JobType
    number_shots: int
    result: dict | Any | None
