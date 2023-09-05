""" Algorithm Typing """

from dataclasses import dataclass
from typing import List, Optional

from qiboconnection.typings.enums import AlgorithmName, AlgorithmType, InitialValue


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
