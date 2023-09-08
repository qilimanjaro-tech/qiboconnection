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

""" Handling Error Utility Functions """
import json
from typing import Union

from requests.models import HTTPError, Response

from qiboconnection.config import logger


class RemoteExecutionException(Exception):
    """Exception raised when calling remote server

    Args:
        Exception (Exception): Inherit from Exception
    """

    def __init__(self, message: Union[dict, str], status_code: int):
        super().__init__(message)
        self.status_code = status_code
        logger.error("RemoteExecutionException: %s, %i", message, status_code)


class ConnectionException(Exception):
    """Exception raised when establishing the connection to a remote server

    Args:
        Exception (Exception): Inherit from Exception
    """


def custom_raise_for_status(response: Response):
    """Raises :class:`HTTPError`, if one occurred."""

    http_error_msg = ""
    if isinstance(response.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = response.reason.decode("iso-8859-1")
    else:
        reason = response.reason

    if 400 <= response.status_code < 500:
        http_error_msg = f"{response.status_code} Client Error: {reason} for url: {response.url}"

    elif 500 <= response.status_code < 600:
        http_error_msg = f"{response.status_code} Server Error: {reason} for url: {response.url}"

    if http_error_msg and response.text:
        try:
            json_text = json.loads(response.text)
            if "detail" in json_text:
                json_text["detail"] += f" {http_error_msg}"
            logger.error(json.dumps(json_text, indent=2))
            raise HTTPError(json.dumps(json_text, indent=2), response=response)
        except Exception as ex:
            json_text_str = str(response.text)
            logger.error(json_text_str)
            raise HTTPError(json_text_str, response=response) from ex

    if http_error_msg:
        raise HTTPError(http_error_msg, response=response)
