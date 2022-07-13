""" Tests util functions """

import json

import pytest
from requests.models import Response

from qiboconnection.connection import ConnectionEstablished
from qiboconnection.util import (
    base64url_decode,
    base64url_encode,
    load_config_file_to_disk,
    process_response,
    write_config_file_to_disk,
)


@pytest.fixture(name="response")
def fixture_response() -> Response:
    """Creates an status_code 200 Response object with demo values

    Returns:
        Response: response object
    """
    response = Response()
    response.status_code = 200
    response.url = "server/api"
    response._content = json.dumps({"DEMO": "200"}).encode("utf8")
    return response


@pytest.fixture(name="connection_established")
def fixture_connection_established() -> ConnectionEstablished:
    """Creates a ConnectionEstablished object with demo values

    Returns:
        ConnectionEstablished: ConnectionEstablished instance
    """
    return ConnectionEstablished(
        api_key="DEMO_KEY", api_path="DEMO_PATH", authorisation_access_token="DEMO_TOKEN", username="DEMO_USERNAME"
    )


def test_base64url_encode():
    """Tests the base64url_encode() function."""
    payload = {
        "name": "alg001",
        "type": "Gate-Based Circuit",
        "options": {"number_qubits": 2, "initial_value": "zero"},
    }
    expected_encoded = "eyJuYW1lIjogImFsZzAwMSIsICJ0eXBlIjogIkdhdGUtQmFzZWQgQ2lyY3VpdCIsICJvcHRpb25zIjogeyJudW1iZXJfcXViaXRzIjogMiwgImluaXRpYWxfdmFsdWUiOiAiemVybyJ9fQ=="
    assert base64url_encode(payload) == expected_encoded


def test_base64url_encode_list():
    """Tests the base64url_encode() function providing it a list of dicts."""
    payload = [
        {
            "name": "alg001",
            "type": "Gate-Based Circuit",
            "options": {"number_qubits": 2, "initial_value": "zero"},
        }
    ]
    expected_encoded = "W3sibmFtZSI6ICJhbGcwMDEiLCAidHlwZSI6ICJHYXRlLUJhc2VkIENpcmN1aXQiLCAib3B0aW9ucyI6IHsibnVtYmVyX3F1Yml0cyI6IDIsICJpbml0aWFsX3ZhbHVlIjogInplcm8ifX1d"
    assert base64url_encode(json.dumps(payload)) == expected_encoded


def test_base64url_decode():
    """Test the base64url_decode() function"""
    data = "WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ=="
    expected_decoded = [0.1, 0.1, 0.1, 0.1, 0.1]
    assert base64url_decode(data) == expected_decoded


def test_base64url_decode_list():
    """Test the base64url_decode() function providing it a list of dicts."""
    data = "W3sibmFtZSI6ICJhbGcwMDEiLCAidHlwZSI6ICJHYXRlLUJhc2VkIENpcmN1aXQiLCAib3B0aW9ucyI6IHsibnVtYmVyX3F1Yml0cyI6IDIsICJpbml0aWFsX3ZhbHVlIjogInplcm8ifX1d"
    expected_decoded = [
        {
            "name": "alg001",
            "type": "Gate-Based Circuit",
            "options": {"number_qubits": 2, "initial_value": "zero"},
        }
    ]
    assert base64url_decode(data) == expected_decoded


def test_save_and_load_config_to_disk(connection_established: ConnectionEstablished):
    """Test write_config_file_to_disk() loads the correct ConnectionEstablished object."""
    write_config_file_to_disk(config_data=connection_established)
    recovered_config_data = load_config_file_to_disk()
    assert connection_established == recovered_config_data


def test_process_response(response: Response):
    """Test that process_response() recovers the correct parameters (text and status_code)."""

    processed_response = process_response(response=response)

    assert processed_response[0] == json.loads(response.text)
    assert processed_response[1] == response.status_code
