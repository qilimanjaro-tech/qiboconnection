""" Tests methods for Devices """

from typing import List

import pytest

from qiboconnection.models.devices import SimulatorDevice
from qiboconnection.models.devices.device import Device
from qiboconnection.models.devices.devices import Devices
from qiboconnection.typings.devices import SimulatorDeviceInput

from .data import simulator_device_inputs


def test_devices_constructor():
    """Test Devices class constructor"""
    devices = Devices()
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_single_device(simulator_device_input: SimulatorDeviceInput):
    """Test Devices class constructor providing a single device"""
    simulator_device: Device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_device_list(simulator_device_input: SimulatorDeviceInput):
    """Test Devices class constructor providing a list of devices"""
    simulator_device_list: List[Device] = [SimulatorDevice(device_input=simulator_device_input)]
    devices = Devices(device=simulator_device_list)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_json(simulator_device_input: SimulatorDeviceInput):
    """Test Devices().toJSON() method"""
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert devices.toJSON() == f"{simulator_device.toJSON()}\n"


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_str(simulator_device_input: SimulatorDeviceInput):
    """Test Devices().__str__() method"""
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert str(devices) == f"<Devices[1]:\n{simulator_device.toJSON()}\n"


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_update_device(simulator_device_input: SimulatorDeviceInput):
    """Test Devices().add_or_update() method with a not-preexisting device (add) and with a preexisting device
    (update)"""
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices()
    # ADDS
    devices.add_or_update(simulator_device)
    assert devices.to_dict() == [dict(simulator_device.__dict__.items())]
    # UPDATES
    devices.add_or_update(simulator_device)
    assert devices.to_dict() == [dict(simulator_device.__dict__.items())]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_select_device(simulator_device_input: SimulatorDeviceInput):
    """Test Devices().select_device() method"""
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
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
def test_devices_select_device_raises_value_error_for_duplicated(simulator_device_input: SimulatorDeviceInput):
    """Test Devices.select_device() method providing it an id of a duplicated device."""
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices([simulator_device, simulator_device])
    with pytest.raises(ValueError) as e_info:
        _ = devices.select_device(device_id=1)
    assert e_info.value.args[0] == "Device duplicated with same id:1"
