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

""" Simulator Device Characteristics Input Typing """
from dataclasses import dataclass
from typing import Literal

from qiboconnection.typings.enums import DeviceType


@dataclass(kw_only=True)
class SimulatorDeviceCharacteristicsInput:
    """Simulator Device Characteristics Input

    Attributes:
        type (str): device type, "simulator"
        cpu (str): device cpu
        gpu (str): device gpu
        os (str): device os
        kernel (str): device kernel
        ram (str): device ram

    """

    type: Literal[DeviceType.SIMULATOR, "simulator"]
    cpu: str | None = None
    gpu: str | None = None
    os: str | None = None  # pylint: disable=invalid-name
    kernel: str | None = None
    ram: str | None = None
