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

""" Device Characteristics Utilities """

from typing import Union

from typeguard import typechecked

from qiboconnection.typings.enums import DeviceAvailability, DeviceType


@typechecked
def create_device_type(device_type: Union[str, DeviceType]) -> DeviceType:
    """Creates a DeviceType object from a string or directly from a DeviceType

    Args:
        device_type (Union[str, DeviceType]): name corresponding to the device type or
        directly the DeviceType

    Returns:
        DeviceType: Created DeviceType object
    """
    return DeviceType(device_type) if isinstance(device_type, str) else device_type


@typechecked
def set_device_status(status: str) -> str:
    """Checks that the device status is a str

    Args:
        status: str

    Returns:
        str
    """
    if isinstance(status, str):
        return status
    else:
        raise ValueError("Status needs to be str")


@typechecked
def set_device_availability(availability: str) -> str:
    """Checks that device availability is a str

    Args:
        availability: str

    Returns:
        str
    """
    if isinstance(availability, str):
        return availability
    else:
        raise ValueError("Availability needs to be a str")
