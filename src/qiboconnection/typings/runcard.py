""" Runcard typing classes """
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuncardRequest:
    """Base structure for a SavedExperiment body of any rest interaction"""

    name: str
    runcard: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str


@dataclass
class RuncardResponse(RuncardRequest):
    """Class for accommodating SavedExperiments web responses."""

    runcard_id: int
    created_at: datetime
    updated_at: datetime
