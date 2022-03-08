import enum
from typing import Literal, TypedDict, Union, Optional


class DeviceStatus(enum.Enum):
    available = "available"
    busy = "busy"
    offline = "offline"


class DeviceType(enum.Enum):
    QUANTUM = "quantum"
    SIMULATOR = "simulator"


class QuantumDeviceCharacteristicsInput(TypedDict):
    type: Literal[DeviceType.QUANTUM, "quantum"]
    description: str


class SimulatorDeviceCharacteristicsInput(TypedDict):
    type: Literal[DeviceType.SIMULATOR, "simulator"]
    cpu: str
    gpu: str
    os: str
    kernel: str
    ram: str


class _BareDevice(TypedDict):
    device_id: int
    device_name: str
    status: Union[str, DeviceStatus]


class DeviceInput(_BareDevice):
    channel_id: int


class CalibrationDetailsInput(TypedDict, total=False):
    elapsed_time: int
    t1: int
    frequency: int


class OfflineDeviceInput(_BareDevice):
    pass


class OnlineDeviceInput(DeviceInput, total=False):
    number_pending_jobs: Optional[int]


class SimulatorDeviceInput(OnlineDeviceInput, total=False):
    characteristics: SimulatorDeviceCharacteristicsInput


class QuantumDeviceInput(OnlineDeviceInput, total=False):
    last_calibration_time: str
    characteristics: QuantumDeviceCharacteristicsInput
    calibration_details: CalibrationDetailsInput
