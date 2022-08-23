""" Job Typing """
import enum
from abc import ABC
from dataclasses import dataclass


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
    description: str
    number_shots: int
    job_type: str | JobType


@dataclass
class JobResponse(JobRequest):
    """Job Response

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
