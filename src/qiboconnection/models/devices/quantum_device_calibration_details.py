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

""" Quantum Calibration Details """

from typeguard import typechecked

from qiboconnection.typings.devices import CalibrationDetailsInput

from .device_details import DeviceDetails


class CalibrationDetails(DeviceDetails):  # pylint: disable=too-few-public-methods
    """Class representation of Quantum Calibration Details"""

    @typechecked
    def __init__(self, characteristics_input: CalibrationDetailsInput):
        super().__init__()

        self._elapsed_time = characteristics_input.elapsed_time
        self._t1 = characteristics_input.t1
        self._frequency = characteristics_input.frequency

        self._str = "<CalibrationDetails:"
        if self._elapsed_time:
            self._str += f" elapsed_time='{self._elapsed_time}'"
        if self._t1:
            self._str += f" t1='{self._t1}'"
        if self._frequency:
            self._str += f" frequency='{self._frequency}'"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of SimulatorDeviceCharacteristics

        Returns:
            dict: Output dictionary of SimulatorDeviceCharacteristics object
        """
        calibration_dict: dict = {}

        if self._elapsed_time:
            calibration_dict |= {"elapsed_time": self._elapsed_time}
        if self._t1:
            calibration_dict |= {"t1": self._t1}
        if self._frequency:
            calibration_dict |= {"frequency": self._frequency}
        return calibration_dict
