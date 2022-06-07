""" User """

from dataclasses import dataclass


@dataclass
class User:
    """User class"""

    username: str
    api_key: str
    user_id: int | None = None
