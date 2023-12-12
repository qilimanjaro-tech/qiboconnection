""" Tests util functions """

import json

import pytest
from qibo.models.circuit import Circuit
from requests.models import Response

from qiboconnection.api_utils import deserialize_job_description
from qiboconnection.typings.enums import JobType
from qiboconnection.typings.responses.job_response import JobResponse
from qiboconnection.util import base64_decode, base64url_encode, from_kwargs, process_response


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


def test_process_response(response: Response):
    """Test that process_response() recovers the correct parameters (text and status_code)."""

    processed_response = process_response(response=response)

    assert processed_response[0] == json.loads(response.text)
    assert processed_response[1] == response.status_code


def test_process_response_non_json(response_plain_text: Response):
    """Test that process_response() recovers the correct parameters (text and status_code)."""

    processed_response = process_response(response=response_plain_text)

    assert processed_response[0] == response_plain_text.text
    assert processed_response[1] == response_plain_text.status_code


def test_deserialize_job_description(
    base64_qibo_circuit: str, base64_qibo_circuits: str, base64_qililab_experiment: str
):
    """Unit test of deserialize_job_description()"""

    assert isinstance(
        deserialize_job_description(base64_description=base64_qibo_circuit, job_type=JobType.CIRCUIT), Circuit
    )
    assert isinstance(
        deserialize_job_description(base64_description=base64_qililab_experiment, job_type=JobType.EXPERIMENT), dict
    )

    assert deserialize_job_description(base64_description=base64_qibo_circuit, job_type="qiskit") is None
    assert isinstance(
        deserialize_job_description(base64_description=base64_qibo_circuits, job_type=JobType.CIRCUIT), list
    )


def test_from_kwargs():
    "Test of from_kwargs methods requires all explicitly typed attributes but accepts new ones."
    assert isinstance(
        from_kwargs(
            JobResponse,
            **{
                "user_id": 1,
                "device_id": 2,
                "description": "Job Description",
                "job_id": 1001,
                "queue_position": 5,
                "status": "Completed",
                "result": "Job Result",
                "number_shots": 10,
                "job_type": "whatever",
                "extra_arg": "Extra Argument",
            }
        ),
        JobResponse,
    )

    with pytest.raises(TypeError):
        isinstance(
            from_kwargs(
                JobResponse, **{"user_id": 1, "device_id": 2, "number_shots": 10, "extra_arg": "Extra Argument"}
            ),
            JobResponse,
        )
