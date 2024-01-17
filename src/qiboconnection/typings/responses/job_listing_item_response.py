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

""" JobListingItemResponse typing """

from dataclasses import dataclass, field

from qiboconnection.util import from_kwargs


@dataclass
class JobListingItemResponse:
    """Job Response without the results. Includes all jobs metadata so that
    the user can identify the id from the job he is interested to retrieve the results.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier

        id (int): Job identifier
        status (str): Status of the job
    """

    status: str
    user_id: int
    device_id: int
    job_type: str
    number_shots: int
    id: int | None = field(default=None)

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Returns an instance of the class including non-typed attributes"""
        return from_kwargs(cls, **kwargs)

    def to_dict(self):
        """Convert into dict, including non-typed attributes"""
        return self.__dict__
