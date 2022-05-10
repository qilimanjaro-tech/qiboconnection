""" Job Typing """
import enum
from abc import ABC
from dataclasses import dataclass


class JobType(enum.Enum):
    """Job Type

    Args:
        enum (str): Accepted values are:
            * "circuit"
            * "experiment"
    """

    CIRCUIT = "circuit"
    EXPERIMENT = "experiment"


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
class JobRESTBase(ABC):
    """
    BaseClass for building JobRequest and JobResponse
    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
    """

    user_id: int
    device_id: int
    description: str


@dataclass
class JobRequest(JobRESTBase):
    """Job Request

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        number_shots (int): number of times the job is to be executed
    """

    number_shots: int


@dataclass
class JobResponse(JobRESTBase):
    """Job Response

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        job_id (int): Job identifier
        queue_position (int): Job queue position
        status (str | JobStatus): Status of the job
        job_type (str | JobType): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    result: str
    status: str | JobStatus
    job_type: str | JobType
