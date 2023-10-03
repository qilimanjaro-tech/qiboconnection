""" Device Typing """
from dataclasses import dataclass
from typing import Optional

from qiboconnection.util import from_kwargs


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

    @classmethod
    def from_kwargs(cls, **kwargs):
        return from_kwargs(cls, **kwargs)
