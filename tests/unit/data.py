# data.py
""" Data to used alongside the test suite. """

from qiboconnection.typings.device import (
    DeviceInput,
    DeviceStatus,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)

device_inputs = [
    DeviceInput(device_id=1, device_name="one_device", status="available", channel_id=None),
    DeviceInput(device_id=2, device_name="second_device", status=DeviceStatus.AVAILABLE, channel_id=None),
]

simulator_device_characteristics_inputs = [
    SimulatorDeviceCharacteristicsInput(
        type="simulator",
        cpu="Intel Core i9-9900K @ 16x 5GHz",
        gpu="NVIDIA GeForce RTX 3090",
        os="Ubuntu 20.04 focal",
        kernel="x86_64 Linux 5.4.0-80-generic",
        ram="64185MiB",
    )
]

simulator_device_inputs = [
    SimulatorDeviceInput(
        device_id=1,
        device_name="radagast-simulator",
        status="available",
        channel_id=None,
        characteristics=simulator_device_characteristics_inputs[0],
    )
]

platform_settings_sample = {
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 4096,
    "software_average": 10,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

platform_settings_updated_sample = {
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 1024,
    "software_average": 5,
    "repetition_duration": 100000,
    "delay_between_pulses": 0,
    "delay_before_readout": 20,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

platform_locations_sample = [
    "/qiboconnection/src/qiboconnection/data/platform-schema_1",
    "/qiboconnection/src/qiboconnection/data/platform-schema_2",
]

platform_mocked_settings_sample = {
    "id": 1,
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 4096,
    "software_average": 10,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}
