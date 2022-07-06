# data.py
""" Data to used alongside the test suite. """

from qiboconnection.typings.device import (
    DeviceInput,
    DeviceStatus,
    QuantumDeviceCharacteristicsInput,
    QuantumDeviceInput,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)
from qiboconnection.typings.live_plot import UnitPoint

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
        characteristics={
            "type": "simulator",
            "cpu": "Intel Core i9-9900K @ 16x 5GHz",
            "gpu": "NVIDIA GeForce RTX 3090",
            "os": "Ubuntu 20.04 focal",
            "kernel": "x86_64 Linux 5.4.0-80-generic",
            "ram": "64185MiB",
        },
    )
]


quantum_device_characteristics_inputs = [QuantumDeviceCharacteristicsInput(type="quantum", description="Cluster")]
quantum_device_inputs = [
    QuantumDeviceInput(
        device_id=1,
        device_name="galadriel-cluster",
        status="available",
        last_calibration_time="0",
        channel_id=None,
        characteristics={"type": "quantum", "description": "Cluster"},
        calibration_details={"t1": 10, "frequency": 988},
    )
]

unit_plot_point = [UnitPoint(x=0, y=0, z=None, idx=None, idy=None)]

heatmap_unit_plot_points = [
    UnitPoint(x=0, y=0, z=0, idx=0, idy=0),
    UnitPoint(x=0, y=1, z=1, idx=0, idy=1),
    UnitPoint(x=1, y=0, z=2, idx=1, idy=0),
    UnitPoint(x=1, y=1, z=3, idx=1, idy=1),
]
