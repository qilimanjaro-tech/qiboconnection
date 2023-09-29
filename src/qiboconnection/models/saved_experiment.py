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

""" SavedExperiment class"""
from dataclasses import dataclass, field
from datetime import datetime

from qiboconnection.typings.requests import SavedExperimentRequest
from qiboconnection.typings.responses import SavedExperimentResponse
from qiboconnection.util import decode_jsonified_dict, jsonify_dict_and_base64_encode


@dataclass
class SavedExperiment:  # pylint: disable=too-many-instance-attributes
    """SavedExperiment representation"""

    name: str
    user_id: int
    device_id: int
    description: str
    experiment: dict
    results: dict
    qililab_version: str
    id: int | None = field(default=None)
    created_at: datetime | None = field(default=None)

    @property
    def _encoded_experiment(self):
        """return base64-encoded stringified jsonified experiment"""
        return jsonify_dict_and_base64_encode(self.experiment) if self.experiment is not None else None

    @property
    def _encoded_results(self):
        """return base64-encoded stringified jsonified results"""
        return jsonify_dict_and_base64_encode(self.results) if self.results is not None else None

    @classmethod
    def from_response(cls, response: SavedExperimentResponse):
        """SavedExperiment constructor that takes in an instance from a SavedExperimentResponse"""
        return cls(
            id=response.saved_experiment_id,
            created_at=response.created_at,
            name=response.name,
            description=response.description,
            user_id=response.user_id,
            device_id=response.device_id,
            experiment=decode_jsonified_dict(response.experiment),
            results=decode_jsonified_dict(response.results),
            qililab_version=response.qililab_version,
        )

    def saved_experiment_request(self, favourite: bool = False):
        """Created a SavedExperimentRequest instance"""
        return SavedExperimentRequest(
            name=self.name,
            user_id=self.user_id,
            device_id=self.device_id,
            description=self.description,
            experiment=self._encoded_experiment,
            results=self._encoded_results,
            favourite=favourite,
            qililab_version=self.qililab_version,
        )
