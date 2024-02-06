"""End to end tests."""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=protected-access
import logging
import os
import sys

import pytest
from qibo.models import Circuit

from qiboconnection.api import API
from qiboconnection.models.devices import Device
from qiboconnection.typings.enums import DeviceAvailability as DA
from qiboconnection.typings.enums import DeviceStatus as DS
from qiboconnection.typings.enums import JobStatus
from qiboconnection.typings.job_data import JobData
from qiboconnection.typings.responses.job_response import JobResponse
from tests.end2end.utils.operations import (
    Operation,
    OperationResult,
    check_operation_possible_or_skip,
    get_expected_operation_result,
)
from tests.end2end.utils.utils import (
    delete_job,
    get_device,
    get_devices_listing_params,
    get_job_result,
    post_and_get_result,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))


# ------------------------------------------------------------------------ TESTS

# Environment
# See pytest.ini for the default value, this is a security to set a default value
os.environ["QIBOCONNECTION_ENVIRONMENT"] = (
    "development" if "QIBOCONNECTION_ENVIRONMENT" not in os.environ else os.environ["QIBOCONNECTION_ENVIRONMENT"]
)

# Globals
TIMEOUT = 240
CALL_EVERY_SECONDS = 5


def test_connection(api: API):
    """Test the connection by pinging the server
    Args:
        api: api instance to call the server with
    """

    response = api.ping()
    assert response == "OK", "Public server may not be answering"


def test_device_listing(devices: list[Device]):
    """Test the device listing call
    Args:
        devices (Devices): list of devices
    """
    assert len(devices) > 0, "No list of devices retrieved"


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_device_selection(device: Device, api: API):
    """Test the device electability for every listed device. The offline devices are skipped.
    Args:
        api: api instance to call the server with
    """

    op_result = get_expected_operation_result(Operation.SELECT, device)
    if op_result == OperationResult.EXCEPTION:
        with pytest.raises(Exception):
            api.select_device_id(device_id=device.id)
    elif op_result == OperationResult.SUCCESS:
        try:
            api.select_device_id(device_id=device.id)
        except ConnectionError:
            pytest.fail(f"Connection was not possible to {device.name}", pytrace=False)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            pytest.fail(f"Connecting to {device.name} raised {ex}", pytrace=True)
    else:
        pytest.skip(f"Operation {Operation.SELECT} not possible for {device}")


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_device_blocking_and_release(device: Device, api: API):
    """Test whether each device can be blocked and released

    Args:
        api: api instance to call the server with
    """

    op_result = get_expected_operation_result(Operation.BLOCK, device)
    if op_result == OperationResult.EXCEPTION:
        with pytest.raises(Exception):
            api.block_device_id(device_id=device.id)
    elif op_result == OperationResult.SUCCESS:
        try:
            api.block_device_id(device_id=device.id)
            api.release_device(device_id=device.id)
        except ConnectionError:
            pytest.fail(f"Connection was not possible to {device.name}", pytrace=False)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            pytest.fail(f"Connecting to {device.name} raised {ex}", pytrace=True)
    else:
        pytest.skip(f"Operation {Operation.BLOCK} not possbile for {device}")


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_circuit_posting(device: Device, api: API, numpy_circuit: Circuit):
    """Test whether a circuit can be sent to each device
    Args:
        api: api instance to call the server with
    """

    check_operation_possible_or_skip(Operation.POST, device)

    api.select_device_id(device_id=device.id)
    job_id = api.execute(circuit=numpy_circuit)
    assert isinstance(job_id, list)
    assert len(job_id) == 1
    api.delete_job(job_id=job_id[0])


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_circuit_result_response(device: Device, api: API, numpy_circuit: Circuit):
    """Test whether a circuit can be sent and then its result can be retrieved, for each device.

    Args:
        api: api instance to call the server with
    """

    logger = logging.getLogger(__name__)
    logger.debug(f"device: {device}")

    check_operation_possible_or_skip(Operation.POST, device)

    result: JobData = post_and_get_result(api=api, device=device, circuit=numpy_circuit, timeout=15)
    logger.debug(f"result: {result}")

    # The operation post + response can be performed always (it is an async action) but
    # the meaning of SUCCESS/EXCEPTION/FORBIDDEN means something different:
    response_result = get_expected_operation_result(Operation.RESPONSE, device)
    if response_result == OperationResult.SUCCESS:
        assert result.status == JobStatus.COMPLETED
    elif response_result == OperationResult.EXCEPTION:
        assert result.status == JobStatus.ERROR
    else:
        assert result.status == JobStatus.PENDING  # offline device

    delete_job(api, job_id=result.job_id)


# New Tests
@pytest.mark.parametrize("device", get_devices_listing_params())
def test_all_status(device: Device, api: API):
    """Test whether a device can be set to maitenance/online
    Args:
        device: device instance
    """

    check_operation_possible_or_skip(Operation.CHANGE_STATUS, device)

    initial_status = device._status
    initial_availability = device._availability
    if initial_status == DS.ONLINE:
        api.set_device_to_maintenance(device_id=device.id)
        assert get_device(api, device.id)._status == DS.MAINTENANCE
        api.set_device_to_online(device_id=device.id)
        assert get_device(api, device.id)._status == DS.ONLINE
    elif initial_status == DS.MAINTENANCE:
        # If the device is MAINTENANCE +  BLOCKED, we can not put it in online, that
        # will cause an exception. In fact the way to proceed should be
        # {Maintenace, Blocked} --[release]--> {Maintenace, Available} --[online]--> {Online, Available}
        if initial_availability == DA.BLOCKED:
            api.release_device(device_id=device.id)
            assert get_device(api, device.id)._availability == DA.AVAILABLE

        api.set_device_to_online(device_id=device.id)
        assert get_device(api, device.id)._status == DS.ONLINE

        api.set_device_to_maintenance(device_id=device.id)
        assert get_device(api, device.id)._status == DS.MAINTENANCE

        if initial_availability == DA.BLOCKED:
            api.block_device_id(device_id=device.id)
            assert get_device(api, device.id)._availability == DA.BLOCKED
    else:
        pytest.skip(f"Device {device} in status {initial_status}")

    # Check there are no changes in the device before we start the tests
    assert get_device(api, device.id)._status == initial_status
    assert get_device(api, device.id)._availability == initial_availability


@pytest.mark.parametrize("device", get_devices_listing_params())
def test_post_and_results_from_maintenance_to_online(device: Device, api: API, numpy_circuit: Circuit):
    """A Job posted in a device in maintenance mode should be able to get the results when de device goes to online.

    The tests are skipped if the device is quantum or it is in status offline.
    Once the tests are done, the device is returned back to its original status.

    Args:
        device (Device): The device instance
        api (API): The api instance
    """
    check_operation_possible_or_skip(Operation.POST, device)
    check_operation_possible_or_skip(Operation.RESPONSE, device)
    check_operation_possible_or_skip(Operation.CHANGE_STATUS, device)

    logger = logging.getLogger(__name__)

    logger.info(f"Device: {device}")

    original_status = device._status

    logger.info(f"Original Status: {original_status}")

    # Put the device in maintenance mode
    if original_status == DS.ONLINE:
        logger.info("Put it in maintenance mode")
        api.set_device_to_maintenance(device_id=device.id)
    elif original_status == DS.MAINTENANCE:
        pass
    else:
        pytest.skip(f"Device {device} in status {original_status}")

    # Send the job and wait for a while: we do not get the result
    logger.info(
        f"Send the job and wait for a short period, expecting the job will be in {JobStatus.PENDING.value}, because the device is in maintenance mode"
    )
    result: JobResponse = post_and_get_result(api, device, numpy_circuit, timeout=5)
    logger.info(f"Result: {result}")
    assert result.status == JobStatus.QUEUED

    # Put it back to online
    logger.info("Put it back to online")
    api.set_device_to_online(device.id)

    # Get the result
    logger.info(
        f"Now wait longer to get the result for job #{result.job_id}, expecting it  will be in {JobStatus.COMPLETED.value} because the device is in online mode"
    )
    result = get_job_result(api, result.job_id, call_every_seconds=10)
    logger.info(f"Result: {result}")
    assert result.status == JobStatus.COMPLETED

    # Put back to its original state
    if original_status == DS.MAINTENANCE:
        logger.info("Put it back to its original status")
        api.set_device_to_maintenance(device_id=device.id)

    delete_job(api, job_id=result.job_id)
