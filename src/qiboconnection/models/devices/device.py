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

from .device_details import DeviceDetails

# pylint: disable=no-member
# pylint: disable=attribute-defined-outside-init


class Device(DeviceDetails):
    """Abstract class for devices."""

    @typechecked
    def __init__(self, device_input: DeviceInput):
        super().__init__()
        for k, v in vars(device_input).items():
            setattr(self, f"_{k}", v)
        self._str = (
            f"<Device: device_id={self._id}, device_name='{self._name}', "  # type: ignore[attr-defined]
            + f"status='{self._status}', availability='{self._availability}'>"  # type: ignore[attr-defined]
        )

    @property
    def id(self) -> int:  # pylint: disable=invalid-name
        """Returns device identifier

        Returns:
            int: device identifier
        """
        return self._id  # type: ignore[attr-defined]

    @property
    def name(self) -> str:
        """Returns device name

        Returns:
            str: device name
        """
        return self._name  # type: ignore[attr-defined]

    @property
    def status(self) -> DeviceStatus | None:
        """Returns device name

        Returns:
            str: device name
        """
        _status = getattr(self, "_status", None)
        return DeviceStatus(_status) if _status else None  # type: ignore[attr-defined]

    @property
    def type(self) -> str:
        """Returns device type

        Returns:
            str: device type
        """
        return getattr(self, "_type")

    @property
    def number_pending_jobs(self) -> int | None:
        """Return pending jobs in the queue for the requested device

        Returns:
            int: pending jobs

        """
        return getattr(self, "_number_pending_jobs", None)

    @property
    def static_features(self) -> int | None:
        """Return pending jobs in the queue for the requested device

        Returns:
            int: pending jobs

        """
        return getattr(self, "_static_features", None)

    @property
    def dynamic_features(self) -> int | None:
        """Return pending jobs in the queue for the requested device

        Returns:
            int: pending jobs

        """
        return getattr(self, "_dynamic_features", None)

    def block_device(self, connection: Connection) -> None:
        """Blocks a device to avoid others to use it

        Args:
            connection (Connection): Qibo API connection

        Raises:
            HTTPError: Error blocking device
        """
        try:
            connection.update_device_availability(device_id=self._id, availability=DeviceAvailability.BLOCKED)  # type: ignore[attr-defined]
            self._availability = DeviceAvailability.BLOCKED
        except HTTPError as ex:
            logger.error("Error blocking device %s.", self._device_name)  # type: ignore[attr-defined]
            raise ex

    def release_device(self, connection: Connection) -> None:
        """Releases a device to let others use it

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_availability(device_id=self._id, availability=DeviceAvailability.AVAILABLE)  # type: ignore[attr-defined]
        self._availability = DeviceAvailability.AVAILABLE

    def set_to_online(self, connection: Connection) -> None:
        """Updates a device status so that it can accept remote jobs. Local jobs will be blocked.

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_status(device_id=self._id, status=DeviceStatus.ONLINE)  # type: ignore[attr-defined]
        self._status = DeviceStatus.ONLINE

    def set_to_maintenance(self, connection: Connection) -> None:
        """Puts a device in maintenance mode, so that it can only accept local jobs.
         Incoming remote jobs will be blocked.

        Args:
            connection (Connection): Qibo API connection
        """
        connection.update_device_status(device_id=self._id, status=DeviceStatus.MAINTENANCE)  # type: ignore[attr-defined]
        self._status = DeviceStatus.MAINTENANCE

    @property
    def to_dict(self):
        """Dictionary representation of a Device

        Returns:
            dict: Output dictionary of a Device object
        """
        result_dict = {}
        for key in self.__dir__():
            if len(key) >= 2 and key[0] == "_" and key[1] != "_":
                value = getattr(self, key, None)
                try:
                    json.dumps(value)
                    result_dict |= {key[1:]: getattr(self, key, None)}
                except (json.JSONDecodeError, TypeError):
                    pass
        return result_dict

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of a Device

        Returns:
            str: JSON serialization of a Device object
        """

        return json.dumps(self.to_dict, indent=2)
