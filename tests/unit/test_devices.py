"""Tests methods for Devices"""

import json
from typing import List

import pytest

from qiboconnection.models.devices.device import Device
from qiboconnection.models.devices.devices import Devices
from qiboconnection.typings.devices import DeviceInput

from .data import simulator_device_inputs


def test_devices_constructor():
    """Test Devices class constructor"""
    devices = Devices()
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_single_device(simulator_device_input: DeviceInput):
    """Test Devices class constructor providing a single device"""
    simulator_device: Device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_device_list(simulator_device_input: DeviceInput):
    """Test Devices class constructor providing a list of devices"""
    simulator_device_list: List[Device] = [Device(device_input=simulator_device_input)]
    devices = Devices(device=simulator_device_list)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_to_dict_expand(simulator_device_input: DeviceInput):
    """
    Test Devices().to_dict() method with expanded fields.
    It must be considered that unexpected fields might arrive to the json here.
    """
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)

    output_dict = devices.to_dict(expand=True)

    assert output_dict[0]["id"] == simulator_device_input.id
    assert output_dict[0]["name"] == simulator_device_input.name
    assert output_dict[0]["status"] == simulator_device_input.status
    assert output_dict[0]["characteristics"] == simulator_device_input.characteristics  # type: ignore[attr-defined]
    assert output_dict == [simulator_device.to_dict(expand=True)]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_to_json_expand(simulator_device_input: DeviceInput):
    """
    Test Devices().to_dict() method with expanded fields.
    It must be considered that unexpected fields might arrive to the json here.
    """

    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)

    output_dict = json.loads(devices.toJSON(expand=True))

    assert output_dict[0]["id"] == simulator_device_input.id
    assert output_dict[0]["name"] == simulator_device_input.name
    assert output_dict[0]["status"] == simulator_device_input.status
    assert output_dict[0]["characteristics"] == simulator_device_input.characteristics  # type: ignore[attr-defined]
    assert output_dict == [simulator_device.to_dict(expand=True)]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_json_ontent(simulator_device_input: DeviceInput):
    """Test Devices().toJSON() method"""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)

    devices_json_deserialized: dict = json.loads(devices.toJSON(expand=True))[0]
    device_json_deserialized: dict = json.loads(simulator_device.toJSON(expand=True))
    for key in [*devices_json_deserialized.keys(), *device_json_deserialized.keys()]:
        assert devices_json_deserialized[key] == device_json_deserialized[key]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_json_expand_content(simulator_device_input: DeviceInput):
    """Test Devices().toJSON() method"""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)

    devices_json_deserialized: dict = json.loads(devices.toJSON(expand=False))[0]
    device_json_deserialized: dict = json.loads(simulator_device.toJSON(expand=False))
    for key in [*devices_json_deserialized.keys(), *device_json_deserialized.keys()]:
        assert devices_json_deserialized[key] == device_json_deserialized[key]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_str(simulator_device_input: DeviceInput):
    """Test Devices().__str__() method"""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)

    str_method = str(devices).translate(str.maketrans("", "", " "))
    expected_str = f"<Devices[1]:[\n{simulator_device.toJSON()}\n]>".translate(str.maketrans("", "", " "))
    assert str_method == expected_str


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_update_device(simulator_device_input: DeviceInput):
    """Test Devices().add_or_update() method with a not-preexisting device (add) and with a preexisting device
    (update)"""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices()
    # ADDS
    devices.add_or_update(simulator_device)
    assert devices.to_dict() == [dict(simulator_device.to_dict())]
    # UPDATES
    devices.add_or_update(simulator_device)
    assert devices.to_dict() == [dict(simulator_device.to_dict())]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_select_device(simulator_device_input: DeviceInput):
    """Test Devices().select_device() method"""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices(simulator_device)
    selected_device = devices.select_device(device_id=1)
    assert selected_device.toJSON() == simulator_device.toJSON()


def test_devices_select_device_raises_value_error_for_nonexistent_devices():
    """Test Devices().select_device() method providing it an id of a non-existing device."""
    devices = Devices()
    with pytest.raises(ValueError) as e_info:
        _ = devices.select_device(device_id=1)
    assert e_info.value.args[0] == "Device not found"


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_select_device_raises_value_error_for_duplicated(simulator_device_input: DeviceInput):
    """Test Devices.select_device() method providing it an id of a duplicated device."""
    simulator_device = Device(device_input=simulator_device_input)
    devices = Devices([simulator_device, simulator_device])
    with pytest.raises(ValueError) as e_info:
        _ = devices.select_device(device_id=1)
    assert e_info.value.args[0] == "Device duplicated with same id:1"
