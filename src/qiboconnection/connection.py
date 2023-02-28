""" Remote Connection """
import json
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from io import TextIOWrapper
from typing import Any, List, Optional, TextIO, Tuple, Union

import jwt
import requests
from typeguard import typechecked

from qiboconnection.config import get_environment, logger
from qiboconnection.errors import ConnectionException
from qiboconnection.typings.auth_config import AccessTokenResponse, AssertionPayload
from qiboconnection.typings.connection import (
    ConnectionConfiguration,
    ConnectionEstablished,
)
from qiboconnection.user import User
from qiboconnection.util import (
    base64url_encode,
    load_config_file_to_disk,
    process_response,
    write_config_file_to_disk,
)


@dataclass
class Connection(ABC):
    """Class to create a remote connection to a Qibo server"""

    @typechecked
    def __init__(
        self,
        configuration: Optional[ConnectionConfiguration | None] = None,
        api_path: Optional[str] = None,
    ):
        self._environment = get_environment()
        self._api_path = api_path
        self._remote_server_api_url: str | None = None
        self._remote_server_base_url: str | None = None
        self._authorisation_server_api_call: str | None = None
        self._user_slack_id: Union[str, None] = None
        self._audience_url = f"{self._environment.audience_url}/api/v1"
        self._user: User | None = None
        self._authorisation_access_token: str | None = None
        self._load_configuration(configuration, api_path)

    @property
    def user(self) -> User:
        """Gets User

        Returns:
            User: User associated to the connection
        """
        if self._user is None:
            raise ValueError("user not defined")
        return self._user

    @property
    def username(self) -> str:
        """Gets user name

        Returns:
            str: user name associated to the connection
        """
        if self._user is None:
            raise ValueError("user not defined")
        return self._user.username

    @property
    def _user_id(self) -> int | None:
        """Gets user name

        Returns:
            str: user name associated to the connection
        """
        if self._user is None:
            raise ValueError("user not defined")
        return self._user.user_id

    @_user_id.setter
    def _user_id(self, new_id) -> None:
        """Sets user name

        Returns:
            None
        """
        if self._user is None:
            raise ValueError("user not defined")
        self._user.user_id = new_id

    def _load_user_id_from_token(self, access_token):
        self._user_id = jwt.decode(access_token, options={"verify_signature": False})["user_id"]

    @property
    def user_slack_id(self) -> str:
        """Gets user slack id

        Returns:
            str: user slack id associated to the user's connection
        """
        if self._user_slack_id is None:
            self._user_slack_id = self._retrieve_user_slack_id()
        return self._user_slack_id

    def _retrieve_user_slack_id(self) -> str:
        """
        Uses user info to recover the id and make a request to retrieve from server for the User's Slack Id.
        Returns:
        """
        if self._user is None:
            raise ValueError("user not defined")
        user_response, response_status = self.send_get_auth_remote_api_call(path=f"/users/{self._user_id}")
        if response_status != 200:
            raise ValueError(f"Error getting user: {response_status}")
        if "slack_id" not in user_response or user_response["slack_id"] is None:
            return ""
        return user_response["slack_id"]

    def _set_api_calls(self, api_path: str):
        """
        Builds api path, remote server urls and auth server url from env info and api_path kwarg.
        Args:
            api_path: path to api, with leading slash (/).

        Returns:

        """
        self._api_path = api_path
        self._remote_server_api_url = f"{self._environment.qibo_quantum_service_url}{api_path}"
        self._remote_server_base_url = f"{self._environment.qibo_quantum_service_url}"
        self._authorisation_server_api_call = f"{self._remote_server_api_url}/authorisation-tokens"

    def _store_configuration(self) -> None:
        """
        Saves the provided info in the Connection() instance creation to a file.
        """
        logger.info("Storing personal qibo configuration...")
        if self._api_path is None:
            raise ValueError("API path not specified")
        if self._authorisation_access_token is None:
            raise ValueError("Authorisation access token not specified")
        config_data = ConnectionEstablished(
            **self._user.__dict__,
            authorisation_access_token=self._authorisation_access_token,
            api_path=self._api_path,
        )

        write_config_file_to_disk(config_data=config_data)

    def _load_configuration(
        self,
        input_configuration: Optional[ConnectionConfiguration] = None,
        api_path: Optional[str] = None,
    ) -> None:
        if input_configuration is None:
            try:
                self._register_configuration_with_authorisation_access_token(load_config_file_to_disk())
                return
            except FileNotFoundError as ex:
                raise ConnectionException(
                    "No connection configuration found. Please provide a new configuration."
                ) from ex

        if api_path is None:
            raise ConnectionException("No api path provided.")
        self._set_api_calls(api_path=api_path)
        self._register_configuration_and_request_authorisation_access_token(input_configuration)
        self._load_user_id_from_token(access_token=self._authorisation_access_token)
        self._store_configuration()

    def _register_configuration_and_request_authorisation_access_token(self, configuration: ConnectionConfiguration):
        """
        Saves the connection info of user and calls urls, and requests for a new access token to be saved to
         self._authorisation_access_token.
        Args:
            configuration: configuration to save.
        """
        self._register_connection_configuration(configuration)
        self._authorisation_access_token = self._request_authorisation_access_token()

    def _register_configuration_with_authorisation_access_token(self, configuration: ConnectionEstablished):
        """
        Saves the connection info of user and calls urls, and saves to self._authorisation_access_token the access
         token.
        Args:
            configuration: configuration to save.
        """
        logger.debug("Configuration loaded successfully.")
        self._register_connection_established(configuration)
        self._authorisation_access_token = configuration.authorisation_access_token

    def _register_connection_established(self, configuration: ConnectionEstablished):
        """
        Saves to self._user the provided configuration, and sets the api calls using the api_path inside Configuration.
        Args:
            configuration: configuration to save.
        """
        self._register_connection_configuration(configuration)
        self._set_api_calls(api_path=configuration.api_path)

    def _register_connection_configuration(self, configuration: Union[ConnectionConfiguration, ConnectionEstablished]):
        self._user = User(
            user_id=configuration.user_id,
            username=configuration.username,
            api_key=configuration.api_key,
        )

    def update_device_status(self, device_id: int, status: str) -> Tuple[Any, int]:
        """Update a Device status

        Args:
            device_id (int): device identifier
            status (str): device status

        Returns:
            Tuple[Any, int]: Http Response
        """
        return self.send_put_auth_remote_api_call(path=f"/devices/{device_id}", data={"status": status})

    def send_message(self, channel_id: int, message: dict) -> Tuple[Any, int]:
        """Sends a message to a channel registered in the system

        Args:
            channel_id (int): channel identifier
            message (dict): message to send

        Returns:
            Tuple[Any, int]: Http response
        """
        return self.send_post_auth_remote_api_call(path=f"/messages?channel={channel_id}", data=message)

    def send_file(self, channel_id: int, file: TextIOWrapper, filename: str) -> Tuple[Any, int]:
        """Sends a file to a channel registered in the system

        Args:
            channel_id (int): channel identifier
            file (TextIOWrapper): file to send
            filename (str): file name

        Returns:
            Tuple[Any, int]: Http response
        """
        return self.send_post_file_auth_remote_api_call(
            path=f"/files?channel={channel_id}", file=file, filename=filename
        )

    @typechecked
    def send_put_auth_remote_api_call(self, path: str, data: Any) -> Tuple[Any, int]:
        """HTTP PUT REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            data (Any): data to send

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        response = requests.put(f"{self._remote_server_api_url}{path}", json=data.copy(), headers=header)
        return process_response(response)

    @typechecked
    def send_post_auth_remote_api_call(self, path: str, data: Any) -> Tuple[Any, int]:
        """HTTP POST REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            data (Any): data to send

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        response = requests.post(f"{self._remote_server_api_url}{path}", json=data.copy(), headers=header)
        return process_response(response)

    @typechecked
    def send_post_file_auth_remote_api_call(
        self, path: str, file: Union[TextIOWrapper, TextIO], filename: str
    ) -> Tuple[Any, int]:
        """HTTP POST REST API authenticated call to send a file to remote server

        Args:
            path (str): path to add to the remote server api url
            file (Union[TextIOWrapper, TextIO]): file to send
            filename (str): file to send

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        packed_file = {"file": (filename, file)}
        response = requests.post(f"{self._remote_server_api_url}{path}", files=packed_file, headers=header)
        return process_response(response)

    @typechecked
    def send_get_auth_remote_api_call(self, path: str, params: dict | None = None) -> Tuple[Any, int]:
        """HTTP GET REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            params (str): dict of parameters to be encoded as url query params

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        response = requests.get(f"{self._remote_server_api_url}{path}", headers=header, params=params)
        return process_response(response)

    @typechecked
    def send_get_auth_remote_api_call_all_pages(self, path: str, params: dict | None = None) -> List[Tuple[Any, int]]:
        """HTTP GET REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            params (str): dict of parameters to be encoded as url query params

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        next_url = f"{self._remote_server_api_url}{path}"
        responses = []
        while "None" not in next_url:
            response = requests.get(next_url, headers=header, params=params)
            json_content, status_code = process_response(response)
            next_url = json_content["links"]["next"]
            responses.append((json_content, status_code))
        return responses

    @typechecked
    def send_delete_auth_remote_api_call(self, path: str) -> Tuple[Any, int]:
        """HTTP DELETE REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = {"Authorization": f"Bearer {self._authorisation_access_token}"}
        response = requests.delete(f"{self._remote_server_api_url}{path}", headers=header)
        return process_response(response)

    @typechecked
    def send_get_remote_call(self, path: str) -> Tuple[Any, int]:
        """HTTP GET REST API call to remote server (without authentication)

        Args:
            path (str): path to add to the remote server api url

        Returns:
            Tuple[Any, int]: Http response
        """
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        response = requests.get(f"{self._remote_server_base_url}{path}")
        return process_response(response)

    def _request_authorisation_access_token(self) -> str:
        """
        Builds assertion payload with user info, encodes it and uses it to POST the server for a new Access Token.
        Returns: str witha  new Access Token.
        """
        assertion_payload: AssertionPayload = {
            **self._user.__dict__,  # type: ignore
            "audience": self._audience_url,
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }

        encoded_assertion_payload = base64url_encode(json.dumps(assertion_payload, indent=2))

        authorisation_request_payload = {
            "grantType": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": encoded_assertion_payload,
            "scope": "user profile",
        }

        if self._authorisation_server_api_call is None:
            raise ValueError("Authorisation server api call is required")
        logger.debug("Calling: %s", self._authorisation_server_api_call)
        response: requests.Response = requests.post(
            self._authorisation_server_api_call, json=authorisation_request_payload
        )
        if response.status_code not in [200, 201]:
            raise ValueError(f"Authorisation request failed: {response.reason}")

        access_token_response: AccessTokenResponse = AccessTokenResponse(**response.json())
        logger.debug("Connection successfully established.")

        return access_token_response.accessToken
