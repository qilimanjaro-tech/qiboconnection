# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Device class """
import json

from requests import HTTPError
from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.typings.devices import DeviceInput
from qiboconnection.typings.enums import DeviceAvailability, DeviceStatus

from .device_characteristics_util import set_device_availability, set_device_status
from .device_details import DeviceDetails


class Device(DeviceDetails):
    """Abstract class for devices."""

    @typechecked
    def __init__(self, device_input: DeviceInput):
        super().__init__()
        self._device_id = device_input.device_id
        self._device_name = device_input.device_name
        self._status = set_device_status(status=device_input.status)
        self._availability = set_device_availability(availability=device_input.availability)
        self._channel_id = device_input.channel_id

        self._str = (
            f"<Device: device_id={self._device_id}, device_name='{self._device_name}', "
            + f"status='{self._status}', availability='{self._availability}', channel_id={self._channel_id}>"
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
            connection.update_device_availability(device_id=self._device_id, availability=DeviceAvailability.BLOCKED)
            self._availability = set_device_availability(availability=DeviceAvailability.BLOCKED)
        except HTTPError as ex:
            logger.error("Error blocking device %s.", self._device_name)
            raise ex

    def release_device(self, connection: Connection) -> None:
        """Releases a device to let others use it

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_availability(device_id=self._device_id, availability=DeviceAvailability.AVAILABLE)
        self._availability = set_device_availability(availability=DeviceAvailability.AVAILABLE)

    def set_to_online(self, connection: Connection) -> None:
        """Updates a device status so that it can accept remote jobs. Local jobs will be blocked.

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_status(device_id=self._device_id, status=DeviceStatus.ONLINE)
        self._status = set_device_status(status=DeviceStatus.ONLINE)

    def set_to_maintenance(self, connection: Connection) -> None:
        """Puts a device in maintenance mode, so that it can only accept local jobs.
         Incoming remote jobs will be blocked.

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_status(device_id=self._device_id, status=DeviceStatus.MAINTENANCE)
        self._status = set_device_status(status=DeviceStatus.MAINTENANCE)

    @property
    def __dict__(self):
        """Dictionary representation of a Device

        Returns:
            dict: Output dictionary of a Device object
        """
        return {
            "device_id": self._device_id,
            "device_name": self._device_name,
            "status": self._status,
            "availability": self._availability,
        }

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of a Device

        Returns:
            str: JSON serialization of a Device object
        """

        return json.dumps(self.__dict__, indent=2)