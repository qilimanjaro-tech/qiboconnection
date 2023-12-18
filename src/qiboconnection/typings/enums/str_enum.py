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

""" StrEnum base class """
from enum import Enum


class StrEnum(str, Enum):
    """Associates a number to each entry. Unlike a normal enum, this is not used for indexing, and adding the '.value'
    to everywhere is still not needed.
    This int can be used for where a string is not suitable."""

    @property
    def to_int(self):
        """Returns the int associated to the str entry in the enum class. Order is important."""
        return list(self.__class__).index(self)
