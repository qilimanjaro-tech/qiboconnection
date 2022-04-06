""" Job Result """


import pickle  # nosec - temporary bandit ignore
from dataclasses import dataclass
from typing import List

from qibo.abstractions.states import AbstractState

from qiboconnection.util import decode_results_from_circuit, decode_results_from_program


@dataclass
class JobResult:
    """Job Result class"""

    job_id: int
    http_response: str
    data: List[AbstractState] | AbstractState | None = None

    def __post_init__(self) -> None:
        try:
            decoded_results = decode_results_from_circuit(self.http_response)
        except (pickle.PickleError, TypeError):
            decoded_results = decode_results_from_program(self.http_response)

        self.data = decoded_results
