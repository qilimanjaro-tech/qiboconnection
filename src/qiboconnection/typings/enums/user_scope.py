""" UserScope enum """
from .str_enum import StrEnum


class UserScope(StrEnum):
    """User Scope

    Args:
        enum (str): the only available scope is 'user profile'
    """

    USER = "user profile"
