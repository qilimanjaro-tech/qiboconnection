""" Algorithm Typing """

import enum
from dataclasses import dataclass
from typing import List, Optional


class AlgorithmType(enum.Enum):
    """Type of algorithm

    Args:
        enum (str):name types of the initial values.
        Supported values are: 'Gate-Based Circuit' and 'Annealing'
    """

    GATE_BASED = "Gate-Based Circuit"
    ANNEALING = "Annealing"


class InitialValue(enum.Enum):
    """Initial Value

    Args:
        enum (str):name types of the initial values.
        Supported values are: 'zero', 'one', and 'random'
    """

    ZERO = "zero"
    ONE = "one"
    RANDOM = "random"


class AlgorithmName(enum.Enum):
    """Algorithm Name

    Args:
        enum (str): name of the algorithm.
        Supported values are: 'bell-state'
    """

    BELLSTATE = "bell-state"


@dataclass
class AlgorithmOptions:
    """Algorithm Options data class"""

    number_qubits: int
    initial_value: Optional[InitialValue] = InitialValue.ZERO

    @property
    def __dict__(self):
        """
        Build class dict.
        Returns:
            dict: representation of the class
        """
        return {"number_qubits": self.number_qubits, "initial_value": self.initial_value.value}


@dataclass
class AlgorithmDefinition:
    """Algorithm data class"""

    name: AlgorithmName
    algorithm_type: AlgorithmType
    options: AlgorithmOptions

    @property
    def __dict__(self):
        """
        Build class dict.
        Returns:
            dict: representation of the class
        """
        return {
            "name": self.name.value,
            "type": self.algorithm_type.value,
            "options": self.options.__dict__,
        }


@dataclass
class ProgramDefinition:
    """Program data class"""

    algorithms: List[AlgorithmDefinition]
