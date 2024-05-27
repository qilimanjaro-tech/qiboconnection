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

""" Device Typing """
from dataclasses import dataclass

from qiboconnection.util import from_kwargs

# pylint: disable=too-many-instance-attributes


@dataclass(kw_only=True)
class DeviceInput:
    """Device Input

    Attributes:
        id (int): device identifier
        name (str): device name
        status (str): device status
    """

    id: int
    name: str
    status: str
    type: str | None = None
    number_pending_jobs: int | None = None
    slurm_partition: str | None = None
    static_features: dict | None = None
    dynamic_features: dict | None = None

    @classmethod
    def from_kwargs(cls, **kwargs):
        "Returns an instance of DeviceInput including non-typed attributes"

        kwargs = cls._apply_retrocompatibility_conversions(kwargs=kwargs)

        return from_kwargs(cls, **kwargs)

    @classmethod
    def _apply_retrocompatibility_conversions(cls, kwargs):
        """
        If old required keys are provided instead of new ones, update the dictionary with the new
        expected values.
        """
        if "device_id" in kwargs:
            kwargs["id"] = kwargs.pop("device_id")
        if "device_name" in kwargs:
            kwargs["name"] = kwargs.pop("device_name")
        if "device_type" in kwargs:
            kwargs["type"] = kwargs.pop("device_type")
        return kwargs
