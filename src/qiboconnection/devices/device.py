""" Device class """
import json

from requests import HTTPError
from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.device_characteristics_util import set_device_status
from qiboconnection.devices.device_details import DeviceDetails
from qiboconnection.typings.device import DeviceInput, DeviceStatus


class Device(DeviceDetails):
    """Abstract class for devices."""

    @typechecked
    def __init__(self, device_input: DeviceInput):
        super().__init__()
        self._device_id = device_input.device_id
        self._device_name = device_input.device_name
        self._status = set_device_status(status=device_input.status)
        self._channel_id = device_input.channel_id

        self._str = (
            f"<Device: device_id={self._device_id}, device_name='{self._device_name}', "
            + f"status='{self._status.value}', channel_id={self._channel_id}>"
        )

    @property
    def id(self) -> int:  # pylint: disable=invalid-name
        """Returns device identifier

        Returns:
            int: device identifier
        """
        return self._device_id

    @property
    def name(self) -> str:
        """Returns device name

        Returns:
            str: device name
        """
        return self._device_name

    def block_device(self, connection: Connection) -> None:
        """Blocks a device to avoid others to use it

        Args:
            connection (Connection): Qibo API connection

        Raises:
            HTTPError: Error blocking device
        """
        try:
            connection.update_device_status(device_id=self._device_id, status=DeviceStatus.BUSY.value)
            self._status = set_device_status(status=DeviceStatus.BUSY)
        except HTTPError as ex:
            logger.error("Error blocking device %s.", self._device_name)
            raise ex

    def release_device(self, connection: Connection) -> None:
        """Releases a device to let others to use it

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_status(device_id=self._device_id, status=DeviceStatus.AVAILABLE.value)
        self._status = set_device_status(status=DeviceStatus.AVAILABLE)

    @property
    def __dict__(self):
        """Dictionary representation of a Device

        Returns:
            dict: Output dictionary of a Device object
        """
        return {
            "device_id": self._device_id,
            "device_name": self._device_name,
            "status": self._status.value,
        }

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of a Device

        Returns:
            str: JSON serialization of a Device object
        """

        return json.dumps(self.__dict__, indent=2)
