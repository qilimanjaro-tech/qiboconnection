""" Device Details """

from abc import ABC
from dataclasses import dataclass


@dataclass
class DeviceDetails(ABC):
    """Generic Device Details class to include the Device representation"""

    _str = ""

    def __str__(self) -> str:
        """String representation of DeviceDetails

        Returns:
            str: String representationDeviceDetails
        """
        return self._str

    def __repr__(self) -> str:
        """String representation of DeviceDetails

        Returns:
            str: String representationDeviceDetails
        """
        return self._str
