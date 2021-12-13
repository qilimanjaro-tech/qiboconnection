# job_result.py

from dataclasses import dataclass
from typing import Any, Optional
from qiboconnection.util import base64url_decode
from base64 import urlsafe_b64decode
from qiboconnection.config import logger
import numpy as np


@dataclass
class JobResult:
    """Job Result class"""

    http_response: str

    def __init__(self, http_response: str) -> None:
        decoded_results = base64url_decode(http_response)
        decoded_results = [
            np.loads(urlsafe_b64decode(decoded_result))
            for decoded_result in decoded_results
        ]
        self.data = decoded_results
