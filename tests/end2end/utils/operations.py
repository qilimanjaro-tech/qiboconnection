# pylint: disable=logging-fstring-interpolation
# pylint: disable=protected-access
import os
from enum import Enum

import pytest

from qiboconnection.models.devices import Device, QuantumDevice
from qiboconnection.typings.enums import DeviceAvailability, DeviceStatus

from .utils import is_development


# Explanation:
# Given a device, there are a series of OPERATIONS  we can perform:
# - Block: block the device
# - Select: select the device
# - Post: post a job
# - Response: Obtain a job response
# The expected results for such operations depends on its STATUS  that is a combination of
# - Status: online, offline
# - Availability: available, blocked
# - IsDevelopment?: If the test are performed in the development environment
# - IsQuantum?: If it is Quantum device
# where Environment, Type of device are not real attributes of the device (as the others) but
# they must be taken into consideration when testing.
# So, the combination of STATUS + OPERATION can have the following results:
# - Success : the operation can be performed and we expect OK
# - Failure : the operation can be performed and we expect to raise an exception
# - Forbidden : the operation COULD be performed (with maybe Success/Failure) BUT we
#               do not allow its execution because the side effects. This mainly applies
#               when the device is QUANTUM and the environment is PRODUCTION
#
class OperationResult(Enum):
    """Expected result of the operation for a given device in a certain environment"""

    SUCCESS = "Success"
    EXCEPTION = "Exception"
    FORBIDDEN = "Forbidden"


class Operation(Enum):
    """Expected result of the operation for a given device in a certain environment"""

    BLOCK = "block"
    SELECT = "select"
    POST = "post"
    RESPONSE = "response"
    CHANGE_STATUS = "change_status"


def is_device(device: Device, status: DeviceStatus, availability: DeviceAvailability) -> bool:
    return (device._status is None or device._status == status) and (
        device._availability is None or device._availability == availability
    )


def is_quantum(device: Device) -> bool:
    """Returns True if the device is a quantum device
    Args:
        device: device instance

    Returns:
        bool: if the device is a quantum device
    """
    return isinstance(device, QuantumDevice)


def get_expected_operation_result(  # pylint: disable=too-many-branches
    operation: Operation, device: Device
) -> OperationResult:
    """Get the expected result of performing a certain operation in a device.

    Together with the status and availability of the device, it takes into consideration other
    factors as the environment (eg. PRODUCTION) and the type of device (eg. QUANTUM)

    Args:
        op_name (str): the name of the operation
        device (Device): simulator or quantum device class

    Raises:
        Exception: if the operation is not in the list

    Returns:
        OperationResult: SUCCESS if the operation is allowed, else EXCEPTION. In some cases,
                         does not return anything and skip the test instead.

    """

    result: OperationResult = OperationResult.FORBIDDEN
    if operation == Operation.SELECT:
        result = OperationResult.SUCCESS
    elif operation == Operation.POST:
        result = OperationResult.SUCCESS
    elif operation == Operation.BLOCK:
        if is_quantum(device) and not is_development():
            result = OperationResult.FORBIDDEN
        elif is_device(device, DeviceStatus.MAINTENANCE, DeviceAvailability.AVAILABLE):
            result = OperationResult.SUCCESS
        else:
            result = OperationResult.EXCEPTION
    elif operation == Operation.CHANGE_STATUS:
        if is_quantum(device) and not is_development():
            result = OperationResult.FORBIDDEN
        if is_device(device, status=DeviceStatus.ONLINE, availability=DeviceAvailability.AVAILABLE) or is_device(
            device, availability=DeviceAvailability.AVAILABLE, status=DeviceStatus.MAINTENANCE
        ):
            result = OperationResult.SUCCESS
        else:
            result = OperationResult.EXCEPTION

    elif operation == Operation.RESPONSE:
        if is_quantum(device) and is_development():
            result = OperationResult.EXCEPTION
        elif is_device(device, status=DeviceStatus.ONLINE, availability=DeviceAvailability.AVAILABLE):
            result = OperationResult.SUCCESS
        else:
            result = OperationResult.FORBIDDEN
    else:
        raise NameError(f"Unknown operation {operation}")

    return result


def check_operation_possible_or_skip(operation: Operation, device: Device):
    """Skip the test unless the operation is possible in a device.

    Args:
        operation (Operation): _description_.
        device (Device): _description_
    """

    if get_expected_operation_result(operation, device) != OperationResult.SUCCESS:
        pytest.skip(
            f'Operation {operation} is not possible in {device._device_name} in the environment {os.environ["QIBOCONNECTION_ENVIRONMENT"]}.'
        )
