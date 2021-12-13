# user.py

from dataclasses import dataclass


@dataclass
class User:
    """ User class
    """
    id: int
    username: str
    api_key: str

    @property
    def __dict__(self) -> dict:
        return {
            'user_id': self.id,
            'username': self.username,
            'api_key': self.api_key
        }
