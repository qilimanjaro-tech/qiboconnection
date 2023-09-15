""" Tests util functions """

import json

import pytest
from qibo.models.circuit import Circuit
from requests.models import Response

from qiboconnection.api_utils import deserialize_job_description
from qiboconnection.connection import ConnectionEstablished
from qiboconnection.models.job_data import JobType
from qiboconnection.util import (
    base64_decode,
    base64url_encode,
    load_config_file_to_disk,
    process_response,
    write_config_file_to_disk,
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
    assert json.loads(base64_decode(data)) == expected_decoded


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
    assert json.loads(base64_decode(data)) == expected_decoded


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


def test_deserialize_job_description(base64_qibo_circuit: str, base64_qililab_experiment: str):
    """Unit test of deserialize_job_description()"""

    assert isinstance(
        deserialize_job_description(base64_description=base64_qibo_circuit, job_type=JobType.CIRCUIT), Circuit
    )
    assert isinstance(
        deserialize_job_description(base64_description=base64_qililab_experiment, job_type=JobType.EXPERIMENT), dict
    )

    with pytest.raises(ValueError):
        deserialize_job_description(base64_description=base64_qibo_circuit, job_type="qiskit")
