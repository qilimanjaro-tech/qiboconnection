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

""" Device Utility Methods
"""

from typeguard import typechecked

from qiboconnection.typings.devices import DeviceInput

from .device import Device


@typechecked
def create_device(device_input: dict) -> Device:
    """Creates a Device from a given device input.

    Args:
        device_input (dict): Device Input structure

    Returns:
        Device: The constructed Device Object
    """

    return Device(device_input=DeviceInput.from_kwargs(**device_input))
