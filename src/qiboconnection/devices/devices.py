# devices.py
from abc import ABC
from typing import Optional, Union
from typeguard import typechecked
from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.device import Device

from qiboconnection.devices.quantum_device import QuantumDevice
from qiboconnection.devices.simulator_device import SimulatorDevice


class Devices(ABC):
    """List of Quantum or Simulator devices"""

    @typechecked
    def __init__(
        self,
        device: Optional[
            Union[
                QuantumDevice,
                SimulatorDevice,
                list[Union[QuantumDevice, SimulatorDevice]],
            ]
        ] = None,
    ):
        only_one_device_not_null = device is not None and not isinstance(device, list)
        more_than_one_device_not_null = device is not None and isinstance(device, list)

        self._devices: list[Union[QuantumDevice, SimulatorDevice]] = []
        if only_one_device_not_null:
            self._devices.append(device)
        if more_than_one_device_not_null:
            self._create_list_of_devices(list_devices=device)

    @typechecked
    def _create_list_of_devices(
        self, list_devices: list[Union[QuantumDevice, SimulatorDevice]]
    ):
        for device in list_devices:
            self._devices.append(device)

    @typechecked
    def add(self, device: Union[QuantumDevice, SimulatorDevice]) -> None:
        self._devices.append(device)

    @typechecked
    def _update(self, device: Union[QuantumDevice, SimulatorDevice]) -> bool:
        for index, current_device in enumerate(self._devices):
            if current_device.id == device.id:
                self._devices[index] = device
                return True
        return False

    @typechecked
    def add_or_update(self, device: Union[QuantumDevice, SimulatorDevice]) -> None:
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
        return [
            {key: value for (key, value) in device.__dict__().items()}
            for device in self._devices
        ]

    def toJSON(self) -> str:
        one_json = ""
        for device in self._devices:
            one_json += device.toJSON()
            one_json += "\n"
        return one_json

    def select_device(self, id: int,) -> Union[QuantumDevice, SimulatorDevice]:
        device_found = self._find_device(id)
        return device_found

    def _find_device(self, id: int) -> Union[QuantumDevice, SimulatorDevice]:
        device_found = [device for device in self._devices if device.id == id]
        if len(device_found) == 0:
            raise ValueError("Device not found")
        if len(device_found) > 1:
            raise ValueError(f"Device duplicated with same id:{id}")
        return device_found.pop()

    def block_device(self, connection: Connection, device_id: int) -> None:
        device_found = self._find_device(device_id)
        self._block_device(connection=connection, device=device_found)

    def _block_device(self, connection: Connection, device: Device) -> None:
        device.block_device(connection=connection)
        logger.info(f"Device {device.name} blocked.")

    def release_device(self, connection: Connection, device_id: int) -> None:
        device_found = self._find_device(device_id)
        device_found.release_device(connection=connection)
        logger.info(f"Device {device_found.name} released.")
