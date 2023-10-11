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

"""Simulator Device"""

from typeguard import typechecked

from qiboconnection.typings.devices import SimulatorDeviceInput

from .online_device import OnlineDevice
from .simulator_device_characteristics import SimulatorDeviceCharacteristics

# pylint: disable=no-member


class SimulatorDevice(OnlineDevice):
    """Simulator Device class"""

    @typechecked
    def __init__(self, device_input: SimulatorDeviceInput):
        self._characteristics = (
            SimulatorDeviceCharacteristics(device_input.s_characteristics)
            if device_input.s_characteristics is not None
            else None
        )

        super().__init__(device_input=device_input)

        self._str = (
            f"<Simulator Device: device_id={self._device_id}, device_name='{self._device_name}'"  # type: ignore[attr-defined]
            f", status='{self._status}'"
        )
        if self._characteristics:
            self._str += f", characteristics={str(self._characteristics)}"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of a SimulatorDevice

        Returns:
            dict: Output dictionary of a SimulatorDevice object
        """
        device_dict = super().__dict__
        if self._characteristics:
            device_dict |= {"characteristics": self._characteristics.__dict__}
        return device_dict
