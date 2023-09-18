""" DeviceStatus enum """
from .str_enum import StrEnum


class DeviceStatus(StrEnum):
    """Device status"""

    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
