""" GrantType enum """
from .str_enum import StrEnum


class GrantType(StrEnum):
    """Grant Type

    Args:
        enum (str): the only available grant type is urn:ietf:params:oauth:grant-type:jwt-bearer
    """

    JWT_BEARER = "urn:ietf:params:oauth:grant-type:jwt-bearer"
