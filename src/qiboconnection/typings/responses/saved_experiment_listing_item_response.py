""" SavedExperimentListingItemResponse typing """
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SavedExperimentListingItemResponse:
    """Encodes the expected response of the server when requested for a list of SavedExperiment"""

    name: str
    experiment: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str
    id: int
    created_at: datetime
