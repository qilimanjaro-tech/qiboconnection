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
    assert device.name == device_input.name
    assert device.id == device_input.id


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_string_representation(device_input: DeviceInput):
    """Tests Device().__str__() method"""
    device = Device(device_input=device_input)

    assert (
        str(device) == f"<Device: id={device.id},"
        f" name='{device.name}',"
        f" status='{device.status}',"
        f" type='{device.type}'"
        f">"
    )


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_dict_representation(device_input: DeviceInput):
    """Tests Device().__dict__ property"""
    device = Device(device_input=device_input)
    expected_dict = {
        "id": device.id,
        "name": device.name,
        "status": device.status.value,
        "number_pending_jobs": None,
        "type": None,
    }
    assert device.to_dict(expand=False) == expected_dict


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_json_representation(device_input: DeviceInput):
    """Tests Device().toJSON() method"""
    device = Device(device_input=device_input)
    expected_dict = {
        "id": device.id,
        "name": device.name,
        "status": device.status.value,
        "number_pending_jobs": None,
        "type": None,
    }
    assert json.loads(device.toJSON(expand=False)) == expected_dict
