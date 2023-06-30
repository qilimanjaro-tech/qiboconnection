""" Util Functions used by the API module """

import json
from typing import Any, List

from qibo.models.circuit import Circuit

from qiboconnection.config import logger
from qiboconnection.job_result import JobResult
from qiboconnection.typings.job import JobResponse, JobStatus, JobType
from qiboconnection.util import base64_decode


def parse_job_responses_to_results(job_responses: List[JobResponse]) -> List[dict | Any | None]:
    """Parse a list of job_responses to a list of dict with the content of each job. If the job is not COMPLETED,
    put a None in its place. For this, we build a JobResult instance for each COMPLETED job, and then we keep its
    `.data`.

    Args:
        job_responses: list of JobResponse instances from which we'll

    Returns:

    """
    raw_results = [
        JobResult(job_id=job_response.job_id, job_type=job_response.job_type, http_response=job_response.result).data
        if job_response.status == JobStatus.COMPLETED
        else None
        for job_response in job_responses
    ]
    return [raw_result[0] if isinstance(raw_result, List) else raw_result for raw_result in raw_results]


def deserialize_job_description(base64_description: str, job_type: str) -> Circuit | dict:
    if job_type == JobType.CIRCUIT:
        return Circuit.from_qasm(base64_decode(encoded_data=base64_description))
    elif job_type == JobType.EXPERIMENT:
        return json.loads(base64_decode(encoded_data=base64_description))
    else:
        raise ValueError(f"{job_type} not supported, it needs to be either {JobType.CIRCUIT} or {JobType.EXPERIMENT}")


def log_job_status_info(job_response: JobResponse):
    """Logs a message depending on the `JobResponse.status` belonging to a certain job.

    Args:
        job_response:

    Returns:

    """
    status = job_response.status if isinstance(job_response.status, JobStatus) else JobStatus(job_response.status)
    if status == JobStatus.PENDING:
        logger.warning(
            "Your job with id %i is still pending. Job queue position: %s",
            job_response.job_id,
            job_response.queue_position,
        )
        return None
    if status == JobStatus.RUNNING:
        logger.warning("Your job with id %i is still running.", job_response.job_id)
        return None
    if status == JobStatus.NOT_SENT:
        logger.warning("Your job with id %i has not been sent.", job_response.job_id)
        return None
    if status == JobStatus.ERROR:
        logger.error("Your job with id %i failed.", job_response.job_id)
        return None
    if status == JobStatus.COMPLETED:
        logger.warning("Your job with id %i is completed.", job_response.job_id)
        return None

    raise ValueError(
        f"Job status for job with id {job_response.job_id} is not supported: status is {job_response.status}"
    )
