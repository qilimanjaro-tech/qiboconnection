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

""" Quantum Device Characteristics """
import json

from typeguard import typechecked

from qiboconnection.models.devices.device_details import DeviceDetails
from qiboconnection.typings.devices import QuantumDeviceCharacteristicsInput
from qiboconnection.typings.enums import DeviceType


class QuantumDeviceCharacteristics(DeviceDetails):
    """Class representation of a Quantum Device Characteristics"""

    @typechecked
    def __init__(self, characteristics_input: QuantumDeviceCharacteristicsInput):
        super().__init__()
        if characteristics_input.type is not DeviceType.QUANTUM and characteristics_input.type != DeviceType.QUANTUM:
            raise TypeError("Characteristics Device not supported")

        self._type = characteristics_input.type
        self._description = characteristics_input.description

        self._str = f"<QuantumDeviceCharacteristics: type='{self._type}' description='{self._description}'>"

    @property
    def __dict__(self):
        """Dictionary representation of QuantumDeviceCharacteristics

        Returns:
            dict: Output dictionary of QuantumDeviceCharacteristics object
        """
        return {
            "type": self._type,
        }

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of QuantumDeviceCharacteristics

        Returns:
            str: JSON serialization of QuantumDeviceCharacteristics object
        """

        return json.dumps(self.__dict__, indent=2)
