""" Connection Typing """

from abc import ABC
from dataclasses import dataclass


@dataclass
class ConnectionConfiguration(ABC):
    """Connection Configuration

    Attributes:
        user_id (int): The user id
        username (str): The user name
        api_key (str): The API key associated to the user
    """

    user_id: int
    username: str
    api_key: str


@dataclass
class ConnectionEstablished(ConnectionConfiguration):
    """Connection Established

    Attributes:
        authorisation_access_token (str): access token associated
        api_path (str): API path to use the token
    """

    authorisation_access_token: str
    api_path: str
