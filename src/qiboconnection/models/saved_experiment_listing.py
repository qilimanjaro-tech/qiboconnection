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

""" SavedExperimentListing class """

from dataclasses import asdict, dataclass, field
from typing import List

import pandas as pd

from qiboconnection.typings.responses import SavedExperimentListingItemResponse

from .saved_experiment_listing_item import SavedExperimentListingItem


@dataclass
class SavedExperimentListing:
    """SavedExperimentListing representation"""

    items: List[SavedExperimentListingItem]
    _dataframe: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self._dataframe = self._build_dataframe()
        self._coerce_dataframe_column_types()

    def _build_dataframe(self):
        """Builds the dataframe from the info in each listing item"""
        return pd.DataFrame((asdict(item) for item in self.items))

    def _coerce_dataframe_column_types(self):
        """Parses each column that can potentially have its type misinterpretated to the one we would expect"""
        self._dataframe["created_at"] = pd.to_datetime(self._dataframe["created_at"])

    @classmethod
    def from_response(cls, response_list: List[SavedExperimentListingItemResponse]):
        """Constructor for SavedExperimentListing that takes in a list of SavedExperimentListingItemResponse"""
        return cls(items=[SavedExperimentListingItem.from_response(response=response) for response in response_list])

    @property
    def dataframe(self):
        """Returns the dataframe shape of the results. Might be useful for performing queries over listed data."""
        return self._dataframe
