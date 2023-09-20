""" Simulator Device Characteristics Input Typing """
from dataclasses import dataclass
from typing import Literal

from qiboconnection.typings.enums import DeviceType


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
