from typing import Union

from requests.models import HTTPError, Response
from qiboconnection.config import logger

import json


class RemoteExecutionException(Exception):
    def __init__(self, message: Union[dict, str], status_code: int):
        super().__init__(message)
        self.status_code = status_code
        logger.error(f"RemoteExecutionException: {message}, {status_code}")


class ConnectionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


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
        http_error_msg = "%s Client Error: %s for url: %s" % (
            response.status_code,
            reason,
            response.url,
        )

    elif 500 <= response.status_code < 600:
        http_error_msg = "%s Server Error: %s for url: %s" % (
            response.status_code,
            reason,
            response.url,
        )

    if http_error_msg and response.text:
        try:
            json_text = json.loads(response.text)
            if "detail" in json_text:
                json_text["detail"] += f" {http_error_msg}"
            logger.error(json.dumps(json_text, indent=2))
            raise HTTPError(json.dumps(json_text, indent=2), response=response)
        except Exception:
            json_text_str = str(response.text)
            logger.error(json_text_str)
            raise HTTPError(json_text_str, response=response)

    if http_error_msg:
        raise HTTPError(http_error_msg, response=response)