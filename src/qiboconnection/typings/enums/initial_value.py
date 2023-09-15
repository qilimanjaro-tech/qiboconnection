""" InitialValue enum """
from .str_enum import StrEnum


class InitialValue(StrEnum):
    """Initial Value

    Args:
        enum (str):name types of the initial values.
        Supported values are: 'zero', 'one', and 'random'
    """

    ZERO = "zero"
    ONE = "one"
    RANDOM = "random"
