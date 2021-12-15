# devices.py
from abc import ABC
from typing import Optional, Union
from typeguard import typechecked
import json

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

    def select_device(self, id: int) -> Union[QuantumDevice, SimulatorDevice]:
        device_found = [device for device in self._devices if device.id == id]
        if len(device_found) == 0:
            raise ValueError("Device not found")
        if len(device_found) > 1:
            raise ValueError(f"Device duplicated with same id:{id}")
        return device_found.pop()
