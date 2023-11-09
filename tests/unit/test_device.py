""" Tests methods for Device """

import json

import pytest

from qiboconnection.models.devices import (
    Device,
    OfflineDevice,
    QuantumDevice,
    QuantumDeviceCharacteristics,
    SimulatorDevice,
    SimulatorDeviceCharacteristics,
)
from qiboconnection.models.devices.util import create_device, is_offline_device_input, is_quantum_device_input
from qiboconnection.typings.devices import (
    DeviceInput,
    OfflineDeviceInput,
    QuantumDeviceCharacteristicsInput,
    QuantumDeviceInput,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)
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


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_constructor(simulator_device_input: SimulatorDeviceInput):
    """Tests SimulatorDevice class constructor"""
    assert isinstance(simulator_device_input, SimulatorDeviceInput)
    device = SimulatorDevice(device_input=simulator_device_input)
    assert isinstance(device, SimulatorDevice)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_dict_representation(simulator_device_input: SimulatorDeviceInput):
    """Tests SimulatorDevice().__str__() method"""
    device = SimulatorDevice(device_input=simulator_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    if device._characteristics:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_simulator_device_json_representation(simulator_device_input: SimulatorDeviceInput):
    """Tests SimulatorDevice().toJSON() method"""
    device = SimulatorDevice(device_input=simulator_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    if device._characteristics:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    assert json.loads(device.toJSON()) == expected_dict


@pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
def test_simulator_device_characteristics_constructor(
    simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
):
    """Tests SimulatorCharacteristics class constructor"""
    characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
    assert isinstance(characteristics, SimulatorDeviceCharacteristics)


@pytest.mark.parametrize("simulator_device_characteristics_input", simulator_device_characteristics_inputs)
def test_simulator_device_characteristics_json_representation(
    simulator_device_characteristics_input: SimulatorDeviceCharacteristicsInput,
):
    """Tests SimulatorDeviceCharacteristics().toJSON() method"""
    characteristics = SimulatorDeviceCharacteristics(characteristics_input=simulator_device_characteristics_input)
    expected_dict = {
        "type": characteristics._type,
        "cpu": characteristics._cpu,
        "gpu": characteristics._gpu,
        "os": characteristics._os,
        "kernel": characteristics._kernel,
        "ram": characteristics._ram,
    }
    assert characteristics.toJSON() == json.dumps(expected_dict, indent=2)


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_quantum_device_constructor(quantum_device_input: QuantumDeviceInput):
    """Tests QuantumDevice class constructor"""
    assert isinstance(quantum_device_input, QuantumDeviceInput)
    device = QuantumDevice(device_input=quantum_device_input)
    assert isinstance(device, QuantumDevice)


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_quantum_device_dict_representation(quantum_device_input: QuantumDeviceInput):
    """Tests QuantumDevice().__dict__ property"""
    device = QuantumDevice(device_input=quantum_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    if device._last_calibration_time is not None:
        expected_dict |= {"last_calibration_time": str(device._last_calibration_time)}
    if device._characteristics is not None:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    if device._calibration_details is not None:
        expected_dict |= {"calibration_details": device._calibration_details.__dict__}
    assert device.__dict__ == expected_dict


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_quantum_device_json_representation(quantum_device_input: QuantumDeviceInput):
    """Tests QuantumDevice().toJSON() representation"""
    device = QuantumDevice(device_input=quantum_device_input)
    expected_dict = {
        "device_id": device._device_id,
        "device_name": device._device_name,
        "status": device._status,
        "availability": device._availability,
    }
    if device._last_calibration_time is not None:
        expected_dict |= {"last_calibration_time": str(device._last_calibration_time)}
    if device._characteristics is not None:
        expected_dict |= {"characteristics": device._characteristics.__dict__}
    if device._calibration_details is not None:
        expected_dict |= {"calibration_details": device._calibration_details.__dict__}
    assert json.loads(device.toJSON()) == expected_dict


@pytest.mark.parametrize("quantum_device_characteristics_input", quantum_device_characteristics_inputs)
def test_quantum_device_characteristics_constructor(
    quantum_device_characteristics_input: QuantumDeviceCharacteristicsInput,
):
    """Tests QuantumDeviceCharacteristics class constructor"""
    characteristics = QuantumDeviceCharacteristics(characteristics_input=quantum_device_characteristics_input)
    assert isinstance(characteristics, QuantumDeviceCharacteristics)


@pytest.mark.parametrize("quantum_device_characteristics_input", quantum_device_characteristics_inputs)
def test_quantum_device_characteristics_json_representation(
    quantum_device_characteristics_input: QuantumDeviceCharacteristicsInput,
):
    """Tests QuantumDeviceCharacteristics().toJSON() method"""
    characteristics = QuantumDeviceCharacteristics(characteristics_input=quantum_device_characteristics_input)
    expected_dict = {
        "type": characteristics._type,
    }
    assert json.loads(characteristics.toJSON()) == expected_dict


@pytest.mark.parametrize("offline_device_input", offline_device_inputs)
def test_offline_device_constructor(offline_device_input: OfflineDeviceInput):
    """Tests OfflineDevice class constructor"""
    device = OfflineDevice(device_input=offline_device_input)
    assert isinstance(device, OfflineDevice)


@pytest.mark.parametrize("offline_device_input", offline_device_inputs)
def test_is_offline_device_input(offline_device_input: OfflineDeviceInput):
    """Tests is_offline_device() utility function over an OfflineDevice-like input data"""
    assert is_offline_device_input(device_input=offline_device_input.__dict__)


@pytest.mark.parametrize("offline_device_input", offline_device_inputs)
def test_is_offline_device_input_rises_value_error_if_no_status(offline_device_input: OfflineDeviceInput):
    """Tests is_offline_device() utility function rises error when provided an OnlineDevice-like input data"""
    offline_device_input.status = None  # type: ignore

    with pytest.raises(ValueError) as e_info:
        _ = is_offline_device_input(device_input=offline_device_input.__dict__)

    assert e_info.value.args[0] == "'status' missing in device_input keys"


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_is_quantum_device_input(quantum_device_input: QuantumDeviceInput):
    """Tests is_quantum_device_input() utility function over an QuantumDevice-like input data"""
    assert is_quantum_device_input(device_input=quantum_device_input.__dict__)


@pytest.mark.parametrize("offline_device_input", offline_device_inputs)
def test_create_offline_device(offline_device_input: OfflineDeviceInput):
    """Tests create_device() utility function creates an OfflineDevice when provided OfflineDevice-like input data"""
    offline_device_input.status = DeviceStatus.OFFLINE

    device = create_device(device_input=offline_device_input.__dict__)
    assert isinstance(device, OfflineDevice)


@pytest.mark.parametrize("simulator_device_input", simulator_device_inputs)
def test_create_simulator_device(simulator_device_input: SimulatorDeviceInput):
    """Tests create_device() utility function creates an SimulatorDevice when provided SimulatorDevice-like input
    data"""
    stripped_down_simulator_device_input = simulator_device_input.__dict__.copy()

    stripped_down_simulator_device_input["characteristics"] = stripped_down_simulator_device_input[
        "_characteristics"
    ].__dict__
    del stripped_down_simulator_device_input["_characteristics"]

    device = create_device(device_input=stripped_down_simulator_device_input)
    assert isinstance(device, SimulatorDevice)


@pytest.mark.parametrize("quantum_device_input", quantum_device_inputs)
def test_create_quantum_device(quantum_device_input: QuantumDeviceInput):
    """Tests create_device() utility function creates an QuantumDevice when provided QuantumDevice-like input data"""
    stripped_down_quantum_device_input = quantum_device_input.__dict__.copy()

    stripped_down_quantum_device_input["characteristics"] = stripped_down_quantum_device_input[
        "_characteristics"
    ].__dict__
    del stripped_down_quantum_device_input["_characteristics"]

    stripped_down_quantum_device_input["calibration_details"] = stripped_down_quantum_device_input[
        "_calibration_details"
    ].__dict__
    del stripped_down_quantum_device_input["_calibration_details"]

    device = create_device(device_input=stripped_down_quantum_device_input)
    assert isinstance(device, QuantumDevice)
