"""Tests methods for Job"""

from typing import cast

import pytest
from qibo import gates
from qibo.models.circuit import Circuit

from qiboconnection.api_utils import deserialize_job_description
from qiboconnection.models import User
from qiboconnection.models.algorithm import (
    AlgorithmDefinition,
    AlgorithmName,
    AlgorithmOptions,
    AlgorithmType,
    InitialValue,
    ProgramDefinition,
)
from qiboconnection.models.devices.device import Device
from qiboconnection.models.job import Job
from qiboconnection.models.job_result import JobResult
from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.requests import JobRequest
from qiboconnection.typings.responses.job_response import JobResponse

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


@pytest.fixture(name="circuits")
def fixture_circuits():
    """Create a circuit

    Returns:
        Circuit: Instance of Circuit with a couple of gates
    """
    circuit = Circuit(1)
    circuit.add(gates.H(0))
    circuit.add(gates.M(0))

    return [circuit]


@pytest.fixture(name="user")
def fixture_user() -> User:
    """Create a new user

    Returns:
        User: Instance of the User class.
    """
    return User(user_id=1, username="test-user", api_key="000-3333")


@pytest.fixture(name="simulator_device")
def fixture_simulator_device() -> Device:
    """Create a new SimulatorDevice

    Returns:
        SimulatorDevice: Instance of the SimulatorDevice class.
    """
    return Device(device_input=simulator_device_inputs[0])


def test_job_creation(circuits: list[Circuit], user: User, simulator_device: Device):
    """Test job creation

    Args:
        circuits (list(Circuit)): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job_id = 23
    job_status = JobStatus.COMPLETED
    job_result = JobResult(
        job_id=job_id,
        http_response='{"data": "H4sIABrWEWcC/4uuViooyk9KTMrMySzJTC1WslKoVjIAkgZ6JjoKSoZgllktkJmcX5pXgpCHyYLlihNzC3LAmqOjDWJ1FKIN4QQaF03CIBZIKqVl5iXmxBeXJJakws1X0jDQMzcwNzQwM7cwNLQwMzUxN9U2yNJUgtqLU74W1cB4nN6zRAVw36JL1NbGAgB4XNujJgEAAA==", "encoding": "utf-8", "compression": "gzip"}',
        job_type=JobType.CIRCUIT,
    )
    job = Job(
        circuit=circuits,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        job_result=job_result,
        id=job_id,
    )
    assert isinstance(job, Job)


def test_job_creation_default_values(circuits: list[Circuit], user: User, simulator_device: Device):
    """test job creation using the default values

    Args:
        circuits (list[Circuit]): ProgramDefinition
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job = Job(circuit=circuits, user=user, device=cast(Device, simulator_device))
    assert isinstance(job, Job)
    assert job.job_status == JobStatus.NOT_SENT
    assert job.job_result is None
    assert job.job_id == 0
    assert job.job_type == JobType.CIRCUIT
    assert job.user_id == user.user_id
    assert job.device_id == simulator_device.id
    with pytest.raises(ValueError) as e_info:
        job.result()
    assert e_info.value.args[0] == "Job result still not completed"
    with pytest.raises(ValueError) as e_info:
        _ = job.algorithms
    assert e_info.value.args[0] == "Job does not contain an algorithm Program"


def test_jobs_job_type_raises_value_error(circuits: list[Circuit], user: User, simulator_device: Device):
    """test job.job_type raises value error when unable to determine type

    Args:
        circuit (list[Circuit]): circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job = Job(circuit=circuits, user=user, device=cast(Device, simulator_device))
    job.circuit = None

    with pytest.raises(ValueError) as e_info:
        _ = job.job_type

    assert e_info.value.args[0] == "Could not determine JobType"


def test_job_creation_qprogram(user: User, simulator_device: Device):
    """test job creation using an qprogram instead of a circuit

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job = Job(qprogram="", user=user, device=cast(Device, simulator_device))
    assert job.job_type == JobType.QPROGRAM


def test_job_creation_annealing(user: User, simulator_device: Device):
    """test job creation using an qprogram instead of a circuit

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job = Job(anneal_program_args={}, user=user, device=cast(Device, simulator_device))
    assert job.job_type == JobType.ANNEALING_PROGRAM


def test_job_creation_raises_value_error_when_circuit_qprogram_anneal_or_vqa_are_defined_simultaneously(
    circuits: list[Circuit], user: User, simulator_device: Device
):
    """test job creation only allows defining one of the following: qprogram, circuit or vqa.

    Args:
        circuits (list[Circuit]): ProgramDefinition
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    with pytest.raises(ValueError) as e_info:
        _ = Job(qprogram="", circuit=circuits, user=user, device=cast(Device, simulator_device))
    assert (
        e_info.value.args[0]
        == "VQA, circuit, qprogram and anneal_program_args were provided, but execute() only takes one of them."
    )


def test_job_creation_qprogram_raises_value_error_when_neither_of_circuit_qprogram_anneal_or_vqa_are_defined(
    user: User, simulator_device: Device
):
    """test job creation using neither qprogram nor circuit or vqa

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    with pytest.raises(ValueError) as e_info:
        _ = Job(qprogram=None, circuit=None, user=user, device=cast(Device, simulator_device))
    assert e_info.value.args[0] == "Neither of circuit, vqa, qprogram or anneal_program_args were provided."


def test_job_request_with_circuit(circuits: list[Circuit], user: User, simulator_device: Device):
    """test job request

    Args:
        circuits (list[Circuit]): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    job_status = JobStatus.COMPLETED
    user_id = user.user_id
    job = Job(
        circuit=circuits,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
        nshots=10,
        name="test",
        summary="test",
    )
    expected_job_request = JobRequest(
        user_id=user_id,
        device_id=simulator_device.id,
        description=job.job_request.description,
        number_shots=10,
        job_type=JobType.CIRCUIT,
        name="test",
        summary="test",
    )

    assert isinstance(job, Job)
    assert job.job_request == expected_job_request
    assert all(
        [
            "data" in job.job_request.description,
            "encoding" in job.job_request.description,
            "compression" in job.job_request.description,
        ]
    )
    for reconstructed_circuit, circuit in zip(
        deserialize_job_description(raw_description=job.job_request.description, job_type=JobType.CIRCUIT.value)[
            "data"
        ],
        job.circuit,
    ):
        assert reconstructed_circuit.to_qasm() == circuit.to_qasm()


def test_job_request_with_qprogram(user: User, simulator_device: Device):
    """test job request

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job_status = JobStatus.COMPLETED
    user_id = user.user_id
    job = Job(
        qprogram="",
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
        nshots=10,
        name="test",
        summary="test",
    )
    expected_job_request = JobRequest(
        user_id=user_id,
        device_id=simulator_device.id,
        description=job.job_request.description,
        number_shots=10,
        job_type=JobType.QPROGRAM,
        name="test",
        summary="test",
    )

    assert isinstance(job, Job)
    assert job.job_request == expected_job_request
    assert all(
        [
            "data" in job.job_request.description,
            "encoding" in job.job_request.description,
            "compression" in job.job_request.description,
        ]
    )
    reconstructed_qprogram = deserialize_job_description(
        raw_description=job.job_request.description, job_type=JobType.QPROGRAM
    )["data"]
    assert reconstructed_qprogram == ""  # noqa: PLC1901


def test_job_request_with_annealing_program(user: User, simulator_device: Device):
    """test job request

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job_status = JobStatus.COMPLETED
    user_id = user.user_id
    job = Job(
        anneal_program_args={},
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
        nshots=10,
        name="test",
        summary="test",
    )
    expected_job_request = JobRequest(
        user_id=user_id,
        device_id=simulator_device.id,
        description=job.job_request.description,
        number_shots=10,
        job_type=JobType.ANNEALING_PROGRAM,
        name="test",
        summary="test",
    )

    assert isinstance(job, Job)
    assert job.job_request == expected_job_request
    assert all(
        [
            "data" in job.job_request.description,
            "encoding" in job.job_request.description,
            "compression" in job.job_request.description,
        ]
    )
    reconstructed_annealing_program = deserialize_job_description(
        raw_description=job.job_request.description, job_type=JobType.ANNEALING_PROGRAM
    )["data"]
    assert reconstructed_annealing_program == {}


def test_job_request_raises_value_error_if_no_input_description_for_any_type(
    circuits: list[Circuit], user: User, simulator_device: Device
):
    """test job raises proper exceptions when trying to build request with none of circuit, qprogram

    Args:
        circuits (list[Circuit]): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job = Job(
        circuit=circuits,
        user=user,
        device=cast(Device, simulator_device),
        job_status=JobStatus.COMPLETED,
        id=23,
        nshots=10,
    )
    job.circuit = None
    with pytest.raises(ValueError) as e_info:
        _ = job.job_request
    assert e_info.value.args[0] == "Could not determine JobType"


def test_job_request_raises_value_error_if_several_of_description_input_types(
    circuits: list[Circuit], user: User, simulator_device: Device
):
    """test job raises proper exceptions when trying to build request with more than one of circuit, qprogram

    Args:
        circuits (list[Circuit]): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job = Job(
        qprogram="",
        user=user,
        device=cast(Device, simulator_device),
        job_status=JobStatus.COMPLETED,
        id=23,
        nshots=10,
    )
    job.circuit = circuits
    with pytest.raises(ValueError) as e_info:
        _ = job.job_request
    assert e_info.value.args[0] == "Could not determine JobType"


def test_job_request_raises_value_error_if_unknown_type(user: User, simulator_device: Device):
    """test job raises proper exceptions when trying to build request with more than one of circuit, qprogram

    Args:
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """
    job = Job(
        qprogram="",
        user=user,
        device=cast(Device, simulator_device),
        job_status=JobStatus.COMPLETED,
        id=23,
        nshots=10,
    )
    job.qprogram = None

    with pytest.raises(ValueError) as e_info:
        _ = job._get_job_description()
    assert e_info.value.args[0] == "No suitable information found for building description."


def test_update_with_job_response(circuits: list[Circuit], user: User, simulator_device: Device):
    """test update with job response

    Args:
        circuits (list[Circuit]): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    user_id = user.user_id
    job_status = JobStatus.PENDING
    job = Job(
        circuit=circuits,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
    )
    job_response = JobResponse(
        user_id=user_id,
        number_shots=10,
        job_type=JobType.CIRCUIT,
        device_id=simulator_device.id,
        description="",
        job_id=job.id,
        queue_position=0,
        status=JobStatus.COMPLETED,
        result='{"data": "H4sIABrWEWcC/4uuViooyk9KTMrMySzJTC1WslKoVjIAkgZ6JjoKSoZgllktkJmcX5pXgpCHyYLlihNzC3LAmqOjDWJ1FKIN4QQaF03CIBZIKqVl5iXmxBeXJJakws1X0jDQMzcwNzQwM7cwNLQwMzUxN9U2yNJUgtqLU74W1cB4nN6zRAVw36JL1NbGAgB4XNujJgEAAA==", "encoding": "utf-8", "compression": "gzip"}',
        name="test",
        summary="summary",
    )
    job.update_with_job_response(job_response=job_response)
    assert job.result == [
        {
            "probabilities": {"0": 0.4, "1": 0.6},
            "counts": {"0": 4, "1": 6},
            "samples": [[0], [1], [1], [0], [1], [1], [1], [1], [0], [0]],
            "final_state": {"0": "(0.7071067811865475+0j)", "1": "(0.7071067811865475+0j)"},
            "final_state_probabilities": {"0": 0.4999999999999999, "1": 0.4999999999999999},
        }
    ]


def test_update_with_job_response_raises_error_when_updating_incorrect_job(
    circuits: list[Circuit], user: User, simulator_device: Device
):
    """test update with job response of different user or from different device raises ValueError

    Args:
        circuits (list[Circuit]): Circuit
        user (User): User
        simulator_device (SimulatorDevice): SimulatorDevice
    """

    user_id = user.user_id
    job_status = JobStatus.PENDING
    job = Job(
        circuit=circuits,
        user=user,
        device=cast(Device, simulator_device),
        job_status=job_status,
        id=23,
        name="test",
        summary="test",
    )

    job_response_different_user = JobResponse(
        user_id=user_id + 1 if user_id is not None else 1,
        number_shots=10,
        job_type=JobType.CIRCUIT,
        device_id=simulator_device.id,
        description="",
        job_id=job.id,
        queue_position=0,
        status=JobStatus.COMPLETED,
        result="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
        name="test",
        summary="test",
    )
    with pytest.raises(ValueError) as e_info:
        job.update_with_job_response(job_response=job_response_different_user)
    assert e_info.value.args[0] == "Job response does not belong to the user."

    job_response_different_device = JobResponse(
        user_id=user_id,
        number_shots=10,
        job_type=JobType.CIRCUIT,
        device_id=simulator_device.id + 1,
        description="",
        job_id=job.id,
        queue_position=0,
        status=JobStatus.COMPLETED,
        result="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
        name="test",
        summary="test",
    )
    with pytest.raises(ValueError) as e_info:
        job.update_with_job_response(job_response=job_response_different_device)
    assert e_info.value.args[0] == "Job response does not belong to the device."
