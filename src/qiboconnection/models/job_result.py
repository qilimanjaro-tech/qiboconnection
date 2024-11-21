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
"""JobResult typing"""

import json
import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import List

from numpy import typing as npt
from qibo.result import CircuitResult  # type: ignore[import-untyped]

from qiboconnection.typings.enums import JobType
from qiboconnection.util import decode_results_from_qprogram, decompress_any

logger = logging.getLogger(__name__)


@dataclass
class JobResult(ABC):
    """Job Result class"""

    job_id: int
    http_response: str
    job_type: str
    data: (
        List[CircuitResult] | CircuitResult | npt.NDArray | List[int] | List[float] | dict | List[dict] | str | None
    ) = field(init=False)

    def __post_init__(self) -> None:
        """
        Decodes data from the http_response provided at instance creation, and uses that info to build the self.data
        attribute.
        """
        try:
            self.data = decompress_any(**json.loads(self.http_response))
            return
        except Exception as ex:  # noqa: BLE001 # delete ASAP
            logger.warning(
                "Unable to decompress JobResult with get_results interface due to %s(%s). Falling back to legacy methods.",
                ex,
                type(ex),
            )

            if self.job_type == JobType.CIRCUIT:
                raise ValueError("Circuits should be serialized using compression.")

            if self.job_type in {JobType.QPROGRAM, JobType.ANNEALING_PROGRAM, JobType.VQA}:
                self.data = decode_results_from_qprogram(self.http_response)
                return

            logger.warning("Result not supported for type of job. Returning a plain string. ")
            self.data = self.http_response
