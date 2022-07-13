from abc import ABC
from dataclasses import asdict, dataclass

from qibo.models.circuit import Circuit


@dataclass
class Experiment(ABC):
    """Experiment skeleton, from QiliLab project."""

    platform_name: str
    parameter_name: str
    parameter_range: tuple[float]
    circuit: Circuit
