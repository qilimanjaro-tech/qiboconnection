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

"""DeviceType enum"""

from .str_enum import StrEnum


class DeviceType(StrEnum):
    """Device Type

    Args:
        enum (str): Device type options available:
        * quantum
        * simulator
    """

    SIMULATOR_DEVICE = "simulator_device"
    QUANTUM_DEVICE = "quantum_device"
    QUANTUM_ANALOG_DEVICE = "quantum_analog_device"
    QUANTUM_DIGITAL_DEVICE = "quantum_digital_device"
