""" Simulator Device Input Typing """
from dataclasses import InitVar, dataclass

from .online_device_input import OnlineDeviceInput
from .simulator_device_characteristics_input import SimulatorDeviceCharacteristicsInput


@dataclass(kw_only=True)
class SimulatorDeviceInput(OnlineDeviceInput):
    """Simulator Device Input"""

    characteristics: InitVar[dict | None] = None

    def __post_init__(self, characteristics):
        self._characteristics = SimulatorDeviceCharacteristicsInput(**characteristics)

    @property
    def s_characteristics(self):
        """Characteristics getter"""
        return self._characteristics
