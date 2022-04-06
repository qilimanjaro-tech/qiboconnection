""" Job Typing """
import enum
from abc import ABC
from dataclasses import dataclass


class JobStatus(enum.Enum):
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
    """

    user_id: int
    device_id: int
    description: str


@dataclass
class JobResponse(JobRequest):
    """Job Response

    Attributes:
        job_id (int): Job identifier
        queue_position (int): Job queue position
        status (str | JobStatus): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    status: str | JobStatus
    result: str
