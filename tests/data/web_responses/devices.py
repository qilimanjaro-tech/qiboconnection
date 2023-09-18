""" Devices Web Responses """

device_base_response_a = {
    "device_id": 1,
    "device_name": "AWS Development Simulator",
    "status": "other",
    "availability": "available",
    "channel_id": 2,
    "number_pending_jobs": 6,
    "characteristics": {
        "type": "simulator",
        "cpu": "Intel @ 4x 2GHz",
        "gpu": "None",
        "os": "Ubuntu 22.04 jammy",
        "kernel": "x86_64 Linux 5.4.0-80-generic",
        "ram": "4096MiB",
    },
}

device_base_response_b = {
    "device_id": 9,
    "device_name": "AWS Development Quantum",
    "status": "online",
    "availability": "available",
    "channel_id": 2,
    "characteristics": {"type": "quantum"},
    "calibration_details": {"t1": 10, "frequency": 988},
}

device_base_response_c = {  # since the device is offline, there is not calibration info
    "device_id": 7,
    "device_name": "AWS Development Simulator",
    "status": "offline",
    "availability": "available",
    "channel_id": 2,
    "number_pending_jobs": 6,
}


class Devices:
    """Devices Web Responses"""

    retrieve_response: tuple[dict, int] = (device_base_response_a, 200)
    ise_response: tuple[dict, int] = ({}, 500)
    update_response: tuple[dict, int] = retrieve_response
    retrieve_many_response: tuple[tuple[dict, int]] = (
        (
            {
                "items": [device_base_response_a, device_base_response_b, device_base_response_c],
                "total": 3,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/devices?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/devices?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/devices?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/devices?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/devices?page=1&per_page=5",
                },
            },
            200,
        ),
    )
    ise_many_response: tuple[tuple[dict, int]] = (
        (
            {},
            500,
        ),
    )
