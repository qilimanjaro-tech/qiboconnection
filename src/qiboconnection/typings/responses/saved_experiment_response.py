""" SavedExperimentResponse Typing"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SavedExperimentResponse:
    """Encodes the expected response of the server when requested for a specific SavedExperiment"""

    name: str
    experiment: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str
    results: str
    saved_experiment_id: int
    created_at: datetime
