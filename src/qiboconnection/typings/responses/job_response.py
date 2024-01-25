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
""" JobResponse """
from dataclasses import dataclass

from qiboconnection.util import from_kwargs

from ..requests import JobRequest


@dataclass
class JobResponse(JobRequest):
    """Full Job Response. Includes job results which may
    be weight a few GB.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        job_id (int): Job identifier
        queue_position (int): Job queue position
        status (str): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    result: str
    status: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Returns an instance of JobResponse including non-typed attributes"""
        return from_kwargs(cls, **kwargs)
