""" JobListingItem class """

from dataclasses import dataclass, field

from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.responses import JobListingItemResponse


@dataclass
class JobListingItem:
    """JobListing single item representation."""

    user_id: int
    device_id: int
    status: str | JobStatus
    job_type: str | JobType
    number_shots: int
    id: int | None = field(default=None)

    @classmethod
    def from_response(cls, response: JobListingItemResponse):
        """Constructor for JobListingItems that takes in a JobListingItemResponse"""
        return cls(
            id=response.id,
            user_id=response.user_id,
            device_id=response.device_id,
            job_type=response.job_type,
            status=response.status,
            number_shots=response.number_shots,
        )
