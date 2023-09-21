""" Device Typing """
from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class DeviceInput:
    """Device Input

    Attributes:
        device_id (int): device identifier
        device_name (str): device name
        status (str): device status
    """

    device_id: int
    device_name: str
    status: str
    availability: str
    channel_id: int | None
    number_pending_jobs: Optional[int] = 0
