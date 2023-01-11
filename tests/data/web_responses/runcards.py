""" Runcards Web Responses """

runcard_base_response = {
    "runcard_id": 1,
    "name": "MyDemoRuncard",
    "user_id": 1,
    "device_id": 1,
    "description": "A test runcard",
    "runcard": "",
    "created_at": "Fri, 16 Dec 2022 18:40:24 GMT",
    "qililab_version": "0.0.0",
}


class Runcards:
    """Runcards Web Responses"""

    create_response: tuple[dict, int] = (runcard_base_response, 201)
    retrieve_response: tuple[dict, int] = (runcard_base_response, 200)
    retrieve_many_response: tuple[tuple[dict, int]] = (
        (
            {
                "items": [runcard_base_response],
                "total": 1,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/runcards?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/runcards?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/runcards?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/runcards?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/runcards?page=1&per_page=5",
                },
            },
            200,
        ),
    )
    update_response: tuple[dict, int] = retrieve_response
    delete_response: tuple[str, int] = ("Runcard deleted", 204)
