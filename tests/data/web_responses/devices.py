""" Devices Web Responses """


class Devices:
    """Devices Web Responses"""

    retrieve_response = (
        {
            "device_id": 1,
            "device_name": "AWS Development Simulator",
            "status": "available",
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
        },
        200,
    )

    update_response = retrieve_response

    retrieve_many_response = (
        (
            {
                "items": [
                    {
                        "device_id": 1,
                        "device_name": "AWS Development Simulator",
                        "status": "available",
                        "channel_id": 2,
                        "characteristics": {
                            "type": "simulator",
                            "cpu": "Intel @ 4x 2GHz",
                            "gpu": "None",
                            "os": "Ubuntu 22.04 jammy",
                            "kernel": "x86_64 Linux 5.4.0-80-generic",
                            "ram": "4096MiB",
                        },
                    },
                    {
                        "device_id": 9,
                        "device_name": "AWS Development Quantum",
                        "status": "available",
                        "channel_id": 2,
                        "characteristics": {"type": "quantum"},
                        "calibration_details": {"t1": 10, "frequency": 988},
                    },
                    {
                        "device_id": 10,
                        "device_name": "Galadriel Qblox rack                              ",
                        "status": "offline",
                        "channel_id": 0,
                    },
                ],
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
