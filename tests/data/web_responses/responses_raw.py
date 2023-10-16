"""requests module raw responses"""

import json

from requests import Response


class ResponsesRaw:
    """Raw Response from requests library examples"""

    @property
    def response_200(self):
        """Builds a 200 OK response"""
        response = Response()
        response.status_code = 200
        response._content = json.dumps({"status": "OK"}).encode("utf-8")
        return response

    @property
    def response_200_paginated(self):
        """Builds a 200 OK response"""
        response = Response()
        response.status_code = 200
        response._content = json.dumps(
            {
                "items": [{"key": "value"}],
                "total": 2,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=None&per_page=5",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=5",
                },
            }
        ).encode("utf-8")
        return response

    @property
    def response_200_paginated_last(self):
        """Builds a 200 OK response"""
        response = Response()
        response.status_code = 200
        response._content = json.dumps(
            {
                "items": [{"key": "value"}],
                "total": 2,
                "per_page": 5,
                "self": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=5",
                "links": {
                    "first": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=5",
                    "prev": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=None&per_page=5",
                    "next": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=None&per_page=None",
                    "last": "https://qilimanjarodev.ddns.net:8080/api/v1/path?page=1&per_page=None",
                },
            }
        ).encode("utf-8")
        return response

    @property
    def response_201(self):
        """Builds a 201 CREATED response"""
        response = Response()
        response.status_code = 201
        response._content = json.dumps({"status": "CREATED"}).encode("utf-8")
        return response

    @property
    def response_204(self):
        """Builds a 201 NO CONTENT response"""
        response = Response()
        response.status_code = 204
        response._content = json.dumps("").encode("utf-8")
        return response

    @property
    def response_301(self):
        """Builds a 301 MOVED response"""
        response = Response()
        response.status_code = 301
        response._content = json.dumps({"status": "MOVED"}).encode("utf-8")
        return response

    @property
    def response_400(self):
        """Builds a 400 BAD REQUEST response"""
        response = Response()
        response.status_code = 400
        response._content = json.dumps({"status": "BAD REQUEST"}).encode("utf-8")
        return response

    @property
    def response_401(self):
        """Builds a 400 UNAUTHORISED response"""
        response = Response()
        response.status_code = 401
        response._content = json.dumps({"status": "UNAUTHORISED"}).encode("utf-8")
        return response

    @property
    def response_404(self):
        """Builds a 404 NOT FOUND response"""
        response = Response()
        response.status_code = 404
        response._content = json.dumps({"status": "NOT FOUND"}).encode("utf-8")
        return response

    @property
    def response_500(self):
        """Builds a 500 SERVER ERROR response"""
        response = Response()
        response.status_code = 500
        response._content = json.dumps({"status": "INTERNAL SERVER ERROR"}).encode("utf-8")
        return response
