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
""" JobListingItem class """

from dataclasses import field

from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.responses import JobListingItemResponse
from qiboconnection.util import from_kwargs


class JobListingItem:  # pylint: disable=too-few-public-methods
    """JobListing single item representation."""

    user_id: int
    device_id: int
    status: str | JobStatus
    job_type: str | JobType
    number_shots: int
    id: int | None = field(default=None)

    @classmethod
    def from_response(cls, response: JobListingItemResponse):
        """Constructor for JobListingItems that takes in a JobListingItemResponse"""
        return from_kwargs(cls, **response.__dict__)
