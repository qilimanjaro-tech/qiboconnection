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

""" PlottingResponse class """
from abc import ABC
from dataclasses import dataclass


@dataclass
class PlottingResponse(ABC):
    """Class for typecasting the PlottingService responses for requesting the creation of new plots."""

    websocket_url: str
    plot_id: int

    @classmethod
    def from_response(cls, websocket_url: str, plot_id: str):
        """Builds a PlottingResponse from a response json, where everything could be a string."""
        return cls(websocket_url=websocket_url, plot_id=int(plot_id))

    def to_dict(self):
        """Casts the info of the class as a dict."""
        return {"websocket_url": self.websocket_url, "plot_id": self.plot_id}
