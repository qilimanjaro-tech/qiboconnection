""" Utility functions """
import io
import json
import os
import pickle  # nosec - temporary bandit ignore
from base64 import urlsafe_b64decode, urlsafe_b64encode
from json.decoder import JSONDecodeError
from typing import Any, List, Tuple

import numpy as np
import requests
from qibo.abstractions.states import AbstractState

from qiboconnection.errors import custom_raise_for_status
from qiboconnection.typings.connection import ConnectionEstablished

QIBO_CONFIG_DIR = "qibo_configuration"
QIBO_CONFIG_FILE = ".user_configuration.json"


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


def base64url_decode(encoded_data: str) -> Any:
    """Decodes a base64 encoded string

    Args:
        encoded_data (str): a base64 encoded string

    Returns:
        Any: The data decoded
    """
    return json.loads(urlsafe_b64decode(encoded_data).decode("utf-8"))


def write_config_file_to_disk(config_data: ConnectionEstablished) -> None:
    """Write the Connection configuration data to a local file

    Args:
        config_data (ConnectionEstablished): Connection configuration data
    """
    current_dir = os.getcwd()
    os.chdir(current_dir)
    if not os.path.isdir(QIBO_CONFIG_DIR):
        os.mkdir(QIBO_CONFIG_DIR)
    os.chdir(QIBO_CONFIG_DIR)

    with open(QIBO_CONFIG_FILE, "w", encoding="utf-8") as config_file:
        json.dump(obj=vars(config_data), fp=config_file, indent=2)
    os.chdir("..")


def load_config_file_to_disk() -> ConnectionEstablished:
    """Load a Connection configuration data from a local file

    Returns:
        ConnectionEstablished: Connection configuration data
    """
    current_dir = os.getcwd()
    os.chdir(current_dir)
    os.chdir(QIBO_CONFIG_DIR)
    with open(QIBO_CONFIG_FILE, encoding="utf-8") as config_file:
        os.chdir("..")
        return ConnectionEstablished(**json.load(fp=config_file))


def decode_results_from_program(http_response: str) -> List[AbstractState | float]:
    """Decode the results from the program execution

    Args:
        http_response (str): the execution results as an Http Response

    Returns:
        List[AbstractState]: a Qibo AbstractState
    """
    decoded_results = base64url_decode(http_response)
    if not isinstance(decoded_results, list):
        raise ValueError(f"decoded results is not a list. type: {type(decoded_results)}")
    if len(decoded_results) <= 0:
        raise ValueError("decoded results does not contain results.")
    if isinstance(decoded_results[0], float):
        return decoded_results
    return [np.load(urlsafe_b64decode(decoded_result)) for decoded_result in decoded_results]


def decode_results_from_circuit(http_response: str) -> AbstractState:
    """Decode the results from the Qibo circuit execution

    Args:
        http_response (str): the execution results as an Http Response

    Returns:
        List[AbstractState]: a Qibo AbstractState
    """
    decoded_result_str = urlsafe_b64decode(http_response)
    result_bytes = io.BytesIO(decoded_result_str)
    return pickle.loads(result_bytes.getbuffer())  # nosec - temporary bandit ignore


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
