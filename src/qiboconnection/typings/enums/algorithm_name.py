""" AlgorithmName enum """
from .str_enum import StrEnum


class AlgorithmName(StrEnum):
    """Algorithm Name

    Args:
        enum (str): name of the algorithm.
        Supported values are: 'bell-state'
    """

    BELLSTATE = "bell-state"
