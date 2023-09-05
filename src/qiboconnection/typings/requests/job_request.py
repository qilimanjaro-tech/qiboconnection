from abc import ABC
from dataclasses import dataclass

from ..enums import JobType


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
