# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Util Functions used by the API module """

import json
from typing import Any, List

from qibo.models.circuit import Circuit

from qiboconnection.config import logger
from qiboconnection.models import JobResult
from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.responses.job_response import JobResponse
from qiboconnection.util import decompress_any


def parse_job_responses_to_results(job_responses: List[JobResponse]) -> List[dict | Any | None]:
    """Parse a list of job_responses to a list of dict with the content of each job. If the job is not COMPLETED,
    put a None in its place. For this, we build a JobResult instance for each COMPLETED job, and then we keep its
    `.data`.

    Args:
        job_responses: list of JobResponse instances from which we'll

    Returns:

    """
    raw_results = [parse_job_response_to_result(job_response=job_response) for job_response in job_responses]
    return list(raw_results)


def parse_job_response_to_result(job_response: JobResponse):
    """Parse a single job_response to a single dict with the content of a job. If the job is not COMPLETED,
    put a None in its place. For this, we build a JobResult instance for each COMPLETED job, and then we keep its
    `.data`.

    Args:
        job_response: JobResponse instance from which we'll get the results

    Returns:

    """
    return (
        JobResult(job_id=job_response.job_id, job_type=job_response.job_type, http_response=job_response.result).data
        if job_response.status == JobStatus.COMPLETED
        else None
    )


def deserialize_job_description(raw_description: str, job_type: str) -> dict:
    """Convert base64 job description to its corresponding Qibo Circuit or Qililab experiment

    Args:
        raw_description (str):
        job_type (str):

    Raises:
        ValueError: Job type isn't nor Qibo Circuit neither Qililab experiment

    Returns:
        Circuit | dict: _description_
    """

    description_dict = json.loads(raw_description)
    decompressed_data = decompress_any(**description_dict)
    compressed_data = description_dict.pop("data")
    if job_type == JobType.CIRCUIT:
        return {
            **description_dict,
            "data": [Circuit.from_qasm(decom_data) for decom_data in decompressed_data],
        }
    if job_type == JobType.VQA:
        return {**description_dict, "vqa_dict": decompressed_data}
    if job_type in [JobType.QPROGRAM, JobType.ANNEALING_PROGRAM, JobType.OTHER]:
        return {**description_dict, "data": decompressed_data}
    return {**description_dict, "data": compressed_data}


def log_job_status_info(job_response: JobResponse):
    """Logs a message depending on the `JobResponse.status` belonging to a certain job.

    Args:
        job_response:

    Returns:

    """
    if job_response.status in [JobStatus.QUEUED, JobStatus.PENDING]:
        logger.warning(
            "Your job with id %i is still pending. Job queue position: %s",
            job_response.job_id,
            job_response.queue_position,
        )
        return None

    if job_response.status == JobStatus.RUNNING:
        logger.warning("Your job with id %i is still running.", job_response.job_id)
        return None
    if job_response.status == JobStatus.NOT_SENT:
        logger.warning("Your job with id %i has not been sent.", job_response.job_id)
        return None
    if job_response.status == JobStatus.ERROR:
        logger.error("Your job with id %i failed.", job_response.job_id)
        return None
    if job_response.status == JobStatus.COMPLETED:
        logger.warning("Your job with id %i is completed.", job_response.job_id)
        return None

    logger.warning(f"Your job with id %i is {job_response.status}.", job_response.job_id)
    return None
