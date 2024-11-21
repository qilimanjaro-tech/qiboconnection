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

from dataclasses import dataclass


@dataclass
class VQA:
    """
    Class to be filled for executing variational quantum algorithms through Qilimanjaro's QaaS.
    """

    vqa_dict: dict
    init_params: list
    optimizer_params: dict | None = None

    def __post_init__(self):
        if self.optimizer_params is None:
            self.optimizer_params = {}
