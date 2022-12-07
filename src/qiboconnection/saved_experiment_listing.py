""" SavedExperimentListing class """

from abc import ABC
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List

import pandas as pd

from qiboconnection.typings.saved_experiment import SavedExperimentListingItemResponse
from qiboconnection.util import decode_jsonified_dict


@dataclass
class SavedExperimentListingItem(ABC):
    """SavedExperimentListing single item representation"""

    name: str
    user_id: int
    device_id: int
    description: str
    experiment: dict
    id: int | None = field(default=None)
    created_at: datetime | None = field(default=None)

    @classmethod
    def from_response(cls, response: SavedExperimentListingItemResponse):
        """Constructor for SavedExperimentListingItems that takes in a SavedExperimentListingItemResponse"""
        return cls(
            id=response.id,
            created_at=response.created_at,
            name=response.name,
            user_id=response.user_id,
            device_id=response.device_id,
            description=response.description,
            experiment=decode_jsonified_dict(response.experiment),
        )


@dataclass
class SavedExperimentListing(ABC):
    """SavedExperimentListing representation"""

    items: List[SavedExperimentListingItem]
    _dataframe: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self._dataframe = pd.DataFrame((asdict(item) for item in self.items)).set_index("id")

    @classmethod
    def from_response(cls, response_list: List[SavedExperimentListingItemResponse]):
        """Constructor for SavedExperimentListing that takes in a list of SavedExperimentListingItemResponse"""
        return cls(items=[SavedExperimentListingItem.from_response(response=response) for response in response_list])

    @property
    def dataframe(self):
        """Returns the dataframe shape of the results. Might be useful for performing queries over listed data."""
        return self._dataframe
