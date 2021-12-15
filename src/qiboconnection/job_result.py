# job_result.py

from dataclasses import dataclass
from typing import List

from qibo.abstractions.states import AbstractState
from qiboconnection.util import base64url_decode
from base64 import urlsafe_b64decode
import numpy as np
import io
import pickle


@dataclass
class JobResult:
    """Job Result class"""

    http_response: str

    def __init__(self, http_response: str) -> None:
        try:
            decoded_results = self._decode_results_from_circuit(http_response)
        except:
            decoded_results = self._decode_results_from_program(http_response)

        self.data = decoded_results

    def _decode_results_from_program(self, http_response: str) -> List[AbstractState]:
        decoded_results = base64url_decode(http_response)
        return [
            np.loads(urlsafe_b64decode(decoded_result))
            for decoded_result in decoded_results
        ]

    def _decode_results_from_program(self, http_response: str) -> AbstractState:
        decoded_result_str = urlsafe_b64decode(http_response)
        result_bytes = io.BytesIO(decoded_result_str)
        state: AbstractState = pickle.loads(result_bytes.getbuffer())
        return state
