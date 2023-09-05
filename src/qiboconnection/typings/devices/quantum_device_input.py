""" Quantum Device Typing """
from dataclasses import InitVar, dataclass

from .calibration_details_input import CalibrationDetailsInput
from .online_device_input import OnlineDeviceInput
from .quantum_device_characteristics_input import QuantumDeviceCharacteristicsInput


@dataclass(kw_only=True)
class QuantumDeviceInput(OnlineDeviceInput):
    """Quantum Device Input"""

    last_calibration_time: str | None = ""
    characteristics: InitVar[dict | None] = None
    calibration_details: InitVar[dict | None] = None

    def __post_init__(self, characteristics, calibration_details):
        self._characteristics = QuantumDeviceCharacteristicsInput(**characteristics)
        self._calibration_details = CalibrationDetailsInput(**calibration_details)

    @property
    def q_characteristics(self):
        """Characteristics getter"""
        return self._characteristics

    @property
    def q_calibration_details(self):
        """Calibration details getter"""
        return self._calibration_details
