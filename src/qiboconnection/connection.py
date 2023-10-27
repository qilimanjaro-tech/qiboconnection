# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Remote Connection """
import json
import os
from abc import ABC
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import TextIOWrapper
from typing import Any, List, Optional, TextIO, Tuple, Union

import jwt
import requests
from typeguard import typechecked

from qiboconnection import __version__ as VERSION  # pylint: disable=cyclic-import
from qiboconnection.config import get_environment, logger
from qiboconnection.errors import ConnectionException, HTTPError, RemoteExecutionException
from qiboconnection.models.user import User
from qiboconnection.typings.connection import ConnectionConfiguration, ConnectionEstablished
from qiboconnection.typings.requests import AssertionPayload
from qiboconnection.typings.responses import AccessTokenResponse
from qiboconnection.util import base64url_encode, process_response


def TIMEOUT():
    """Returns always the last TIMEOUT env var that the user might have set."""
    return int(os.getenv("QIBOCONNECTION_TIMEOUT", "10"))


def refresh_token_if_unauthorised(func):
    """Decorator that, if an HttpError is raised during a call, will retry to perform the call after
    updating the AccessToken.

    Args:
        func: function to decorate
    """

    def decorated(self: "Connection", *args, **kwargs):
        """decorated"""
        try:
            return func(self, *args, **kwargs)
        except HTTPError as ex:
            if ex.response.status_code not in [400, 401]:
                raise ex
            self.update_authorisation_using_refresh_token()
            return func(self, *args, **kwargs)

    return decorated


@dataclass
class Connection(ABC):  # pylint: disable=too-many-instance-attributes
    """Class to create a remote connection to a Qibo server"""

    @typechecked
    def __init__(
        self,
        configuration: ConnectionConfiguration,
        api_path: Optional[str] = None,
    ):
        self._environment = get_environment()
        self._api_path = api_path
        self._remote_server_api_url: str | None = None
        self._remote_server_base_url: str | None = None
        self._authorisation_server_api_call: str | None = None
        self._authorisation_server_refresh_api_call: str | None = None
        self._user_slack_id: Union[str, None] = None
        self._audience_url = f"{self._environment.audience_url}/api/v1"
        self._user: User | None = None
        self._authorisation_access_token: str | None = None
        self._authorisation_refresh_token: str | None = None
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
        self._authorisation_server_refresh_api_call = f"{self._remote_server_api_url}/authorisation-tokens/refresh"

    def _add_version_header(self, header):
        header["X-Client-Version"] = VERSION
        return header

    def _load_configuration(
        self,
        input_configuration: ConnectionConfiguration,
        api_path: Optional[str] = None,
    ) -> None:
        if api_path is None:
            raise ConnectionException("No api path provided.")
        self._set_api_calls(api_path=api_path)
        self._register_configuration_and_request_authorisation_access_token(input_configuration)
        self._load_user_id_from_token(access_token=self._authorisation_access_token)

    def _register_configuration_and_request_authorisation_access_token(self, configuration: ConnectionConfiguration):
        """
        Saves the connection info of user and calls urls, and requests for a new access token to be saved to
         self._authorisation_access_token.
        Args:
            configuration: configuration to save.
        """
        self._register_connection_configuration(configuration)
        self._authorisation_access_token, self._authorisation_refresh_token = self._request_authorisation_token()

    def _register_configuration_with_authorisation_tokens(self, configuration: ConnectionEstablished):
        """
        Saves the connection info of user and calls urls, and saves to self._authorisation_access_token the access
         token.
        Args:
            configuration: configuration to save.
        """
        logger.debug("Configuration loaded successfully.")
        self._register_connection_established(configuration)
        self._authorisation_access_token = configuration.authorisation_access_token
        self._authorisation_refresh_token = configuration.authorisation_refresh_token

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

    def update_device_availability(self, device_id: int, availability: str) -> Tuple[Any, int]:
        """Makes the request for updating a Device availability with a new value.

        Args:
            device_id (int): device identifier
            availability (str): device availability

        Returns:
            Tuple[Any, int]: Http Response
        """
        return self.send_put_auth_remote_api_call(path=f"/devices/{device_id}", data={"availability": availability})

    def send_message(self, channel_id: int, message: dict) -> Tuple[Any, int]:
        """Sends a message to a channel registered in the system

        Args:
            channel_id (int): channel identifier
            message (dict): message to send

        Returns:
            Tuple[Any, int]: Http response
        """
        return self.send_post_auth_remote_api_call(path=f"/messages?channel={channel_id}", data=message)

    @refresh_token_if_unauthorised
    @typechecked
    def send_post_auth_remote_api_call(self, path: str, data: Any, timeout: int | None = None) -> Tuple[Any, int]:
        """HTTP POST REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            data (Any): data to send
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        response = requests.post(
            f"{self._remote_server_api_url}{path}", json=data.copy(), headers=header, timeout=timeout
        )
        return process_response(response)

    def send_file(
        self, channel_id: int, file: TextIOWrapper, filename: str, timeout: int | None = None
    ) -> Tuple[Any, int]:
        """Sends a file to a channel registered in the system

        Args:
            channel_id (int): channel identifier
            file (TextIOWrapper): file to send
            filename (str): file name
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        return self.send_post_file_auth_remote_api_call(
            path=f"/files?channel={channel_id}", file=file, filename=filename, timeout=timeout
        )

    @refresh_token_if_unauthorised
    @typechecked
    def send_put_auth_remote_api_call(self, path: str, data: Any, timeout: int | None = None) -> Tuple[Any, int]:
        """HTTP PUT REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            data (Any): data to send
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        response = requests.put(
            f"{self._remote_server_api_url}{path}", json=data.copy(), headers=header, timeout=timeout
        )
        return process_response(response)

    @refresh_token_if_unauthorised
    @typechecked
    def send_post_file_auth_remote_api_call(
        self, path: str, file: Union[TextIOWrapper, TextIO], filename: str, timeout: int | None = None
    ) -> Tuple[Any, int]:
        """HTTP POST REST API authenticated call to send a file to remote server

        Args:
            path (str): path to add to the remote server api url
            file (Union[TextIOWrapper, TextIO]): file to send
            filename (str): file to send
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        packed_file = {"file": (filename, file)}
        response = requests.post(
            f"{self._remote_server_api_url}{path}", files=packed_file, headers=header, timeout=timeout
        )
        return process_response(response)

    @refresh_token_if_unauthorised
    @typechecked
    def send_get_auth_remote_api_call(
        self, path: str, params: dict | None = None, timeout: int | None = None
    ) -> Tuple[Any, int]:
        """HTTP GET REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            params (str): dict of parameters to be encoded as url query params
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        response = requests.get(f"{self._remote_server_api_url}{path}", headers=header, params=params, timeout=timeout)

        if response.status_code != 200:
            error_details = response.json()
            if "detail" in error_details and "does not exist" in error_details["detail"]:
                raise RemoteExecutionException("The job does not exist!", status_code=400)

        return process_response(response)

    @refresh_token_if_unauthorised
    @typechecked
    def send_get_auth_remote_api_call_all_pages(
        self, path: str, params: dict | None = None, timeout: int | None = None
    ) -> List[Tuple[Any, int]]:
        """HTTP GET REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            params (str): dict of parameters to be encoded as url query params
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        next_url = f"{self._remote_server_api_url}{path}"
        responses = []
        while "None" not in next_url:
            response = requests.get(next_url, headers=header, params=params, timeout=timeout)
            json_content, status_code = process_response(response)
            next_url = json_content["links"]["next"]
            responses.append((json_content, status_code))
        return responses

    @refresh_token_if_unauthorised
    @typechecked
    def send_delete_auth_remote_api_call(self, path: str, timeout: int | None = None) -> Tuple[Any, int]:
        """HTTP DELETE REST API authenticated call to remote server

        Args:
            path (str): path to add to the remote server api url
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        header = self._add_version_header({"Authorization": f"Bearer {self._authorisation_access_token}"})
        response = requests.delete(f"{self._remote_server_api_url}{path}", headers=header, timeout=timeout)

        if response.status_code != 204:
            error_details = response.json()
            if "detail" in error_details and "does not exist" in error_details["detail"]:
                raise RemoteExecutionException("The job does not exist!", status_code=400)
            response.raise_for_status()

        return ("", 204)

    @refresh_token_if_unauthorised
    @typechecked
    def send_get_remote_call(self, path: str, timeout: int | None = None) -> Tuple[Any, int]:
        """HTTP GET REST API call to remote server (without authentication)

        Args:
            path (str): path to add to the remote server api url
            timeout (int): time to wait. If not provided, a default will be used.

        Returns:
            Tuple[Any, int]: Http response
        """
        timeout = timeout or TIMEOUT()
        logger.debug("Calling: %s%s", self._remote_server_api_url, path)
        response = requests.get(
            f"{self._remote_server_base_url}{path}", timeout=timeout, headers=self._add_version_header({})
        )
        return process_response(response)

    def _request_authorisation_token(self, timeout: int | None = None):
        """
        Builds assertion payload with user info, encodes it and uses it to POST the server for a new Access Token.
        Args:
            timeout (int): time to wait. If not provided, a default will be used.
        Returns: str tuple with new Access  and Refresh Tokens.
        """
        timeout = timeout or TIMEOUT()
        assertion_payload = AssertionPayload(
            **self._user.__dict__,  # type: ignore
            audience=self._audience_url,
            iat=int(datetime.now(timezone.utc).timestamp()),
        )

        encoded_assertion_payload = base64url_encode(json.dumps(asdict(assertion_payload), indent=2))

        authorisation_request_payload = {
            "grantType": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": encoded_assertion_payload,
            "scope": "user profile",
        }

        if self._authorisation_server_api_call is None:
            raise ValueError("Authorisation server api call is required")
        logger.debug("Calling: %s", self._authorisation_server_api_call)
        response: requests.Response = requests.post(
            self._authorisation_server_api_call,
            json=authorisation_request_payload,
            timeout=timeout,
            headers=self._add_version_header({}),
        )
        if response.status_code not in [200, 201]:
            try:
                json_content = json.loads(response.content)
                detail = json_content["detail"]
            except (TypeError, KeyError, json.JSONDecodeError):
                detail = ""
            reason_text = f" Reason: {response.reason}." if response.reason else ""
            details_text = f" Details: {detail}." if detail else ""
            raise ValueError(f"Authorisation request failed.{reason_text}{details_text}")

        access_token_response: AccessTokenResponse = AccessTokenResponse(**response.json())
        logger.debug("Connection successfully established.")

        return access_token_response.accessToken, access_token_response.refreshToken

    def update_authorisation_using_refresh_token(self, timeout: int | None = None):
        """Updates the saved access token sending the request token. For this, it
        builds assertion payload with user info, encodes it and uses it to POST the server for a new Access Token.
        Args:
            timeout (int): time to wait. If not provided, a default will be used.
        Returns:
            str with a new Access Token
        """
        timeout = timeout or TIMEOUT()

        if self._authorisation_server_refresh_api_call is None:
            raise ValueError("Authorisation server api call is required")
        logger.debug("Calling: %s", self._authorisation_server_refresh_api_call)
        response: requests.Response = requests.post(
            self._authorisation_server_refresh_api_call,
            json={},
            headers=self._add_version_header({"Authorization": f"Bearer {self._authorisation_refresh_token}"}),
            timeout=timeout,
        )
        if response.status_code not in [200, 201]:
            raise ValueError(f"Authorisation request failed: {response.reason},{response.status_code}")
        logger.debug("Connection successfully renewed.")
        self._authorisation_access_token = AccessTokenResponse(**response.json()).accessToken
