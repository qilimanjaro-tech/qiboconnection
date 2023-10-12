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

""" Quantum Device Typing """
from dataclasses import InitVar, dataclass

from .calibration_details_input import CalibrationDetailsInput
from .online_device_input import OnlineDeviceInput
from .quantum_device_characteristics_input import QuantumDeviceCharacteristicsInput


@dataclass(kw_only=True)
class QuantumDeviceInput(OnlineDeviceInput):
    """Quantum Device Input"""

    last_calibration_time: str | None = ""
    characteristics: InitVar[dict | None] = None
    calibration_details: InitVar[dict | None] = None

    def __post_init__(self, characteristics, calibration_details):
        self._characteristics = QuantumDeviceCharacteristicsInput(**characteristics)
        self._calibration_details = CalibrationDetailsInput(**calibration_details)

    @property
    def q_characteristics(self):
        """Characteristics getter"""
        return self._characteristics

    @property
    def q_calibration_details(self):
        """Calibration details getter"""
        return self._calibration_details
