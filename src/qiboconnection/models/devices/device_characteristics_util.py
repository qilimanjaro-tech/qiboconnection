""" Device Characteristics Utilities """

from typing import Union

from typeguard import typechecked

from qiboconnection.typings.enums import DeviceAvailability, DeviceStatus, DeviceType


@typechecked
def create_device_type(device_type: Union[str, DeviceType]) -> DeviceType:
    """Creates a DeviceType object from a string or directly from a DeviceType

    Args:
        device_type (Union[str, DeviceType]): name corresponding to the device type or
        directly the DeviceType

    Returns:
        DeviceType: Created DeviceType object
    """
    return DeviceType(device_type) if isinstance(device_type, str) else device_type


@typechecked
def set_device_status(status: Union[str, DeviceStatus]) -> DeviceStatus:
    """Creates a DeviceStatus object from a string or directly from a DeviceStatus

    Args:
        status (Union[str, DeviceStatus]): name corresponding to the device status or
        directly the DeviceStatus

    Returns:
        DeviceStatus: Created DeviceStatus object
    """
    return DeviceStatus(status) if isinstance(status, str) else status


@typechecked
def set_device_availability(availability: Union[str, DeviceAvailability]) -> DeviceAvailability:
    """Creates a DeviceAvailability object from a string or directly from a DeviceStatus

    Args:
        availability (Union[str, DeviceAvailability]): name corresponding to the device status or
        directly the DeviceStatus

    Returns:
        DeviceAvailability: Created DeviceAvailability object
    """
    return DeviceAvailability(availability) if isinstance(availability, str) else availability
