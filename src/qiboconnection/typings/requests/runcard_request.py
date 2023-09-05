""" Runcard typing classes """
from dataclasses import dataclass


@dataclass
class RuncardRequest:
    """Base structure for a SavedExperiment body of any rest interaction"""

    name: str
    runcard: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str
