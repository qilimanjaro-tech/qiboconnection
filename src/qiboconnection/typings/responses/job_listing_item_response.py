""" JobListingItemResponse typing """

from dataclasses import dataclass, field


@dataclass(slots=True)
class JobListingItemResponse:
    """Job Response without the results. Includes all jobs metadata so that
    the user can identify the id from the job he is interested to retrieve the results.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier

        id (int): Job identifier
        status (str): Status of the job
    """

    status: str
    user_id: int
    device_id: int
    job_type: str
    number_shots: int
    id: int | None = field(default=None)
