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
    api_path: str


@dataclass
class ConnectionEstablished(ConnectionConfiguration, _ConnectionEstablishedBase):
    """Connection Established

    Attributes:
        authorisation_access_token (str): access token associated
        api_path (str): API path to use the token
    """
