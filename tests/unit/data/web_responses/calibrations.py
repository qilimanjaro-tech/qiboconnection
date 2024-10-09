""" Calibrations Web Responses """

calibration_base_response = {
    "calibration_id": 1,
    "name": "MyDemoCalibration",
    "user_id": 1,
    "device_id": 1,
    "description": "A test calibration",
    "calibration": "IUNhbGlicmF0aW9uCmNyb3NzdGFsa19tYXRyaXg6ICFDcm9zc3RhbGtNYXRyaXgKICBtYXRyaXg6CiAgICBmbHV4XzA6IHtmbHV4XzA6IDEuNDcwNDY5MDUsIGZsdXhfMTogMC4xMjI3NjI2MX0KICAgIGZsdXhfMToge2ZsdXhfMDogLTAuNTUzMjIyMDcsIGZsdXhfMTogMS41ODI0Nzg1Nn0Kd2F2ZWZvcm1zOgogIGRyaXZlX3EwX2J1czoKICAgIFhwaTogIUlRUGFpcgogICAgICBJOiAmaWQwMDEgIUdhdXNzaWFuIHthbXBsaXR1ZGU6IDEuMCwgZHVyYXRpb246IDQwLCBudW1fc2lnbWFzOiA0LjV9CiAgICAgIFE6ICFEcmFnQ29ycmVjdGlvbgogICAgICAgIGRyYWdfY29lZmZpY2llbnQ6IC0yLjUKICAgICAgICB3YXZlZm9ybTogKmlkMDAxCiAgcmVhZG91dF9idXM6CiAgICBNZWFzdXJlOiAhSVFQYWlyCiAgICAgIEk6ICFTcXVhcmUge2FtcGxpdHVkZTogMS4wLCBkdXJhdGlvbjogMjAwfQogICAgICBROiAhU3F1YXJlIHthbXBsaXR1ZGU6IDAuMCwgZHVyYXRpb246IDIwMH0Kd2VpZ2h0czoKICByZWFkb3V0X2J1czoKICAgIG9wdGltYWxfd2VpZ2h0czogIUlRUGFpcgogICAgICBJOiAhU3F1YXJlIHthbXBsaXR1ZGU6IDEuMCwgZHVyYXRpb246IDIwMH0KICAgICAgUTogIVNxdWFyZSB7YW1wbGl0dWRlOiAxLjAsIGR1cmF0aW9uOiAyMDB9Cg==",
    "created_at": "Fri, 16 Dec 2022 18:40:24 GMT",
    "updated_at": "Fri, 16 Dec 2022 18:40:24 GMT",
    "qililab_version": "0.0.0",
    "new_field": "hello",
}


class Calibrations:
    """Calibrations Web Responses"""

    ise_response: tuple[dict, int] = ({}, 500)
    create_response: tuple[dict, int] = (calibration_base_response, 201)
    retrieve_response: tuple[dict, int] = (calibration_base_response, 200)
    retrieve_many_response: tuple[tuple[dict, int]] = (
        (
            {
                "items": [calibration_base_response],
                "total": 2,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/calibrations?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/calibrations?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/calibrations?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/calibrations?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/calibrations?page=1&per_page=5",
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
    update_response: tuple[dict, int] = retrieve_response
    delete_response: tuple[str, int] = ("Calibration deleted", 204)
