from enum import Enum


class UserRole(str, Enum):
    """User roles with different permissions. admin is allowed to change device status and availability. qilimanjaro_user can only change availability provided that device status is maintenance. bsc_user can change none."""

    ADMIN = "admin"
    QILI = "qilimanjaro_user"
    BSC = "bsc_user"
    MACHINE = "machine"


class DeviceStatus(str, Enum):
    """Device status"""

    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class DeviceAvailability(str, Enum):
    """Device availability"""

    AVAILABLE = "available"
    BLOCKED = "blocked"
