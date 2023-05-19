""" JobListing class """


from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List

import pandas as pd

from qiboconnection.typings.job import JobListingItemResponse
from qiboconnection.util import decode_jsonified_dict


@dataclass
class JobListingItem:
    """JobListing single item representation"""

    name: str
    user_id: int
    device_id: int       
    description: str
    experiment: dict
    qililab_version: str
    id: int | None = field(default=None)
    created_at: datetime | None = field(default=None)

    @classmethod
    def from_response(cls, response: JobListingItemResponse):
        """Constructor for JobListingItems that takes in a JobListingItemResponse"""
        return cls(
            id=response.id,
            created_at=response.created_at,
            name=response.name,
            user_id=response.user_id,
            device_id=response.device_id,
            description=response.description,
            experiment=decode_jsonified_dict(response.experiment),
            qililab_version=response.qililab_version,
        )


@dataclass
class JobListing:
    """JobListing representation"""

    items: List[JobListingItem]
    _dataframe: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self._dataframe = self._build_dataframe()
        self._coerce_dataframe_column_types()

    def _build_dataframe(self):
        """Builds the dataframe from the info in each listing item"""
        return pd.DataFrame((asdict(item) for item in self.items))

    def _coerce_dataframe_column_types(self):
        """Parses each column that can potentially have its type missinterpretated to the one we would expect"""
        self._dataframe["created_at"] = pd.to_datetime(self._dataframe["created_at"])

    @classmethod
    def from_response(cls, response_list: List[JobListingItemResponse]):
        """Constructor for JobListing that takes in a list of JobListingItemResponse"""
        return cls(items=[JobListingItem.from_response(response=response) for response in response_list])

    @property
    def dataframe(self):
        """Returns the dataframe shape of the results. Might be useful for performing queries over listed data."""
        return self._dataframe
