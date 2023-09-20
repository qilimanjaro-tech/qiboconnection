""" DeviceAvailability enum """
from .str_enum import StrEnum


class DeviceAvailability(StrEnum):
    """Device availability"""

    AVAILABLE = "available"
    BLOCKED = "blocked"
