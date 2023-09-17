""" AlgorithmType enum """
from .str_enum import StrEnum


class AlgorithmType(StrEnum):
    """Type of algorithm

    Args:
        enum (str):name types of the initial values.
        Supported values are: 'Gate-Based Circuit' and 'Annealing'
    """

    GATE_BASED = "Gate-Based Circuit"
    ANNEALING = "Annealing"
