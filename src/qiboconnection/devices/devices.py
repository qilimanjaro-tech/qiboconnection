""" Devices class """
from abc import ABC
from typing import List, Optional, Union

from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.offline_device import OfflineDevice
from qiboconnection.devices.quantum_device import QuantumDevice
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.devices.util import block_device


class Devices(ABC):
    """List of Quantum or Simulator devices"""

    @typechecked
    def __init__(
        self,
        device: Optional[
            Union[
                QuantumDevice,
                SimulatorDevice,
                OfflineDevice,
                List[Union[QuantumDevice, SimulatorDevice, OfflineDevice]],
            ]
        ] = None,
    ):
        only_one_device_not_null = device is not None and not isinstance(device, list)
        more_than_one_device_not_null = device is not None and isinstance(device, list)

        self._devices: list[Union[QuantumDevice, SimulatorDevice, OfflineDevice]] = []
        if only_one_device_not_null:
            self.add(device=device)  # type: ignore
        if more_than_one_device_not_null:
            self._create_list_of_devices(list_devices=device)  # type: ignore

    @typechecked
    def _create_list_of_devices(self, list_devices: list[Union[QuantumDevice, SimulatorDevice, OfflineDevice]]):
        for device in list_devices:
            self._devices.append(device)

    @typechecked
    def add(self, device: Union[QuantumDevice, SimulatorDevice, OfflineDevice]) -> None:
        """Adds a new Device

        Args:
            device (Union[QuantumDevice, SimulatorDevice, OfflineDevice]): any Device supported type
        """
        self._devices.append(device)

    @typechecked
    def _update(self, device: Union[QuantumDevice, SimulatorDevice, OfflineDevice]) -> bool:
        for index, current_device in enumerate(self._devices):
            if current_device.id == device.id:
                self._devices[index] = device
                return True
        return False

    @typechecked
    def add_or_update(self, device: Union[QuantumDevice, SimulatorDevice, OfflineDevice]) -> None:
        """Adds a new Device or updates an existing one

        Args:
            device (Union[QuantumDevice, SimulatorDevice, OfflineDevice]): any Device supported type
        """
        updated = self._update(device=device)
        if not updated:
            self.add(device=device)

    def __str__(self) -> str:
        """String representation of a List of Devices

        Returns:
            str: String representation of a List of Devices
        """
        jsonized_devices = self.toJSON()
        return f"<Devices[{len(self._devices)}]:\n" f"{jsonized_devices}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> list[dict]:
        """returns a list of Devices converted into a dictionary

        Returns:
            list[dict]: a list of Devices converted into a dictionary
        """
        return [dict(device.__dict__().items()) for device in self._devices]

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """returns a JSON string representation of the devices

        Returns:
            str: a JSON string representation of the devices
        """
        one_json = ""
        for device in self._devices:
            one_json += device.toJSON()
            one_json += "\n"
        return one_json

    def select_device(
        self,
        device_id: int,
    ) -> Union[QuantumDevice, SimulatorDevice, OfflineDevice]:
        """Finds the specific device and returns it

        Args:
            id (int): Device identifier

        Returns:
            Union[QuantumDevice, SimulatorDevice]: Device selected
        """
        return self._find_device(device_id)

    def _find_device(self, device_id: int) -> Union[QuantumDevice, SimulatorDevice, OfflineDevice]:
        device_found = [device for device in self._devices if device.id == device_id]
        if not device_found:
            raise ValueError("Device not found")
        if len(device_found) > 1:
            raise ValueError(f"Device duplicated with same id:{device_id}")
        return device_found.pop()

    def block_device(self, connection: Connection, device_id: int) -> None:
        """Blocks a device to avoid besing used by others

        Args:
            connection (Connection): Qibo remote connection
            device_id (int): Device identifier
        """
        device_found = self._find_device(device_id)
        block_device(connection=connection, device=device_found)

    def release_device(self, connection: Connection, device_id: int) -> None:
        """Releases a device to let others use it

        Args:
            connection (Connection): Qibo remote connection
            device_id (int): Device identifier
        """
        device_found = self._find_device(device_id)
        device_found.release_device(connection=connection)
        logger.info("Device %s released.", device_found.name)
