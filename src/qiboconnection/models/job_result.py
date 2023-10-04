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
""" JobResult typing """

from abc import ABC
from dataclasses import dataclass, field
from typing import List

from numpy import typing as npt
from qibo.states import CircuitResult

from qiboconnection.typings.enums import JobType
from qiboconnection.util import decode_results_from_circuit, decode_results_from_experiment


@dataclass
class JobResult(ABC):
    """Job Result class"""

    job_id: int
    http_response: str
    job_type: str
    data: List[CircuitResult] | CircuitResult | npt.NDArray | List[int] | List[float] | dict | List[
        dict
    ] | None = field(init=False)

    def __post_init__(self) -> None:
        """
        Decodes data from the http_response provided at instance creation, and uses that info to build the self.data
        attribute.
        """

        if self.job_type == JobType.CIRCUIT:
            self.data = decode_results_from_circuit(self.http_response)
            return None
        if self.job_type == JobType.EXPERIMENT:
            self.data = decode_results_from_experiment(self.http_response)
            return None

        self.data = f"JobType {self.job_type} not supported!"
        return None
