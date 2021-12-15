# data.py
""" Data to used alongside the test suite. """

from qiboconnection.typings.device import (
    DeviceInput,
    DeviceStatus,
    SimulatorDeviceInput,
    SimulatorDeviceCharacteristicsInput,
)

device_inputs = [
    DeviceInput({"device_id": 1, "device_name": "one_device", "status": "online"}),
    DeviceInput(
        {"device_id": 2, "device_name": "two_device", "status": DeviceStatus.online}
    ),
]

simulator_device_inputs = [
    SimulatorDeviceInput(
        {
            "device_id": 1,
            "device_name": "radagast-simulator",
            "status": "online",
            "characteristics": {
                "type": "simulator",
                "cpu": "Intel Core i9-9900K @ 16x 5GHz",
                "gpu": "NVIDIA GeForce RTX 3090",
                "os": "Ubuntu 20.04 focal",
                "kernel": "x86_64 Linux 5.4.0-80-generic",
                "ram": "64185MiB",
            },
        }
    )
]

simulator_device_characteristics_inputs = [
    SimulatorDeviceCharacteristicsInput(
        {
            "type": "simulator",
            "cpu": "Intel Core i9-9900K @ 16x 5GHz",
            "gpu": "NVIDIA GeForce RTX 3090",
            "os": "Ubuntu 20.04 focal",
            "kernel": "x86_64 Linux 5.4.0-80-generic",
            "ram": "64185MiB",
        }
    )
]
