""" Job Data Typing """
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass

from qibo.models.circuit import Circuit

from qiboconnection.typings.enums import JobStatus, JobType


@dataclass(slots=True)
class JobData:
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
    description: Circuit | dict
    result: dict | None
