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

""" Utility functions """
import base64
import binascii
import io
import json
import pickle  # nosec - temporary bandit ignore
from base64 import urlsafe_b64decode, urlsafe_b64encode
from inspect import signature
from json.decoder import JSONDecodeError
from typing import Any, List, Tuple

import requests
from qibo.states import CircuitResult

from qiboconnection.errors import custom_raise_for_status


def base64url_encode(payload: dict | bytes | str) -> str:
    """Encode a given payload to base64 string

    Args:
        payload ( dict | bytes | str): data to be encoded

    Returns:
        str: base64 encoded data
    """
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    if not isinstance(payload, bytes):
        payload = payload.encode("utf-8")
    return urlsafe_b64encode(payload).decode("utf-8")


def base64_decode(encoded_data: str) -> str:
    """Decodes a base64 encoded string

    Args:
        encoded_data (str): a base64 encoded string

    Returns:
        Any: The data decoded
    """
    return urlsafe_b64decode(encoded_data).decode("utf-8")


def decode_jsonified_dict(http_response: str) -> dict:
    """Decodes results that have been jsonified and base64 encoded."""
    return json.loads(urlsafe_b64decode(http_response))


def _decode_pickled_results(http_response: str) -> Any:
    """Decodes results that have been pickled and base64 encoded."""
    decoded_result_str = urlsafe_b64decode(http_response)
    result_bytes = io.BytesIO(decoded_result_str)
    return pickle.loads(result_bytes.getbuffer())  # nosec - temporary bandit ignore


def decode_results_from_circuit(http_response: str) -> CircuitResult | dict:
    """Decode the results from the circuit execution. Ideally we should always expect dictionaries here, but for qibo we
    are still serializing `CircuitResult`s that must be pickled.

    Args:
        http_response (str): the execution results as an Http Response

    Returns:
        List[CircuitResult]: a Qibo CircuitResult
    """
    try:
        return decode_jsonified_dict(http_response)
    except (binascii.Error, UnicodeDecodeError, JSONDecodeError):
        return _decode_pickled_results(http_response)


def decode_results_from_qprogram(http_response: str) -> dict:
    """Decode the results from the Qililab experiment execution

    Args:
        http_response (str): the execution results as an Http Response

    Returns:
        dict: object containing a serialized representation of a qililab Results object
    """
    return decode_jsonified_dict(http_response)


def process_response(response: requests.Response) -> Tuple[Any, int]:
    """Process an Http Response to check for errors

    Args:
        response (requests.Response): Http Response

    Returns:
        Tuple[Any, int]: Data from the Response, and status code
    """
    custom_raise_for_status(response)
    try:
        return response.json(), response.status_code
    except JSONDecodeError:
        return response.text, response.status_code


def jsonify_dict_and_base64_encode(object_to_encode: dict) -> str:
    """
    Jsonifies a given dict, encodes it to bytes assuming utf-8, and encodes that byte obj to an url-save base64 str
    """
    return str(base64.urlsafe_b64encode(json.dumps(object_to_encode).encode("utf-8")), "utf-8")


def jsonify_list_with_str_and_base64_encode(object_to_encode: List[str]) -> str:
    """Encodes a given list of strings to bytes assuming utf-8, and encodes that byte-array to an url-save base64 str"""
    return str([str(base64.urlsafe_b64encode(s.encode("utf-8")), "utf-8") for s in object_to_encode])


def unzip(zipped_list: List[Tuple[Any, Any]]):
    """Inverse of the python builtin `zip` operation"""
    return tuple(zip(*zipped_list))


def from_kwargs(cls, **kwargs: dict):
    """
    Create an instance of the class by extracting attributes from keyword arguments.

    This method takes keyword arguments and initializes an instance of the class
    with attributes that match the class's constructor parameters. Any additional
    keyword arguments that don't correspond to class attributes are assigned as
    attributes to the created instance.

    Args:
        cls: The class (typically, the class that defines this method).
        **kwargs: Keyword arguments to initialize the instance.

    Returns:
        An instance of the class with attributes initialized from the keyword
        arguments.
    """
    cls_fields = set(signature(cls).parameters)
    native_args, new_args = {}, {}

    for name, val in kwargs.items():
        if name in cls_fields:
            native_args[name] = val
        else:
            new_args[name] = val

    ret = cls(**native_args)

    for new_name, new_val in new_args.items():
        setattr(ret, new_name, new_val)
    return ret
