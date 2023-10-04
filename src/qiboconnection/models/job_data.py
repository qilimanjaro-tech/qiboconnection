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

""" Job Data Typing """
# pylint: disable=too-many-instance-attributes
# pylint: disable=E1101
from qibo.models import Circuit

from qiboconnection.api_utils import deserialize_job_description, parse_job_responses_to_results
from qiboconnection.models.job_response import JobResponse

# pylint: disable=super-init-not-called


class JobData(JobResponse):
    """Data shown to the user when get_job() method is used. It includes job human-readable results and metadata."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.result = parse_job_responses_to_results(job_responses=[JobResponse.from_kwargs(**kwargs)])[0]
        self.description = deserialize_job_description(base64_description=self.description, job_type=self.job_type)

        if not isinstance(self.result, (dict, type(None))):
            raise ValueError("Job result needs to be a dict!")

        if not isinstance(self.description, (dict, type(None), Circuit)):
            raise ValueError("Job description needs to be a dict of a Qibo Circuit!")

    def __repr__(self):
        # Use dataclass-like formatting, excluding attributes starting with an underscore
        attributes = [
            f"{attr}={getattr(self, attr)!r}"
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__") and attr != "_abc_impl"
        ]
        return f"JobData({', '.join(attributes)})"
