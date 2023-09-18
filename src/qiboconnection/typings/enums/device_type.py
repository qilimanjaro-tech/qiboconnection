""" DeviceType enum """
from .str_enum import StrEnum


class DeviceType(StrEnum):
    """Device Type

    Args:
        enum (str): Device type options available:
        * quantum
        * simulator
    """

    QUANTUM = "quantum"
    SIMULATOR = "simulator"
