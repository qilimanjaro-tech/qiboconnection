""" Device Typing """
import enum
from dataclasses import dataclass
from typing import Literal, Optional


class DeviceStatus(enum.Enum):
    """Device Status

    Args:
        enum (str): Device Status options available:
            * available
            * busy
            * offline
    """

    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class DeviceType(enum.Enum):
    """Device Type

    Args:
        enum (str): Device type options available:
        * quantum
        * simulator
    """

    QUANTUM = "quantum"
    SIMULATOR = "simulator"


@dataclass
class QuantumDeviceCharacteristicsInput:
    """Quantum Device Characteristics Input

    Attributes:
        type (str): device type, "quantum"
        description (str): device description

    """

    type: Literal[DeviceType.QUANTUM, "quantum"]
    description: str


@dataclass
class SimulatorDeviceCharacteristicsInput:
    """Simulator Device Characteristics Input

    Attributes:
        type (str): device type, "simulator"
        cpu (str): device cpu
        gpu (str): device gpu
        os (str): device os
        kernel (str): device kernel
        ram (str): device ram

    """

    type: Literal[DeviceType.SIMULATOR, "simulator"]
    cpu: str
    gpu: str
    os: str  # pylint: disable=invalid-name
    kernel: str
    ram: str


@dataclass
class DeviceInput:
    """Device Input

    Attributes:
        device_id (int): device identifier
        device_name (str): device name
        status (str | DeviceStatus): device status
    """

    device_id: int
    device_name: str
    status: str | DeviceStatus
    channel_id: int | None


@dataclass
class CalibrationDetailsInput:
    """Calibration Details Input

    Attributes:
        elapsed_time (int): elapsed time
        t1 (int): last calibrated t1 time
        frequency (int): last calibrated frequency
    """

    elapsed_time: Optional[int]
    t1: Optional[int]  # pylint: disable=invalid-name
    frequency: Optional[int]


@dataclass
class OfflineDeviceInput(DeviceInput):
    """Offline Device Input"""


@dataclass
class OnlineDeviceInput(DeviceInput):
    """Online Device Input"""

    number_pending_jobs: Optional[int] = 0


@dataclass
class SimulatorDeviceInput(OnlineDeviceInput):
    """Simulator Device Input

    Args:
        OnlineDeviceInput (OnlineDeviceInput): Inherits from OnlineDeviceInput
    """

    characteristics: Optional[SimulatorDeviceCharacteristicsInput | None] = None


@dataclass
class QuantumDeviceInput(OnlineDeviceInput):
    """Quantum Device Input

    Args:
        OnlineDeviceInput (OnlineDeviceInput): Inherits from OnlineDeviceInput
    """

    last_calibration_time: Optional[str] = ""
    characteristics: Optional[QuantumDeviceCharacteristicsInput | None] = None
    calibration_details: Optional[CalibrationDetailsInput | None] = None
