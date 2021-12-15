# simulator_device_characteristics.py
from abc import ABC
from typing import Union
from typeguard import typechecked
import json

from qiboconnection.typings.device import (
    SimulatorDeviceCharacteristicsInput,
    DeviceType,
)


class SimulatorDeviceCharacteristics(ABC):
    """Class representation of a Simulator Device Characteristics"""

    @typechecked
    def __init__(self, characteristics_input: SimulatorDeviceCharacteristicsInput):
        if (
            characteristics_input["type"] is not DeviceType.SIMULATOR
            and characteristics_input["type"] != DeviceType.SIMULATOR.value
        ):
            raise TypeError("Characteristics Device not supported")

        self._type = self._create_device_type(device_type=characteristics_input["type"])
        self._cpu = characteristics_input["cpu"]
        self._gpu = characteristics_input["gpu"]
        self._os = characteristics_input["os"]
        self._kernel = characteristics_input["kernel"]
        self._ram = characteristics_input["ram"]

        self._str = f"<SimulatorDeviceCharacteristics: type='{self._type.value}'"
        self._str += f" cpu='{self._cpu}'"
        self._str += f" gpu='{self._gpu}'"
        self._str += f" os='{self._os}'"
        self._str += f" kernel='{self._kernel}'"
        self._str += f" ram='{self._ram}'"
        self._str += ">"

    def __str__(self) -> str:
        """String representation of SimulatorDeviceCharacteristics

        Returns:
            str: String representation SimulatorDeviceCharacteristics
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of SimulatorDeviceCharacteristics

        Returns:
            dict: Output dictionary of SimulatorDeviceCharacteristics object
        """
        return {
            "type": self._type.value,
            "cpu": self._cpu,
            "gpu": self._gpu,
            "os": self._os,
            "kernel": self._kernel,
            "ram": self._ram,
        }

    def toJSON(self) -> str:
        """JSON representation of SimulatorDeviceCharacteristics

        Returns:
            str: JSON serialization of SimulatorDeviceCharacteristics object
        """

        return json.dumps(self.__dict__(), indent=2)

    @typechecked
    def _create_device_type(self, device_type: Union[str, DeviceType]) -> DeviceType:
        if type(device_type) is str:
            return DeviceType(device_type)
        return device_type
