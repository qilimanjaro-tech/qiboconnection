""" User """

from dataclasses import dataclass


@dataclass
class User:
    """User class"""

    user_id: int
    username: str
    api_key: str
