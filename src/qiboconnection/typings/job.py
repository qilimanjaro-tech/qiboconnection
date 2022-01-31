import enum
from typing import TypedDict, Union


class JobStatus(enum.Enum):
    not_sent = "not sent"
    pending = "pending"
    running = "running"
    completed = "completed"
    error = "error"


class JobRequest(TypedDict):
    user_id: int
    device_id: int
    description: str


class JobResponse(JobRequest):
    job_id: int
    queue_position: int
    status: Union[str, JobStatus]
    result: str
