""" SavedExperiment class"""
from abc import ABC
from dataclasses import asdict, dataclass, field
from datetime import datetime

from qiboconnection.typings.saved_experiment import (
    SavedExperimentRequest,
    SavedExperimentResponse,
)
from qiboconnection.util import decode_jsonified_dict, jsonify_dict_and_base64_encode


@dataclass
class SavedExperiment(ABC):
    """SavedExperiment representation"""

    name: str
    user_id: int
    device_id: int
    description: str
    experiment: dict
    results: dict
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
        decode_jsonified_dict(response.experiment)
        return cls(
            id=response.saved_experiment_id,
            created_at=response.created_at,
            name=response.name,
            description=response.description,
            user_id=response.user_id,
            device_id=response.device_id,
            experiment=decode_jsonified_dict(response.experiment),
            results=decode_jsonified_dict(response.results),
        )

    def saved_experiment_request(self, favourite: bool = False):
        """Created a SevedExperimentRequest instance"""
        return SavedExperimentRequest(
            name=self.name,
            user_id=self.user_id,
            device_id=self.device_id,
            description=self.description,
            experiment=self._encoded_experiment,
            results=self._encoded_results,
            favourite=favourite,
        )
