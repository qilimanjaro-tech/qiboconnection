""" Runcard typing classes """
from dataclasses import dataclass
from datetime import datetime

from ..requests import RuncardRequest


@dataclass
class RuncardResponse(RuncardRequest):
    """Class for accommodating Runcards."""

    runcard_id: int
    created_at: datetime
    updated_at: datetime
