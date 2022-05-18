""" Job Typing """
import enum
from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Dict, List

from qiboconnection.typings.job import JobRequest


@dataclass
class ExecutionRequest(ABC):
    """Job Request

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        number_shots (int): number of times the job is to be executed
    """

    user_id: int
    device_id: int
    jobs: List[JobRequest] = field(default_factory=List)
