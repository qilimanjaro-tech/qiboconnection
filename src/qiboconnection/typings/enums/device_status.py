""" DeviceStatus enum """
from dataclasses import dataclass

from .str_enum import StrEnum


class DeviceStatus(StrEnum):
    """Device status typing for posting"""

    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
