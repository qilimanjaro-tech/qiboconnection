"""Job listing web responses"""

import json

from requests import Response

from qiboconnection.typings.enums import JobStatus, JobType

job_listing_item_response_a = {
    "user_id": 1,
    "device_id": 7,
    "status": JobStatus.COMPLETED,
    "job_type": JobType.CIRCUIT,
    "number_shots": 45,
    "id": None,
    "whatever": "newfield",
    "more_strange_fields": 79,
}
job_listing_item_response_b = {
    "user_id": 12,
    "device_id": 7,
    "status": JobStatus.PENDING,
    "job_type": JobType.QPROGRAM,
    "number_shots": 45,
    "id": 45,
}

job_listing_item_response_c = {
    "title": "Bad Request",
    "status": 400,
    "detail": "Requested job with 'job_id': 8310, does not exist.",
}

job_listing_item_response_d = {
    "user_id": 12,
    "device_id": 7,
    "status": "canceled",
    "job_type": JobType.OTHER,
    "number_shots": 45,
    "id": 45,
}

job_listing_item_response_e = {
    "user_id": 12,
    "device_id": 7,
    "status": "canceled",
    "job_type": "unknown",
    "number_shots": 45,
    "id": 45,
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
                "items": [job_listing_item_response_a, job_listing_item_response_b, job_listing_item_response_d],
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

    delete_job_response: tuple[str, int] = ("", 204)
    delete_job_response_ise: tuple[str, int] = ("", 500)
    cancel_job_response: tuple[str, int] = ("", 204)
    cancel_job_response_ise: tuple[str, int] = ("", 500)

    retrieve_job_response_1: tuple[dict[str, object], int] = (
        {
            "job_id": 10320,
            "user_id": 6,
            "device_id": 10,
            "status": "pending",
            "job_type": "other",
            "queue_position": 73,
            "description": '{"data": "H4sIAOrAE2YC/81ZS2/jOAz+K0XOgSH5mex1TnvoYXraxaAQFFtxhLEtV5an6Rb570vJ8jN2HrvTor0UFiXy40eJpJT3VZlRtRcyX/3x8L6qmFK8SCvzwRMC/9H6YRVTxVIh3+Cznw/jNONUzy3qLIPPguZMT0lpRhPJWabnJCyjb2TH1CtjBSnrrGKVVduKQB0jktFE1ApEG+RoaU4rxSSheZlxVSeMpIACxLiXJbWkiouiEyG9UH9oEz/eO0SPBm2rSY/Ma4dZ5YFWrAVo9cOni4zu6kBLZthpVUsWK1qkdUbl6nRaDyR/To2iZfX36v7rfzs0z+EsjETSVEuKOicVT3MTc3/dCEgs2H7PY84KHTw0xvn3/TixE0Qo2oaeG0Zbf7MNw88C/nzSWuIDy6lREx94eeEkGLHWLpLpfiuFVFo0v1AvmDs+rR7vecThWBm+U5k7ViZZJQqqhOw1ulc0jtd0igGI9wwDe8lealbEem3k+ZGH9J+DRmZf6h0fOOFdM9nN78wBie7UnOcHGFlza7uI8ORowmmiyYtKyTqHEE8i9P3b43KA6Gs6QmMn77nMX6k065ETOWg1wYMNDLPbmkEmKxuylPLCsKZ9YGXFM7OZf6DnJhEq2n2J/R7yMOHTgZduIK8zxcuMHSFXkxYAt2FBqKVET63eipiwgu4yloAYyGAW4g64aXLmKFLfnx6XN9sZMU+3EeNaTNfYQU7w0fy4I3po/FLzips80pQjxfO+lNzCnskZomTE6IJKpiRPU0hQuWgyXuftqpt6oDLRhBH6i0EqApi99sqkRgAuu6LWs8cLCEaXCu2KwSDJWJGqQ1+whrIOULUzUCwu43JTevGEkoFknEXEATI3pEpw4p/lcwQ5t6AZSVkBXtr80WeViqDp5vEdDwLjh467DUxNEK9AG1gPbjGP7zSP/6P5nBecxFzGNYe0snxYlGJFfWZ4PDwwbzN3K29C7I1P50/G1SFjb8QNEVo2ncSkErWMx0n1bPG58ZweSVxLaWuig+3YLwEnMGVmX0Fq10dnV1dt2ZuPPkww26zejaqmKJQUpjWs3qCQ56QdWa60k4nnSnN+hAO3gwYiIeeTddbqs/jZrmj34mlta62uHuuH+9xq29dLbuGPcevpklvYuDXYc2c70LqMTVD7etlayposPSidL7tMHE0nT+X47Hc7rREOVJCXOG+O+9C/WWszPFSQDjNG+ulGkSgK6I+bY9KjU3FJmr6MJgl0LgYP3roODjcOcjzDB2TCOmt372R7ZEL3EE0LsdaB3TNp0mScifhnAxv6TyB7NW5xZmnBV2iRX4MWf5mWp1tpYcc5WhZytTvKxcM5Q3q+AjUYnXOzmEOmTN1ChXcTFfgLUBHdzAS+zMRCBfXn6+RX2xGu684clwspdpmIhXoeLJbtL3c68AwXffsx5+KYjeeTuXUPH54m3XHTBLt6c1Rir6YSk4xKpmwTP36yMZebrtO18FjGBjdC3eNCv82aL/NANSKgGZk8YzQ3veEVxzZQ3WuLM3lvaW4KRhn5DU8sq0pRqdrbStOv/C7s115gPtSV9j56ozPICaPNJnJDHEWRu8G+d9k3z8E+DrZuGHjBZhttvU90zb3XtSjyQ3/jbt0oCDch8r5w2Lx7ffOD0PM2PgqDyEPhNoguOxc6OEC+76No44fY9fEn+uajpucZXQ6upQ17ISDzR/BK8ph9e17ybvpKPAYfbNoLW9/om89MiLKtXeO3w0FdWLhF9y1/SSXAUOaaPHCpRdE+bStRWrchBrb9g/tM2RvVcIxbfbc8+KVhBKmFaUC01A1xzP6wMIDkDzG1r1K9LgvMzDqDNcuRfRf7OFr01+lk4taGnR1LJrlBcPoXz/KBaccZAAA=", "encoding": "utf-8", "compression": "gzip"}',
            "number_shots": 10,
            "result": None,
            "name": "-",
            "summary": "-",
        },
        200,
    )
    retrieve_job_response_2: tuple[dict[str, object], int] = (
        {
            "job_id": 10320,
            "user_id": 6,
            "device_id": 10,
            "status": "canceled",
            "job_type": "qprogram",
            "queue_position": 73,
            "description": '{"data": "H4sIACzEE2YC/81ZS2/jOAz+K0XOgSH5mex1TnvoYXraxaAQFFtxhLEtV5an6Rb570vJ8jN2HrvTor0UFiXy40eJpJT3VZlRtRcyX/3x8L6qmFK8SCvzwRMC/9H6YRVTxVIh3+Cznw/jNONUzy3qLIPPguZMT0lpRhPJWabnJCyjb2TH1CtjBSnrrGKVVduKQB0jktFE1ApEG+RoaU4rxSSheZlxVSeMpIACxLiXJbWkiouiEyG9UH9oEz/eO0SPBm2rSY/Ma4dZ5YFWrAVo9cOni4zu6kBLZthpVUsWK1qkdUbl6nRaDyR/To2iZfX36v7rfzs0z+EsjETSVEuKOicVT3MTc3/dCEgs2H7PY84KHTw0xvn3/TixE0Qo2oaeG0Zbf7MNw88C/nzSWuIDy6lREx94eeEkGLHWLpLpfiuFVFo0v1AvmDs+rR7vecThWBm+U5k7ViZZJQqqhOw1ulc0jtd0igGI9wwDe8lealbEem3k+ZGH9J+DRmZf6h0fOOFdM9nN78wBie7UnOcHGFlza7uI8ORowmmiyYtKyTqHEE8i9P3b43KA6Gs6QmMn77nMX6k065ETOWg1wYMNDLPbmkEmKxuylPLCsKZ9YGXFM7OZf6DnJhEq2n2J/R7yMOHTgZduIK8zxcuMHSFXkxYAt2FBqKVET63eipiwgu4yloAYyGAW4g64aXLmKFLfnx6XN9sZMU+3EeNaTNfYQU7w0fy4I3po/FLzips80pQjxfO+lNzCnskZomTE6IJKpiRPU0hQuWgyXuftqpt6oDLRhBH6i0EqApi99sqkRgAuu6LWs8cLCEaXCu2KwSDJWJGqQ1+whrIOULUzUCwu43JTevGEkoFknEXEATI3pEpw4p/lcwQ5t6AZSVkBXtr80WeViqDp5vEdDwLjh467DUxNEK9AG1gPbjGP7zSP/6P5nBecxFzGNYe0snxYlGJFfWZ4PDwwbzN3K29C7I1P50/G1SFjb8QNEVo2ncSkErWMx0n1bPG58ZweSVxLaWuig+3YLwEnMGVmX0Fq10dnV1dt2ZuPPkww26zejaqmKJQUpjWs3qCQ56QdWa60k4nnSnN+hAO3gwYiIeeTddbqs/jZrmj34mlta62uHuuH+9xq29dLbuGPcevpklvYuDXYc2c70LqMTVD7etlayposPSidL7tMHE0nT+X47Hc7rREOVJCXOG+O+9C/WWszPFSQDjNG+ulGkSgK6I+bY9KjU3FJmr6MJgl0LgYP3roODjcOcjzDB2TCOmt372R7ZEL3EE0LsdaB3TNp0mScifhnAxv6TyB7NW5xZmnBV2iRX4MWf5mWp1tpYcc5WhZytTvKxcM5Q3q+AjUYnXOzmEOmTN1ChXcTFfgLUBHdzAS+zMRCBfXn6+RX2xGu684clwspdpmIhXoeLJbtL3c68AwXffsx5+KYjeeTuXUPH54m3XHTBLt6c1Rir6YSk4xKpmwTP36yMZebrtO18FjGBjdC3eNCv82aL/NANSKgGZk8YzQ3veEVxzZQ3WuLM3lvaW4KRhn5DU8sq0pRqdrbStOv/C7s115gPtSV9j56ozPICaPNJnJDHEWRu8G+d9k3z8E+DrZuGHjBZhttvU90zb3XtSjyQ3/jbt0oCDch8r5w2Lx7ffOD0PM2PgqDyEPhNoguOxc6OEC+76No44fY9fEn+uajpucZXQ6upQ17ISDzR/BK8ph9e17ybvpKPAYfbNoLW9/om89MiLKtXeO3w0FdWLhF9y1/SSXAUOaaPHCpRdE+bStRWrchBrb9g/tM2RvVcIxbfbc8+KVhBKmFaUC01A1xzP6wMIDkDzG1r1K9LgvMzDqDNcuRfRf7OFr01+lk4taGnR1LJrlBcPoXz/KBaccZAAA=", "encoding": "utf-8", "compression": "gzip"}',
            "number_shots": 10,
            "result": None,
            "duration": 45,
            "name": "-",
            "summary": "-",
        },
        200,
    )

    retrieve_job_response_3: tuple[dict[str, object], int] = (
        {
            "job_id": 10320,
            "user_id": 6,
            "device_id": 10,
            "status": "completed",
            "job_type": "circuit",
            "queue_position": 73,
            "number_shots": 18,
            "result": '{"data": "H4sIAD3LE2YC/6tWKi5JLElVslJQSlJ3hAILFwtHAsBWXUlHQamgKD8pMSkzJ7MkM7UYnxm2EPVpRamFpal5yRDV0YYGsbUAVo9LroEAAAA=", "encoding": "utf-8", "compression": "gzip"}',
            "description": '{"data": "H4sIAP/oE2YC/12MywrCMBBFf2XIWtNMxJUgKIi40FpcJl30MWigBpK2on9vEhBsFwNn7rkzimUZHMmSrwZqof5AcdrnIDhylLyll9A2vx4uxe52BsnFRltjm25sCTRz1JkaeQg0C8J5uoNT6zJwEzmM6QfyQq1i9ghS/ABT651o4ZSM65OqfvSUarDc/t2LqcaZxqmWMx2es/ILKnGVruoAAAA=", "encoding": "utf-8", "compression": "gzip"}',
            "duration": 45,
            "name": "-",
            "summary": "-",
        },
        200,
    )
