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

"""Job Data Typing"""

from inspect import signature

from qibo.models import Circuit  # type: ignore[import-untyped]

from qiboconnection.api_utils import deserialize_job_description, parse_job_response_to_result
from qiboconnection.typings.responses.job_response import JobResponse


class JobData(JobResponse):
    """Data shown to the user when get_job() method is used. It includes job human-readable results and metadata."""

    def __init__(self, **kwargs):
        super().__init__(**{key: kwargs[key] for key in set(signature(JobResponse).parameters)})
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.result = parse_job_response_to_result(job_response=JobResponse.from_kwargs(**kwargs))  # type: ignore
        self.description = deserialize_job_description(raw_description=self.description, job_type=self.job_type)

        if not isinstance(self.result, (dict, list, str, type(None))):
            raise ValueError("Job result needs to be a dict, a list, a string or a None!")
        if not isinstance(self.description, (dict, type(None), Circuit, list, str)):
            raise ValueError("Job description needs to be a Qibo Circuit, a dict, a list, a str or a None!")

    def __repr__(self):
        # Use dataclass-like formatting, excluding attributes starting with an underscore
        attributes = [
            f"{attr}={getattr(self, attr)!r}"
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__") and attr != "_abc_impl"
        ]
        return f"JobData({', '.join(attributes)})"
