"""Testing different large circuits."""
# pylint: disable=logging-fstring-interpolation
import logging

import pytest
from end2end.utils.operations import Operation, check_operation_possible_or_skip
from end2end.utils.utils import delete_job, get_devices_listing_params, post_and_get_result
from qibo.models import Circuit

from qiboconnection.api import API
from qiboconnection.models.devices import Device

# ------------------------------------------------------------------------ TESTS

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_one_qubit_500_gates_circuit(device: Device, api: API, one_qubits_500_gates_circuit: Circuit):
    """Test whether a one-qubit 500 gates circuit can be sent and then its result can be retrieved, for each device. This is the real user case. Note that this only considers ONLINE and AVAILABLE devices. Should be run with qili-admin-test user.

    Args:
        api: api instance to call the server with
    """
    logger.info(f"Device: {device}")
    check_operation_possible_or_skip(Operation.RESPONSE, device=device)
    jobdata = post_and_get_result(api=api, device=device, circuit=one_qubits_500_gates_circuit)
    result = jobdata.result
    assert isinstance(result, list)

    delete_job(api, job_id=jobdata.job_id)


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_two_qubit_500_gates_circuit(device: Device, api: API, two_qubits_500_gates_circuit: Circuit):
    """Test whether a two-qubit 500 gates circuit can be sent and then its result can be retrieved, for each device. This is the real user case. Note that this only considers ONLINE and AVAILABLE devices. Should be run with qili-admin-test user.


    Args:
        api: api instance to call the server with
    """
    logger.info(f"Device: {device}")
    check_operation_possible_or_skip(Operation.RESPONSE, device=device)
    jobdata = post_and_get_result(api=api, device=device, circuit=two_qubits_500_gates_circuit)
    result = jobdata.result
    assert isinstance(result, list)

    delete_job(api, job_id=jobdata.job_id)


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_five_qubit_500_gates_circuit(device: Device, api: API, five_qubits_500_gates_circuit: Circuit):
    """Test whether a five-qubit 500 gates circuit can be sent and then its result can be retrieved, for each device. This is the real user case. Note that this only considers ONLINE and AVAILABLE devices. Should be run with qili-admin-test user.


    Args:
        api: api instance to call the server with
    """
    logger.info(f"Device: {device}")
    check_operation_possible_or_skip(Operation.RESPONSE, device=device)
    jobdata = post_and_get_result(api=api, device=device, circuit=five_qubits_500_gates_circuit)
    result = jobdata.result
    assert isinstance(result, list)

    delete_job(api, job_id=jobdata.job_id)


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_all_circuits(
    device: Device,
    api: API,
    five_qubits_500_gates_circuit: Circuit,
    two_qubits_500_gates_circuit: Circuit,
    one_qubits_500_gates_circuit: Circuit,
):
    """Test whether all circuits can be sent in a single job and then its result can be retrieved, for each device. This is the real user case. Note that this only considers ONLINE and AVAILABLE devices. Should be run with qili-admin-test user.


    Args:
        api: api instance to call the server with

    """
    logger.info(f"Device: {device}")
    check_operation_possible_or_skip(Operation.RESPONSE, device=device)
    jobdata = post_and_get_result(
        api=api,
        device=device,
        circuit=[five_qubits_500_gates_circuit, two_qubits_500_gates_circuit, one_qubits_500_gates_circuit],
    )
    result = jobdata.result
    assert isinstance(result, list)

    delete_job(api, job_id=jobdata.job_id)
