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

""" SavedExperimentListingItem class """
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass, field
from datetime import datetime

from qiboconnection.typings.responses import SavedExperimentListingItemResponse
from qiboconnection.util import decode_jsonified_dict


@dataclass
class SavedExperimentListingItem:
    """SavedExperimentListing single item representation"""

    name: str
    user_id: int
    device_id: int
    description: str
    experiment: dict
    qililab_version: str
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
            qililab_version=response.qililab_version,
        )
