# algorithm.py

from dataclasses import dataclass
from typing import List, Optional
import enum


class AlgorithmType(enum.Enum):
    GATE_BASED = "Gate-Based Circuit"
    ANNEALING = "Annealing"


class InitialValue(enum.Enum):
    ZERO = "zero"
    ONE = "one"
    RANDOM = "random"


class AlgorithmName(str, enum.Enum):
    BELLSTATE = 'bell-state'


@dataclass
class AlgorithmOptions:
    """ Algorithm Options data class
    """
    number_qubits: str
    initial_value: Optional[InitialValue] = InitialValue.ZERO

    @property
    def __dict__(self) -> dict:
        return {
            'number_qubits': self.number_qubits,
            'initial_value': self.initial_value.value
        }


@dataclass
class AlgorithmDefinition:
    """ Algorithm data class
    """
    name: AlgorithmName
    type: AlgorithmType
    options: AlgorithmOptions

    @property
    def __dict__(self) -> dict:
        return {
            'name': self.name.value,
            'type': self.type.value,
            'options': self.options.__dict__,
        }


@dataclass
class ProgramDefinition:
    """ Program data class
    """
    algorithms: List[AlgorithmDefinition]
