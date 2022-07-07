""" Device Utility Methods
"""
from typing import Union

from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.device import Device
from qiboconnection.devices.offline_device import OfflineDevice
from qiboconnection.devices.quantum_device import QuantumDevice
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.typings.device import (
    DeviceStatus,
    OfflineDeviceInput,
    QuantumDeviceInput,
    SimulatorDeviceInput,
)


def block_device(connection: Connection, device: Device) -> None:
    """Blocks a device to avoid being used by others

    Args:
        connection (Connection): Qibo remote connection
        device (Device): the Device to block
    """
    device.block_device(connection=connection)
    logger.info("Device %s blocked.", device.name)


@typechecked
def is_offline_device_input(device_input: dict) -> bool:
    """Determine if the given device_input is from an Offline Device or not

    Args:
        device_input (dict): Device Input structure

    Returns:
        bool: True if the device is from an Offline Device
    """
    if "status" not in device_input or device_input["status"] is None:
        raise ValueError("'status' missing in device_input keys")
    return device_input["status"] in [
        DeviceStatus.OFFLINE,
        DeviceStatus.OFFLINE.value,
    ]


@typechecked
def is_quantum_device_input(device_input: dict) -> bool:
    """Determine if the given device_input is from a Quantum Device or not

    Args:
        device_input (dict): Device Input structure

    Returns:
        bool: True if the device is from a Quantum Device
    """
    return not {"last_calibration_time", "calibration_details"}.isdisjoint(device_input)


@typechecked
def create_device(device_input: dict) -> Union[QuantumDevice, SimulatorDevice, OfflineDevice]:
    """Creates a Device from a given device input.

    Args:
        device_input (dict): Device Input structure

    Returns:
        Union[QuantumDevice, SimulatorDevice, OfflineDevice]: The constructed Device Object
    """
    if is_offline_device_input(device_input=device_input):
        return OfflineDevice(device_input=OfflineDeviceInput(**device_input))
    if is_quantum_device_input(device_input=device_input):
        return QuantumDevice(device_input=QuantumDeviceInput(**device_input))
    return SimulatorDevice(device_input=SimulatorDeviceInput(**device_input))
