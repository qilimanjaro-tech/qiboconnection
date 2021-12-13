# device.py
from abc import ABC
from typing import Union
from typeguard import typechecked
import json

from qiboconnection.typings.device import DeviceInput, DeviceStatus


class Device(ABC):
    """Abstract class for devices."""

    @typechecked
    def __init__(self, device_input: DeviceInput):
        self._device_id = device_input["device_id"]
        self._device_name = device_input["device_name"]
        self._status = self._create_device_status(status=device_input["status"])

        self._str = f"<Device: device_id={self._device_id}, device_name='{self._device_name}', status='{self._status.value}'>"

    @property
    def id(self) -> int:
        return self._device_id

    def __str__(self) -> str:
        """String representation of a Device

        Returns:
            str: String representation of a Device
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of a Device

        Returns:
            dict: Output dictionary of a Device object
        """
        return {
            "device_id": self._device_id,
            "device_name": self._device_name,
            "status": self._status.value,
        }

    def toJSON(self) -> str:
        """JSON representation of a Device

        Returns:
            str: JSON serialization of a Device object
        """

        return json.dumps(self.__dict__(), indent=2)

    @typechecked
    def _create_device_status(self, status: Union[str, DeviceStatus]) -> DeviceStatus:
        if type(status) is str:
            return DeviceStatus(status)
        return status
