""" SavedExperiment request"""
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass


@dataclass
class SavedExperimentRequest:
    """Class for encoding how the server expects to be requested SavedExperiments."""

    name: str
    experiment: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str
    results: str
    favourite: bool = False
