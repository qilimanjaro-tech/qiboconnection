import enum
from typing import Literal, TypedDict, Union


class DeviceStatus(enum.Enum):
    online = "online"
    offline = "offline"


class DeviceType(enum.Enum):
    QUANTUM = "quantum"
    SIMULATOR = "simulator"


class QuantumDeviceCharacteristicsInput(TypedDict):
    type: Literal[DeviceType.QUANTUM, "quantum"]


class SimulatorDeviceCharacteristicsInput(TypedDict):
    type: Literal[DeviceType.SIMULATOR, "simulator"]
    cpu: str
    gpu: str
    os: str
    kernel: str
    ram: str


class DeviceInput(TypedDict):
    device_id: int
    device_name: str
    status: Union[str, DeviceStatus]


class CalibrationDetailsInput(TypedDict, total=False):
    elapsed_time: int
    t1: int
    frequency: int


class SimulatorDeviceInput(DeviceInput, total=False):
    characteristics: SimulatorDeviceCharacteristicsInput


class QuantumDeviceInput(DeviceInput, total=False):
    last_calibration_time: str
    characteristics: QuantumDeviceCharacteristicsInput
    calibration_details: CalibrationDetailsInput
