""" Quantum Device Characteristics Input Typing """
from dataclasses import dataclass
from typing import Literal

from qiboconnection.typings.enums import DeviceType


@dataclass(kw_only=True)
class QuantumDeviceCharacteristicsInput:
    """Quantum Device Characteristics Input

    Attributes:
        type (str): device type, "quantum"
        description (str): device description

    """

    type: Literal[DeviceType.QUANTUM, "quantum"]
    description: str | None = None
