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
from qiboconnection.typings.responses import JobResponse
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


def deserialize_job_description(base64_description: str, job_type: str) -> Circuit | dict | str:
    """Convert base64 job description to its corresponding Qibo Circuit or Qililab experiment

    Args:
        base64_description (str):
        job_type (str):

    Raises:
        ValueError: Job type isn't nor Qibo Circuit neither Qililab experiment

    Returns:
        Circuit | dict: _description_
    """
    if job_type == JobType.CIRCUIT:
        return Circuit.from_qasm(base64_decode(encoded_data=base64_description))

    if job_type == JobType.EXPERIMENT:
        return json.loads(base64_decode(encoded_data=base64_description))

    return "JobType not supported!"  # this will be developed in the future. No exception needs to be risen here because we are reading past resulls here.


def log_job_status_info(job_response: JobResponse):
    """Logs a message depending on the `JobResponse.status` belonging to a certain job.

    Args:
        job_response:

    Returns:

    """
    if job_response.status == JobStatus.PENDING:
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
    else:
        logger.warning(f"Your job with id %i is {job_response.status}.", job_response.job_id)
        return None
