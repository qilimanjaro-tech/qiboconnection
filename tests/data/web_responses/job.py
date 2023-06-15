"""Job listing web responses"""

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


class JobResponse:
    """mock job web responses"""

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
