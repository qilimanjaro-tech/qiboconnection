# connection.py
from abc import ABC
from json.decoder import JSONDecodeError
from typing import Any, Optional, Tuple, Union
from datetime import datetime, timezone
import json
import requests
from typeguard import typechecked
from qiboconnection.config import QQS_URL, AUDIENCE_URL, logger
from qiboconnection.user import User
from qiboconnection.util import (
    base64url_encode,
    write_config_file_to_disk,
    load_config_file_to_disk,
)
from qiboconnection.typings.auth_config import AssertionPayload, AccessTokenResponse
from qiboconnection.errors import custom_raise_for_status, ConnectionException
from qiboconnection.typings.connection import (
    ConnectionConfiguration,
    ConnectionEstablished,
)


class Connection(ABC):
    """Class to create a remote connection to a Qibo server"""

    @typechecked
    def __init__(
        self,
        configuration: Optional[ConnectionConfiguration] = None,
        api_path: Optional[str] = None,
    ):
        self._audience_url = f"{AUDIENCE_URL}/api/v1"
        self._load_configuration(configuration, api_path)

    @property
    def user(self) -> User:
        return self._user

    def _set_api_calls(self, api_path: str):
        self._api_path = api_path
        self._remote_server_api_url = f"{QQS_URL}{api_path}"
        self._remote_server_base_url = f"{QQS_URL}"
        self._authorisation_server_api_call = (
            f"{self._remote_server_api_url}/authorisation-tokens"
        )

    def _store_configuration(self) -> None:
        logger.info("Storing personal qibo configuration...")
        write_config_file_to_disk(
            config_data=ConnectionEstablished(
                {
                    **self._user.__dict__,
                    "authorisation_access_token": self._authorisation_access_token,
                    "api_path": self._api_path,
                }
            )
        )

    def _load_configuration(
        self,
        input_configuration: Optional[ConnectionConfiguration] = None,
        api_path: Optional[str] = None,
    ) -> None:
        if input_configuration is None:
            try:
                return self._register_configuration_with_authorisation_access_token(
                    load_config_file_to_disk()
                )
            except FileNotFoundError:
                raise ConnectionException(
                    "No connection configuration found. Please provide a new configuration."
                )

        if api_path is None:
            raise ConnectionException("No api path provided.")
        self._set_api_calls(api_path=api_path)
        self._register_configuration_and_request_authorisation_access_token(
            input_configuration
        )
        self._store_configuration()

    def _register_configuration_and_request_authorisation_access_token(
        self, configuration: ConnectionConfiguration
    ):
        self._register_connection_configuration(configuration)
        self._authorisation_access_token = self._request_authorisation_access_token()

    def _register_configuration_with_authorisation_access_token(
        self, configuration: ConnectionEstablished
    ):
        logger.debug("Configuration loaded successfully.")
        self._register_connection_established(configuration)
        self._authorisation_access_token = configuration["authorisation_access_token"]

    def _register_connection_established(self, configuration: ConnectionEstablished):
        self._register_connection_configuration(configuration)
        self._set_api_calls(api_path=configuration["api_path"])

    def _register_connection_configuration(
        self, configuration: Union[ConnectionConfiguration, ConnectionEstablished]
    ):
        self._user = User(
            id=configuration["user_id"],
            username=configuration["username"],
            api_key=configuration["api_key"],
        )

    @typechecked
    def send_post_auth_remote_api_call(self, path: str, data: Any) -> Tuple[Any, int]:
        logger.debug(f"Calling: {self._remote_server_api_url}{path}")
        header = {"Authorization": "Bearer " + self._authorisation_access_token}
        response = requests.post(
            f"{self._remote_server_api_url}{path}", json=data.copy(), headers=header
        )
        return self._process_response(response)

    @typechecked
    def send_get_auth_remote_api_call(self, path: str) -> Tuple[Any, int]:
        logger.debug(f"Calling: {self._remote_server_api_url}{path}")
        header = {"Authorization": "Bearer " + self._authorisation_access_token}
        response = requests.get(f"{self._remote_server_api_url}{path}", headers=header)
        return self._process_response(response)

    @typechecked
    def send_get_remote_call(self, path: str) -> Tuple[Any, int]:
        logger.debug(f"Calling: {self._remote_server_base_url}{path}")
        response = requests.get(f"{self._remote_server_base_url}{path}")
        return self._process_response(response)

    def _process_response(self, response: requests.Response) -> Tuple[Any, int]:
        custom_raise_for_status(response)
        try:
            return response.json(), response.status_code
        except JSONDecodeError:
            return response.text, response.status_code

    def _request_authorisation_access_token(self) -> str:
        assertion_payload: AssertionPayload = {
            **self._user.__dict__,
            "audience": self._audience_url,
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }

        encoded_assertion_payload = base64url_encode(
            json.dumps(assertion_payload, indent=2)
        )

        authorisation_request_payload = {
            "grantType": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": encoded_assertion_payload,
            "scope": "user profile",
        }

        logger.debug(f"Calling: {self._authorisation_server_api_call}")
        response: requests.Response = requests.post(
            self._authorisation_server_api_call, json=authorisation_request_payload
        )
        if response.status_code != 200 and response.status_code != 201:
            raise ValueError("Authorisation request failed: " + response.reason)

        access_token_response: AccessTokenResponse = response.json()
        logger.debug("Connection successfully established.")
        return access_token_response["accessToken"]
