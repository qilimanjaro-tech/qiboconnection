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

""" Calibration class"""

from dataclasses import field

from qiboconnection.typings.requests import CalibrationRequest
from qiboconnection.typings.responses import CalibrationResponse
from qiboconnection.util import base64_decode, base64url_encode, jsonify_dict_and_base64_encode


# pylint: disable=too-many-instance-attributes
# pylint: disable=no-member
class Calibration:
    """Calibration representation"""

    name: str
    description: str
    calibration: str
    id: int | None = field(default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def _encoded_calibration(self):
        """return base64-encoded stringified jsonified experiment"""
        return base64url_encode(self.calibration) if self.calibration is not None else None

    @classmethod
    def from_response(cls, response: CalibrationResponse):
        """Calibration constructor that takes in an instance from a CalibrationResponse"""
        return cls(
            id=response.calibration_id,
            created_at=response.created_at,
            updated_at=response.updated_at,
            name=response.name,
            description=response.description,
            user_id=response.user_id,
            device_id=response.device_id,
            calibration=base64_decode(response.calibration),
            qililab_version=response.qililab_version,
        )

    def calibration_request(self):
        """Created a Request instance"""
        return CalibrationRequest(
            name=self.name,
            user_id=self.user_id,
            device_id=self.device_id,
            description=self.description,
            calibration=self._encoded_calibration,
            qililab_version=self.qililab_version,
        )

    def __repr__(self):
        # Use dataclass-like formatting, excluding attributes starting with an underscore

        return (
            f"Calibration(name={self.name},id={self.id},description={self.description},calibration={self.calibration})"
        )
