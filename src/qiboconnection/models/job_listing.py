# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
