""" Job Result """


import pickle  # nosec - temporary bandit ignore
from dataclasses import dataclass, field
from typing import List

from numpy import ndarray
from qibo.abstractions.states import AbstractState

from qiboconnection.util import decode_results_from_circuit, decode_results_from_program


@dataclass
class JobResult:
    """Job Result class"""

    job_id: int
    http_response: str
    data: List[AbstractState] | AbstractState | ndarray | None = field(init=False)

    def __post_init__(self) -> None:
        """
        Decodes data from the http_response provided at instance creation, and uses that info to build the self.data
        attribute.
        """
        try:
            decoded_results = decode_results_from_circuit(self.http_response)
        except (pickle.PickleError, TypeError):
            decoded_results = decode_results_from_program(self.http_response)

        self.data = decoded_results
