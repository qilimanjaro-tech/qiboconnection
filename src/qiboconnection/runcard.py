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

""" Runcard class"""
from dataclasses import dataclass, field
from datetime import datetime

from qiboconnection.typings.runcard import RuncardRequest, RuncardResponse
from qiboconnection.util import decode_jsonified_dict, jsonify_dict_and_base64_encode


@dataclass
class Runcard:
    """Runcard representation"""

    name: str
    user_id: int
    device_id: int
    description: str
    runcard: dict
    qililab_version: str
    id: int | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    @property
    def _encoded_runcard(self):
        """return base64-encoded stringified jsonified experiment"""
        return jsonify_dict_and_base64_encode(self.runcard) if self.runcard is not None else None

    @classmethod
    def from_response(cls, response: RuncardResponse):
        """SavedExperiment constructor that takes in an instance from a SavedExperimentResponse"""
        return cls(
            id=response.runcard_id,
            created_at=response.created_at,
            updated_at=response.updated_at,
            name=response.name,
            description=response.description,
            user_id=response.user_id,
            device_id=response.device_id,
            runcard=decode_jsonified_dict(response.runcard),
            qililab_version=response.qililab_version,
        )

    def runcard_request(self):
        """Created a SavedExperimentRequest instance"""
        return RuncardRequest(
            name=self.name,
            user_id=self.user_id,
            device_id=self.device_id,
            description=self.description,
            runcard=self._encoded_runcard,
            qililab_version=self.qililab_version,
        )
