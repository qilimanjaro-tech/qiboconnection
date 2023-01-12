""" SavedExperiments typing classes """
from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class _SavedExperimentBodyBase(ABC):
    """Base structure for a SavedExperiment body of any rest interaction"""

    name: str
    experiment: str
    device_id: int
    user_id: int
    description: str
    qililab_version: str


@dataclass
class _FullSavedExperimentBodyBase(_SavedExperimentBodyBase):
    """Base structure for a SavedExperiment body of a rest interaction that includes results"""

    results: str


@dataclass
class SavedExperimentRequest(_FullSavedExperimentBodyBase):
    """Class for accommodating SavedExperiments web requests."""

    favourite: bool = False


@dataclass
class SavedExperimentResponse(_FullSavedExperimentBodyBase):
    """Class for accommodating SavedExperiments web responses."""

    saved_experiment_id: int
    created_at: datetime


@dataclass
class SavedExperimentListingItemResponse(_SavedExperimentBodyBase):
    """Class for accommodating SavedExperimentListings web responses"""

    id: int
    created_at: datetime
