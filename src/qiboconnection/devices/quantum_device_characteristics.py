# quantum_device_characteristics.py
from abc import ABC
from typing import Union
from typeguard import typechecked
import json

from qiboconnection.typings.device import QuantumDeviceCharacteristicsInput, DeviceType


class QuantumDeviceCharacteristics(ABC):
    """Class representation of a Quantum Device Characteristics"""

    @typechecked
    def __init__(self, characteristics_input: QuantumDeviceCharacteristicsInput):
        if (
            characteristics_input["type"] is not DeviceType.QUANTUM
            and characteristics_input["type"] != DeviceType.QUANTUM.value
        ):
            raise TypeError("Characteristics Device not supported")

        self._type = self._create_device_type(device_type=characteristics_input["type"])

        self._str = f"<QuantumDeviceCharacteristics: type='{self._type.value}'>"

    def __str__(self) -> str:
        """String representation of QuantumDeviceCharacteristics

        Returns:
            str: String representation QuantumDeviceCharacteristics
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of QuantumDeviceCharacteristics

        Returns:
            dict: Output dictionary of QuantumDeviceCharacteristics object
        """
        return {
            "type": self._type.value,
        }

    def toJSON(self) -> str:
        """JSON representation of QuantumDeviceCharacteristics

        Returns:
            str: JSON serialization of QuantumDeviceCharacteristics object
        """

        return json.dumps(self.__dict__(), indent=2)

    @typechecked
    def _create_device_type(self, device_type: Union[str, DeviceType]) -> DeviceType:
        if type(device_type) is str:
            return DeviceType(device_type)
        return device_type
