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

"""Utility functions"""

import base64
import gzip
import json
import logging
from base64 import urlsafe_b64decode, urlsafe_b64encode
from inspect import signature
from json.decoder import JSONDecodeError
from typing import Any, List, Tuple

import requests

from qiboconnection.errors import custom_raise_for_status

logger = logging.getLogger()


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


def decode_results_from_qprogram(http_response: str) -> dict:
    """Decode the results from QProgram execution.

    Args:
        http_response (str): the execution results as an Http Response

    Returns:
        dict: qprogram results

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


def compress_any(any_obj, encoding="utf-8") -> dict:
    """
    Transforms any json-serializable object into a compressed string.
    :param any_obj: object to compress
    :param encoding: encoding to use for the byte representation
    :return:
    """

    encoded_data = json.dumps(any_obj).encode(encoding)
    compressed_data = base64.b64encode(gzip.compress(encoded_data)).decode()
    return {"data": compressed_data, "encoding": encoding, "compression": "gzip"}


def decompress_any(data: str, **kwargs) -> dict:
    """
    Decompresses a compressed string into its original datatype.
    :param data: compressed data containing a json to extract a dictionary from
    :return:
    """

    data_bin = base64.urlsafe_b64decode(data)
    data_decompressed = json.loads(gzip.decompress(data_bin))

    return data_decompressed


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
