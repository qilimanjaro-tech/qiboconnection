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

""" Online Device """

from typeguard import typechecked

from qiboconnection.typings.devices import OnlineDeviceInput

from .device import Device

# pylint: disable=no-member


class OnlineDevice(Device):
    """Online Device class"""

    @typechecked
    def __init__(self, device_input: OnlineDeviceInput):
        self._number_pending_jobs = None

        super().__init__(device_input)

        self._str = (
            f"<Online Device: device_id={self._device_id},"  # type: ignore[attr-defined]
            f" device_name='{self._device_name}',"  # type: ignore[attr-defined]
            f" status='{self._status}"
        )
        if self._number_pending_jobs is not None:
            self._str += f", number_pending_jobs={self._number_pending_jobs}"
        self._str += ">"
