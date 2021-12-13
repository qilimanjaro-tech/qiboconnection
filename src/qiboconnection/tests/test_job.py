""" Tests methods for job """
from typing import cast
from qiboconnection.algorithm import Algorithm, AlgorithmOptions
from qiboconnection.devices.device import Device
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.job_result import JobResult
from qiboconnection.job import Job
from qiboconnection.typings.algorithm import AlgorithmType, InitialValue
from qiboconnection.user import User
from qiboconnection.typings.job import JobRequest, JobResponse, JobStatus
from .data import simulator_device_inputs


def test_job_creation():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    user = User(id=1, username="test-user", api_key="000-3333")
    device = SimulatorDevice(device_input=simulator_device_inputs[0])
    job_status = JobStatus.completed
    job_result = JobResult(http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==")
    job = Job(
        algorithm=algorithm,
        user=user,
        device=cast(Device, device),
        job_status=job_status,
        job_result=job_result,
        id=23,
    )
    assert isinstance(job, Job)


def test_job_creation_default_values():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    user = User(id=1, username="test-user", api_key="000-3333")
    device = SimulatorDevice(device_input=simulator_device_inputs[0])
    job = Job(algorithm=algorithm, user=user, device=cast(Device, device))
    assert isinstance(job, Job)
    assert job._status == JobStatus.not_sent
    assert job._result == None
    assert job.id == 0


def test_job_request():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    user = User(id=1, username="test-user", api_key="000-3333")
    device = SimulatorDevice(device_input=simulator_device_inputs[0])
    job_status = JobStatus.completed
    job = Job(
        algorithm=algorithm,
        user=user,
        device=cast(Device, device),
        job_status=job_status,
        id=23,
    )
    expected_job_request = JobRequest(
        {
            "user_id": user.id,
            "device_id": device.id,
            "description": "eyJuYW1lIjogImFsZzAwMSIsICJ0eXBlIjogIkdhdGUtQmFzZWQgQ2lyY3VpdCIsICJvcHRpb25zIjogeyJudW1iZXJfcXViaXRzIjogMiwgImluaXRpYWxfdmFsdWUiOiAiemVybyJ9fQ==",
        }
    )
    assert isinstance(job, Job)
    assert job.job_request == expected_job_request


def test_update_with_job_response():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    user = User(id=1, username="test-user", api_key="000-3333")
    device = SimulatorDevice(device_input=simulator_device_inputs[0])
    job_status = JobStatus.pending
    job = Job(
        algorithm=algorithm,
        user=user,
        device=cast(Device, device),
        job_status=job_status,
        id=23,
    )
    job_response = JobResponse(
        user_id=user.id,
        device_id=device.id,
        description="",
        job_id=job.id,
        queue_position=0,
        status=JobStatus.completed,
        result="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
    )
    job.update_with_job_response(job_response=job_response)
    assert job.result == [0.1, 0.1, 0.1, 0.1, 0.1]
