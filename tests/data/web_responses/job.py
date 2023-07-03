"""Job listing web responses"""

import json

from requests import Response

from qiboconnection.typings.job import JobStatus, JobType

job_listing_item_response_a = {
    "user_id": 1,
    "device_id": 7,
    "status": JobStatus.COMPLETED,
    "job_type": JobType.CIRCUIT,
    "number_shots": 45,
    "id": None,
}
job_listing_item_response_b = {
    "user_id": 12,
    "device_id": 7,
    "status": JobStatus.PENDING,
    "job_type": JobType.EXPERIMENT,
    "number_shots": 45,
    "id": 45,
}

job_listing_item_response_c = {
    "title": "Bad Request",
    "status": 400,
    "detail": "Requested job with 'job_id': 8310, does not exist.",
}


class JobResponse:
    """mock job web responses"""

    @classmethod
    def retrieve_job_response_400_raw(cls):
        response = Response()
        response.status_code = 404
        response._content = json.dumps(
            {"title": "Bad Request", "detail": "Requested job with 'job_id': 8310, does not exist."}
        ).encode("utf-8")
        return response

    retrieve_job_listing_response: tuple[tuple[dict, int]] = (
        (
            {
                "items": [job_listing_item_response_a, job_listing_item_response_b],
                "total": 2,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/jobs?page=1&per_page=5",
                },
            },
            200,
        ),
    )
