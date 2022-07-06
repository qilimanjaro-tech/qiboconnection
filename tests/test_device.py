""" Tests methods for Device """

import json

import pytest

from qiboconnection.devices.device import Device
from qiboconnection.devices.offline_device import OfflineDevice, OfflineDeviceInput
from qiboconnection.devices.quantum_device import QuantumDevice, QuantumDeviceInput
from qiboconnection.devices.quantum_device_calibration_details import (
    CalibrationDetails,
    CalibrationDetailsInput,
)
from qiboconnection.devices.quantum_device_characteristics import (
    QuantumDeviceCharacteristics,
    QuantumDeviceCharacteristicsInput,
)
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
    quantum_device_characteristics_inputs,
    quantum_device_inputs,
    simulator_device_characteristics_inputs,
    simulator_device_inputs,
)


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_constructor(device_input: DeviceInput):
    device = Device(device_input=device_input)
    assert isinstance(device, Device)


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_string_representation(device_input: DeviceInput):
    device = Device(device_input=device_input)

    assert (
        device.__str__()
        == f"<Device: device_id={device._device_id}, device_name='{device._device_name}', status='{device._status.value}', channel_id=None>"
    )


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_dict_representation(device_input: DeviceInput):
    device = Device(device_input=device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status.value,
    }
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("device_input", device_inputs)
def test_device_json_representation(device_input: DeviceInput):
    device = Device(device_input=device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status.value,
    }
    assert device.toJSON() == json.dumps(expected_dict, indent=2)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_constructor(simulator_device_input: SimulatorDeviceInput):
    assert isinstance(simulator_device_input, SimulatorDeviceInput)
    device = SimulatorDevice(device_input=simulator_device_input)
    assert isinstance(device, SimulatorDevice)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_dict_representation(
    simulator_device_input: SimulatorDeviceInput,
):
    device = SimulatorDevice(device_input=simulator_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status.value,
    }
    if device._characteristics:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_json_representation(
    simulator_device_input: SimulatorDeviceInput,
):
    device = SimulatorDevice(device_input=simulator_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status.value,
    }
    if device._characteristics:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    assert device.toJSON() == json.dumps(expected_dict, indent=2)


@pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
def test_simulator_device_characteristics_constructor(
    simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
):
    characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
    assert isinstance(characteristics, SimulatorDeviceCharacteristics)


@pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
def test_simulator_device_characteristics_json_representation(
    simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
):
    characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
    expected_dict = {
        "type": characteristics._type.value,
        "cpu": characteristics._cpu,
        "gpu": characteristics._gpu,
        "os": characteristics._os,
        "kernel": characteristics._kernel,
        "ram": characteristics._ram,
    }
    assert characteristics.toJSON() == json.dumps(expected_dict, indent=2)


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_quantum_device_constructor(quantum_device_input: QuantumDeviceInput):
    assert isinstance(quantum_device_input, QuantumDeviceInput)
    device = QuantumDevice(device_input=quantum_device_input)
    assert isinstance(device, QuantumDevice)


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_quantum_device_dict_representation(
    quantum_device_input: QuantumDeviceInput,
):
    device = QuantumDevice(device_input=quantum_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status.value,
    }
    if device._characteristics:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    if device._calibration_details:
        expected_dict |= {"calibration_details": device._calibration_details.__dict__}
    if device._last_calibration_time:
        expected_dict |= {"last_calibration_time": device._last_calibration_time.__str__()}
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("quantum_device_characteristics_input", quantum_device_characteristics_inputs)
def test_quantum_device_characteristics_constructor(
    quantum_device_characteristics_input: QuantumDeviceCharacteristicsInput,
):
    characteristics = QuantumDeviceCharacteristics(characteristics_input=quantum_device_characteristics_input)
    assert isinstance(characteristics, QuantumDeviceCharacteristics)


@pytest.mark.parametrize("quantum_device_characteristics_input", quantum_device_characteristics_inputs)
def test_quantum_device_characteristics_json_representation(
    quantum_device_characteristics_input: QuantumDeviceCharacteristicsInput,
):
    characteristics = QuantumDeviceCharacteristics(characteristics_input=quantum_device_characteristics_input)
    expected_dict = {
        "type": characteristics._type.value,
    }
    assert characteristics.toJSON() == json.dumps(expected_dict, indent=2)


@pytest.mark.parametrize("device_input", device_inputs)
def test_offline_device_constructor(device_input: DeviceInput):
    offline_device_input = OfflineDeviceInput(**device_input.__dict__)
    device = OfflineDevice(device_input=offline_device_input)
    assert isinstance(device, OfflineDevice)
