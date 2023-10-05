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

"""Simulator Device Characteristics"""
import json

from typeguard import typechecked

from qiboconnection.models.devices.device_details import DeviceDetails
from qiboconnection.typings.devices import SimulatorDeviceCharacteristicsInput
from qiboconnection.typings.enums import DeviceType


class SimulatorDeviceCharacteristics(DeviceDetails):
    """Class representation of a Simulator Device Characteristics"""

    @typechecked
    def __init__(self, characteristics_input: SimulatorDeviceCharacteristicsInput):
        super().__init__()
        if (
            characteristics_input.type is not DeviceType.SIMULATOR
            and characteristics_input.type != DeviceType.SIMULATOR
        ):
            raise TypeError("Characteristics Device not supported")

        self._type = characteristics_input.type
        self._cpu = characteristics_input.cpu
        self._gpu = characteristics_input.gpu
        self._os = characteristics_input.os
        self._kernel = characteristics_input.kernel
        self._ram = characteristics_input.ram

        self._str = f"<SimulatorDeviceCharacteristics: type='{self._type}'"
        self._str += f" cpu='{self._cpu}'"
        self._str += f" gpu='{self._gpu}'"
        self._str += f" os='{self._os}'"
        self._str += f" kernel='{self._kernel}'"
        self._str += f" ram='{self._ram}'"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of SimulatorDeviceCharacteristics

        Returns:
            dict: Output dictionary of SimulatorDeviceCharacteristics object
        """
        return {
            "type": self._type,
            "cpu": self._cpu,
            "gpu": self._gpu,
            "os": self._os,
            "kernel": self._kernel,
            "ram": self._ram,
        }

    def toJSON(self) -> str:  # pylint: disable=invalid-name
        """JSON representation of SimulatorDeviceCharacteristics

        Returns:
            str: JSON serialization of SimulatorDeviceCharacteristics object
        """

        return json.dumps(self.__dict__, indent=2)
