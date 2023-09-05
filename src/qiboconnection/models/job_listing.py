""" JobListing class """

from dataclasses import asdict, dataclass, field
from typing import List

import pandas as pd

from qiboconnection.typings.responses import JobListingItemResponse

from .job_listing_item import JobListingItem


@dataclass
class JobListing:
    """JobListing representation"""

    items: List[JobListingItem]
    _dataframe: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self._dataframe = self._build_dataframe()

    def _build_dataframe(self):
        """Builds the dataframe from the info in each listing item"""
        return pd.DataFrame((asdict(item) for item in self.items))

    @classmethod
    def from_response(cls, response_list: List[JobListingItemResponse]):
        """Constructor for JobListing that takes in a list of JobResponse"""
        return cls(items=[JobListingItem.from_response(response=response) for response in response_list])

    @property
    def dataframe(self):
        """Returns the dataframe shape of the results. Might be useful for performing queries over listed data."""
        return self._dataframe
