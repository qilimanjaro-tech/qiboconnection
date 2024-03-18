""" Tests methods for Device """

import json

import pytest

from qiboconnection.models.devices import Device
from qiboconnection.models.devices.util import create_device, is_offline_device_input, is_quantum_device_input
from qiboconnection.typings.devices import DeviceInput
from qiboconnection.typings.enums import DeviceStatus

from .data import (
    device_inputs,
    offline_device_inputs,
    quantum_device_characteristics_inputs,
    quantum_device_inputs,
    simulator_device_characteristics_inputs,
    simulator_device_inputs,
)

# pylint: disable=no-member


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_constructor(device_input: DeviceInput):
    """Test device instance creation"""
    device = Device(device_input=device_input)
    assert isinstance(device, Device)
    assert device.name == device_input.device_name
    assert device.id == device_input.device_id


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_string_representation(device_input: DeviceInput):
    """Tests Device().__str__() method"""
    device = Device(device_input=device_input)
    print(str(device))
    print(
        f"<Device: device_id={device._device_id},"
        f" device_name='{device._device_name}',"
        f" status='{device._status}',"
        f" availability='{device._availability}',"
        f" channel_id=None"
        f">"
    )

    assert (
        str(device) == f"<Device: device_id={device._device_id},"
        f" device_name='{device._device_name}',"
        f" status='{device._status}',"
        f" availability='{device._availability}',"
        f" channel_id={device._channel_id}"
        f">"
    )


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_dict_representation(device_input: DeviceInput):
    """Tests Device().__dict__ property"""
    device = Device(device_input=device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_json_representation(device_input: DeviceInput):
    """Tests Device().toJSON() method"""
    device = Device(device_input=device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    assert json.loads(device.toJSON()) == expected_dict
