""" Device Typing """
from dataclasses import dataclass

from .device_input import DeviceInput


@dataclass(kw_only=True)
class OfflineDeviceInput(DeviceInput):
    """Offline Device Input"""
