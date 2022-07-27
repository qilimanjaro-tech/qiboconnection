""" Job Result """

from abc import ABC
from dataclasses import dataclass, field
from typing import List

from numpy import typing as npt
from qibo.abstractions.states import AbstractState

from qiboconnection.typings.job import JobType
from qiboconnection.util import (
    decode_results_from_circuit,
    decode_results_from_experiment,
    decode_results_from_program,
)


@dataclass
class JobResult(ABC):
    """Job Result class"""

    job_id: int
    http_response: str
    job_type: str | JobType
    data: List[AbstractState] | AbstractState | npt.NDArray | List[int] | List[float] | None = field(init=False)

    def __post_init__(self) -> None:
        """
        Decodes data from the http_response provided at instance creation, and uses that info to build the self.data
        attribute.
        """

        if self.job_type == JobType.CIRCUIT:
            self.data = decode_results_from_circuit(self.http_response)
            return
        if self.job_type == JobType.EXPERIMENT:
            self.data = decode_results_from_experiment(self.http_response)
            return
        if self.job_type == JobType.PROGRAM:
            self.data = decode_results_from_program(self.http_response)
            return
