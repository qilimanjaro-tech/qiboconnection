""" Tests methods for Device """

import json

import pytest

from qiboconnection.devices.device import Device
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.devices.simulator_device_characteristics import (
    SimulatorDeviceCharacteristics,
)
from qiboconnection.typings.device import (
    DeviceInput,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)

from .data import (
    device_inputs,
    simulator_device_characteristics_inputs,
    simulator_device_inputs,
)

#
# @pytest.mark.parametrize("device_input", device_inputs)
# def test_devices_constructor(device_input: DeviceInput):
#     device = Device(device_input=device_input)
#     assert isinstance(device, Device)
#


def test_devices_constructor():
    devices = Devices()
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_single_device(simulator_device_input: SimulatorDeviceInput):
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_constructor_with_device_list(simulator_device_input: SimulatorDeviceInput):
    simulator_device_list = [SimulatorDevice(device_input=simulator_device_input)]
    devices = Devices(device=simulator_device_list)
    assert isinstance(devices, Devices)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_json(simulator_device_input: SimulatorDeviceInput):
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert devices.toJSON() == f"{simulator_device.toJSON()}\n"


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_str(simulator_device_input: SimulatorDeviceInput):
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(device=simulator_device)
    assert str(devices) == f"<Devices[1]:\n{simulator_device.toJSON()}\n"


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_update_device(simulator_device_input: SimulatorDeviceInput):
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices()
    devices.add_or_update(simulator_device)
    assert devices.to_dict() == [dict(simulator_device.__dict__.items())]


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_devices_select_device(simulator_device_input: SimulatorDeviceInput):
    simulator_device = SimulatorDevice(device_input=simulator_device_input)
    devices = Devices(simulator_device)
    selected_device = devices.select_device(device_id=1)
    assert selected_device.toJSON() == simulator_device.toJSON()


#
# @pytest.mark.parametrize("device_input", device_inputs)
# def test_device_string_representation(device_input: DeviceInput):
#     device = Device(device_input=device_input)
#
#     assert (
#         device.__str__()
#         == f"<Device: device_id={device._device_id}, device_name='{device._device_name}', status='{device._status.value}', channel_id=None>"
#     )
#
#
# @pytest.mark.parametrize("device_input", device_inputs)
# def test_device_dict_representation(device_input: DeviceInput):
#     device = Device(device_input=device_input)
#     expected_dict = {
#         "device_id": device._device_id,
#         "device_name": device._device_name,
#         "status": device._status.value,
#     }
#     assert device.__dict__ == expected_dict
#
#
# @pytest.mark.parametrize("device_input", device_inputs)
# def test_device_json_representation(device_input: DeviceInput):
#     device = Device(device_input=device_input)
#     expected_dict = {
#         "device_id": device._device_id,
#         "device_name": device._device_name,
#         "status": device._status.value,
#     }
#     assert device.toJSON() == json.dumps(expected_dict, indent=2)
#
#
# @pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
# def test_simulator_device_constructor(simulator_device_input: SimulatorDeviceInput):
#     assert isinstance(simulator_device_input, SimulatorDeviceInput)
#     device = SimulatorDevice(device_input=simulator_device_input)
#     assert isinstance(device, SimulatorDevice)
#
#
# @pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
# def test_simulator_device_dict_representation(
#     simulator_device_input: SimulatorDeviceInput,
# ):
#     device = SimulatorDevice(device_input=simulator_device_input)
#     expected_dict = {
#         "device_id": device._device_id,
#         "device_name": device._device_name,
#         "status": device._status.value,
#     }
#     if device._characteristics:
#         expected_dict |= {"characteristics": device._characteristics.__dict__}
#     assert device.__dict__ == expected_dict
#
#
# @pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
# def test_simulator_device_json_representation(
#     simulator_device_input: SimulatorDeviceInput,
# ):
#     device = SimulatorDevice(device_input=simulator_device_input)
#     expected_dict = {
#         "device_id": device._device_id,
#         "device_name": device._device_name,
#         "status": device._status.value,
#     }
#     if device._characteristics:
#         expected_dict |= {"characteristics": device._characteristics.__dict__}
#     assert device.toJSON() == json.dumps(expected_dict, indent=2)
#
#
# @pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
# def test_simulator_device_characteristics_constructor(
#     simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
# ):
#     characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
#     assert isinstance(characteristics, SimulatorDeviceCharacteristics)
#
#
# @pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
# def test_simulator_device_characteristics_json_representation(
#     simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
# ):
#     characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
#     expected_dict = {
#         "type": characteristics._type.value,
#         "cpu": characteristics._cpu,
#         "gpu": characteristics._gpu,
#         "os": characteristics._os,
#         "kernel": characteristics._kernel,
#         "ram": characteristics._ram,
#     }
#     assert characteristics.toJSON() == json.dumps(expected_dict, indent=2)
