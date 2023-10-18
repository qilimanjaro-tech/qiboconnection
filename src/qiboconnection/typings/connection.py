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

""" Connection Typing """

from abc import ABC
from dataclasses import dataclass


@dataclass
class _ConnectionConfigurationDefaultBase(ABC):
    """Internal class for the default-value attributes of ConnectionConfiguration"""

    user_id: int | None = None


@dataclass
class _ConnectionConfigurationBase(ABC):
    """Internal class for the non-default-value attributes of ConnectionConfiguration"""

    username: str
    api_key: str


@dataclass
class ConnectionConfiguration(_ConnectionConfigurationDefaultBase, _ConnectionConfigurationBase):
    """Connection Configuration

    Attributes:
        user_id (int): The user id
        username (str): The user name
        api_key (str): The API key associated to the user
    """


@dataclass
class _ConnectionEstablishedBase(ABC):
    """Internal class for the non-default-value attributes of ConnectionEstablished"""

    authorisation_access_token: str
    authorisation_refresh_token: str
    api_path: str


@dataclass
class ConnectionEstablished(ConnectionConfiguration, _ConnectionEstablishedBase):
    """Connection Established

    Attributes:
        user_id (int): The user id
        username (str): The user name
        api_key (str): The API key associated to the user
        authorisation_access_token (str): access token associated
        authorisation_refresh_token (str): refresh token associated
        api_path (str): API path to use the token
    """
