""" UserRole enum """
from .str_enum import StrEnum


class UserRole(StrEnum):
    """User Roles

    Args:
        enum (str): Available types of user roles:
        * user
        * admin
    """

    USER = "user"
    ADMIN = "admin"
