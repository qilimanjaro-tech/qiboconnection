# device.py
from abc import ABC
from typing import Union
from requests import HTTPError
from typeguard import typechecked
import json
from qiboconnection.connection import Connection
from qiboconnection.config import logger
from qiboconnection.typings.device import DeviceInput, DeviceStatus


class Device(ABC):
    """Abstract class for devices."""

    @typechecked
    def __init__(self, device_input: DeviceInput):
        self._device_id = device_input["device_id"]
        self._device_name = device_input["device_name"]
        self._status = self._set_device_status(status=device_input["status"])
        self._channel_id = device_input["channel_id"]

        self._str = (f"<Device: device_id={self._device_id}, device_name='{self._device_name}', " +
                     f"status='{self._status.value}' channel_id={self._channel_id}>")

    @property
    def id(self) -> int:
        return self._device_id

    @property
    def name(self) -> int:
        return self._device_name

    def block_device(self, connection: Connection) -> None:
        try:
            connection.update_device_status(device_id=self._device_id, status=DeviceStatus.busy.value)
            self._status = self._set_device_status(status=DeviceStatus.busy)
        except HTTPError as ex:
            logger.error(f"Error blocking device {self._device_name}.")
            raise ex

    def release_device(self, connection: Connection) -> None:
        connection.update_device_status(device_id=self._device_id, status=DeviceStatus.available.value)
        self._status = self._set_device_status(status=DeviceStatus.available)

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
    def _set_device_status(self, status: Union[str, DeviceStatus]) -> DeviceStatus:
        if type(status) is str:
            return DeviceStatus(status)
        return status
