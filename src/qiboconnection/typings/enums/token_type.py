""" TokenType enum """
from .str_enum import StrEnum


class TokenType(StrEnum):
    """Token Type

    Args:
        enum (str): only available token type is 'bearer'
    """

    BEARER = "bearer"
