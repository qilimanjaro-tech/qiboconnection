""" Device Typing """
import enum
from dataclasses import InitVar, dataclass
from typing import Literal, Optional


class DeviceStatus(str, enum.Enum):
    """Device status"""

    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class DeviceAvailability(str, enum.Enum):
    """Device availability"""

    AVAILABLE = "available"
    BLOCKED = "blocked"


class DeviceType(str, enum.Enum):
    """Device Type

    Args:
        enum (str): Device type options available:
        * quantum
        * simulator
    """

    QUANTUM = "quantum"
    SIMULATOR = "simulator"


@dataclass(kw_only=True)
class QuantumDeviceCharacteristicsInput:
    """Quantum Device Characteristics Input

    Attributes:
        type (str): device type, "quantum"
        description (str): device description

    """

    type: Literal[DeviceType.QUANTUM, "quantum"]
    description: str | None = None


@dataclass(kw_only=True)
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
    cpu: str | None = None
    gpu: str | None = None
    os: str | None = None  # pylint: disable=invalid-name
    kernel: str | None = None
    ram: str | None = None


@dataclass(kw_only=True)
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
    availability: str | DeviceAvailability
    channel_id: int | None
    number_pending_jobs: Optional[int] = 0


@dataclass(kw_only=True)
class CalibrationDetailsInput:
    """Calibration Details Input

    Attributes:
        elapsed_time (int | None): elapsed time
        t1 (int | None): last calibrated t1 time
        frequency (int | None): last calibrated frequency
    """

    elapsed_time: int | None = None
    t1: int | None = None  # pylint: disable=invalid-name
    frequency: int | None = None


@dataclass(kw_only=True)
class OfflineDeviceInput(DeviceInput):
    """Offline Device Input"""


@dataclass(kw_only=True)
class OnlineDeviceInput(DeviceInput):
    """Online Device Input"""


@dataclass(kw_only=True)
class SimulatorDeviceInput(OnlineDeviceInput):
    """Simulator Device Input"""

    characteristics: InitVar[dict | None] = None

    def __post_init__(self, characteristics):
        self._characteristics = SimulatorDeviceCharacteristicsInput(**characteristics)

    @property
    def s_characteristics(self):
        """Characteristics getter"""
        return self._characteristics


@dataclass(kw_only=True)
class QuantumDeviceInput(OnlineDeviceInput):
    """Quantum Device Input"""

    last_calibration_time: str | None = ""
    characteristics: InitVar[dict | None] = None
    calibration_details: InitVar[dict | None] = None

    def __post_init__(self, characteristics, calibration_details):
        self._characteristics = QuantumDeviceCharacteristicsInput(**characteristics)
        self._calibration_details = CalibrationDetailsInput(**calibration_details)

    @property
    def q_characteristics(self):
        """Characteristics getter"""
        return self._characteristics

    @property
    def q_calibration_details(self):
        """Calibration details getter"""
        return self._calibration_details
