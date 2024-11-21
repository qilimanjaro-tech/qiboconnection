"""Auth Web Responses"""

import json

from requests import Response

from qiboconnection.typings.enums import TokenType

auth_base_response = {
    "accessToken": (
        "eyJhbGciOiJFZERTQSIsImtpZCI6InlYaG5lSUtxUEV5UklSLXVyMHdGZUZzLTZ2VS01amJEY18wUFN0X2Etc1UiLCJ0eXAiOiJKV1QifQ"
        + ".eyJhdWQiOiJodHRwczovL3FpbGltYW5qYXJvZGV2LmRkbnMubmV0OjgwODAvYXBpL3YxIiwiZXhwIjoxNjg0N"
        + "DA1NjcxLCJpYXQiOjE2ODQ0MDU2NzEsImlzcyI6Imh0dHBzOi8vcWlsaW1hbmphcm9kZXYuZGRucy5uZXQ6ODA4"
        + "MC8iLCJ0eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MywidXNlcl9yb2xlIjoiYWRtaW4ifQ"
        + ".aUDUO8n5M5cqyhw8bM9Uo-Ler-MxKsWtA3NNW5IHN4Lza8oK4KlEFXeVaATVOzeg05tsytfkFdR1HPCHx9YiAg"
    ),
    "refreshToken": (
        "eyJhbGciOiJFZERTQSIsImtpZCI6InlYaG5lSUtxUEV5UklSLXVyMHdGZUZzLTZ2VS01amJEY18wUFN0X2Etc1UiLCJ0eXAiOiJKV1QifQ"
        + ".eyJhdWQiOiJodHRwczovL3FpbGltYW5qYXJvZGV2LmRkbnMubmV0OjgwODAvYXBpL3YxIiwiZXhwIjoxNjg0NDk"
        + "yMDcxLCJpYXQiOjE2ODQ0MDU2NzEsImlzcyI6Imh0dHBzOi8vcWlsaW1hbmphcm9kZXYuZGRucy5uZXQ6ODA4MC8i"
        + "LCJ0eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjMsInVzZXJfcm9sZSI6ImFkbWluIn0"
        + ".4oSyRW9Ia7C-50x2yZxQAEXDZp-TLkFkPOtHBR4cCi9LnkREtYrJpDXufep_EYoRwDSJL_2z20moYMuMHy0QCg"
    ),
    "tokenType": TokenType.BEARER.value,
    "expiresIn": 1684402144,
    "issuedAt": 1684403144,
}


class Auth:
    """Auth Web Responses"""

    retrieve_response: tuple[dict, int] = (auth_base_response, 201)
    ise_response: tuple[dict, int] = ({}, 500)

    @property
    def raw_retrieve_response(self):
        """Builds a raw requests' Response() instance, as if we performed directly the request operation

        Returns:
            response instance with the information
        """
        response = Response()
        response._content = json.dumps(self.retrieve_response[0]).encode("utf-8")
        response.status_code = self.retrieve_response[1]
        return response
