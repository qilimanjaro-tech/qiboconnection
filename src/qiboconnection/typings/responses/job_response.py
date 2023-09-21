""" JobResponse """
from dataclasses import dataclass

from ..requests import JobRequest


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
