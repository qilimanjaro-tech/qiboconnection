""" Tests methods for job """

from typing import cast

import pytest
from qibo import gates
from qibo.models.circuit import Circuit

from qiboconnection.devices.device import Device
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.job import Job
from qiboconnection.job_result import JobResult
from qiboconnection.typings.algorithm import (
    AlgorithmDefinition,
    AlgorithmName,
    AlgorithmOptions,
    AlgorithmType,
    InitialValue,
    ProgramDefinition,
)
from qiboconnection.typings.job import JobRequest, JobResponse, JobStatus, JobType
from qiboconnection.user import User

from .data import simulator_device_inputs


@pytest.fixture(name="algorithm_definition")
def fixture_algorithm_definition() -> AlgorithmDefinition:
    """Create a new algorithm definition"""
    return AlgorithmDefinition(
        name=AlgorithmName.BELLSTATE,
        algorithm_type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )


@pytest.fixture(name="program_definition")
def fixture_program_definition(algorithm_definition: AlgorithmDefinition) -> ProgramDefinition:
    """Create a new program definition

    Returns:
        ProgramDefinition: Instance of the ProgramDefinition class.
    """
    return ProgramDefinition(algorithms=[algorithm_definition])


@pytest.fixture(name="circuit")
def fixture_circuit():
    """Create a circuit

    Returns:
        Circuit: Instance of Circuit with a couple of gates
    """
    circuit = Circuit(1)
    circuit.add(gates.H(0))
    circuit.add(gates.M(0))

    return circuit


@pytest.fixture(name="user")
def fixture_user() -> User:
    """Create a new user

    Returns:
        User: Instance of the User class.
    """
    return User(user_id=1, username="test-user", api_key="000-3333")


@pytest.fixture(name="simulator_device")
def fixture_simulator_device() -> SimulatorDevice:
    """Create a new SimulatorDevice

    Returns:
        SimulatorDevice: Instance of the SimulatorDevice class.
    """
    return SimulatorDevice(device_input=simulator_device_inputs[0])


def test_job_creation(circuit: Circuit, user: User, simulator_device: SimulatorDevice):
    """Test job creation

    Args:
        circuit (Circuit): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job_id = 23
    job_status = JobStatus.COMPLETED
    job_result = JobResult(job_id=job_id, http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==")
    job = Job(
        circuit=circuit,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        job_result=job_result,
        id=job_id,
    )
    assert isinstance(job, Job)


def test_job_creation_default_values(circuit: Circuit, user: User, simulator_device: SimulatorDevice):
    """test job creation using the default values

    Args:
        circuit (Circuit): ProgramDefinition
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job = Job(circuit=circuit, user=user, device=cast(Device, simulator_device))
    assert isinstance(job, Job)
    assert job.job_status == JobStatus.NOT_SENT
    assert job.job_result is None
    assert job.job_id == 0
    assert job.job_type == JobType.CIRCUIT
    with pytest.raises(Exception) as e_info:
        job.result()
    assert e_info.type == ValueError
    assert e_info.value.args[0] == "Job result still not completed"


def test_job_request(circuit: Circuit, user: User, simulator_device: SimulatorDevice):
    """test job request

    Args:
        circuit (Circuit): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job_status = JobStatus.COMPLETED
    job = Job(
        circuit=circuit,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
        nshots=10,
    )
    expected_job_request = JobRequest(
        user_id=user.user_id,
        device_id=simulator_device.id,
        description="Ly8gR2VuZXJhdGVkIGJ5IFFJQk8gMC4xLjcKT1BFTlFBU00gMi4wOwppbmNsdWRlICJxZWxpYjEuaW5jIjsKcXJlZyBxWzFdOwpjcmVnIHJlZ2lzdGVyMFsxXTsKaCBxWzBdOwptZWFzdXJlIHFbMF0gLT4gcmVnaXN0ZXIwWzBdOw==",
        number_shots=10,
    )
    assert isinstance(job, Job)
    assert job.job_request == expected_job_request


def test_update_with_job_response(circuit: Circuit, user: User, simulator_device: SimulatorDevice):
    """test update with job response

    Args:
        circuit (Circuit): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job_status = JobStatus.PENDING
    job = Job(
        circuit=circuit,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
    )
    job_response = JobResponse(
        user_id=user.user_id,
        number_shots=10,
        job_type=JobType.CIRCUIT,
        device_id=simulator_device.id,
        description="",
        job_id=job.id,
        queue_position=0,
        status=JobStatus.COMPLETED,
        result="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
    )
    job.update_with_job_response(job_response=job_response)
    assert job.result == [0.1, 0.1, 0.1, 0.1, 0.1]


# def test_job_creation_with_program(program_definition: ProgramDefinition, user: User, simulator_device: SimulatorDevice):
#     """Test job creation
#
#     Args:
#         program_definition (ProgramDefinition): ProgramDefinition
#         user (User): User
#         simulator_device (SimulatorDevice): SimulatorDevice
#     """
#
#     job_id = 23
#     job_status = JobStatus.COMPLETED
#     job_result = JobResult(job_id=job_id, http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==")
#     job = Job(
#         program=program_definition,
#         user=user,
#         device=cast(Device, simulator_device),
#         job_status=job_status,
#         job_result=job_result,
#         id=job_id,
#     )
#     assert isinstance(job, Job)
#
#
# def test_job_creation_with_program_default_values(
#     program_definition: ProgramDefinition, user: User, simulator_device: SimulatorDevice
# ):
#     """test job creation using the default values
#
#     Args:
#         program_definition (ProgramDefinition): ProgramDefinition
#         user (User): User
#         simulator_device (SimulatorDevice): SimulatorDevice
#     """
#
#     job = Job(program=program_definition, user=user, device=cast(Device, simulator_device))
#     assert isinstance(job, Job)
#     assert job.job_status == JobStatus.NOT_SENT
#     assert job.job_result is None
#     assert job.job_id == 0
#
#
# def test_job_request_with_program(program_definition: ProgramDefinition, user: User, simulator_device: SimulatorDevice):
#     """test job request
#
#     Args:
#         program_definition (ProgramDefinition): ProgramDefinition
#         user (User): User
#         simulator_device (SimulatorDevice): SimulatorDevice
#     """
#     job_status = JobStatus.COMPLETED
#     job = Job(
#         program=program_definition,
#         user=user,
#         device=cast(Device, simulator_device),
#         job_status=job_status,
#         id=23,
#         nshots=10,
#     )
#     expected_job_request = JobRequest(
#         user_id=user.user_id,
#         device_id=simulator_device.id,
#         description="W3sibmFtZSI6ICJiZWxsLXN0YXRlIiwgInR5cGUiOiAiR2F0ZS1CYXNlZCBDaXJjdWl0IiwgIm9wdGlvbnMiOiB7Im51bWJlcl9xdWJpdHMiOiAyLCAiaW5pdGlhbF92YWx1ZSI6ICJ6ZXJvIn19XQ==",
#         number_shots=10,
#     )
#     assert isinstance(job, Job)
#     assert job.job_request == expected_job_request
#
#
# def test_update_with_job_response_and_program(program_definition: ProgramDefinition, user: User, simulator_device: SimulatorDevice):
#     """test update with job response
#
#     Args:
#         program_definition (ProgramDefinition): ProgramDefinition
#         user (User): User
#         simulator_device (SimulatorDevice): SimulatorDevice
#     """
#
#     job_status = JobStatus.PENDING
#     job = Job(
#         program=program_definition,
#         user=user,
#         device=cast(Device, simulator_device),
#         job_status=job_status,
#         id=23,
#     )
#     job_response = JobResponse(
#         user_id=user.user_id,
#         device_id=simulator_device.id,
#         description="",
#         job_id=job.id,
#         queue_position=0,
#         status=JobStatus.COMPLETED,
#         result="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
#     )
#     job.update_with_job_response(job_response=job_response)
#     assert job.result == [0.1, 0.1, 0.1, 0.1, 0.1]
