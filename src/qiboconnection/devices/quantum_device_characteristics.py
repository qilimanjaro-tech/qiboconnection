""" Quantum Device Characteristics """
import json

from typeguard import typechecked

from qiboconnection.devices.device_characteristics_util import create_device_type
from qiboconnection.devices.device_details import DeviceDetails
from qiboconnection.typings.device import DeviceType, QuantumDeviceCharacteristicsInput


class QuantumDeviceCharacteristics(DeviceDetails):
    """Class representation of a Quantum Device Characteristics"""

    @typechecked
    def __init__(self, characteristics_input: QuantumDeviceCharacteristicsInput):
        super().__init__()
        if (
            characteristics_input.type is not DeviceType.QUANTUM
            and characteristics_input.type != DeviceType.QUANTUM.value
        ):
            raise TypeError("Characteristics Device not supported")

        self._type = create_device_type(device_type=characteristics_input.type)
        self._description = characteristics_input.description

        self._str = f"<QuantumDeviceCharacteristics: type='{self._type.value}' description='{self._description}'>"

    @property
    def __dict__(self):
        """Dictionary representation of QuantumDeviceCharacteristics

        Returns:
            dict: Output dictionary of QuantumDeviceCharacteristics object
        """
        return {
            "type": self._type.value,
        }

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of QuantumDeviceCharacteristics

        Returns:
            str: JSON serialization of QuantumDeviceCharacteristics object
        """

        return json.dumps(self.__dict__, indent=2)
