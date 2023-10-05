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

""" SavedExperiment request"""
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass


@dataclass
class SavedExperimentRequest:
    """Class for encoding how the server expects to be requested SavedExperiments."""

    name: str
    experiment: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str
    results: str
    favourite: bool = False
