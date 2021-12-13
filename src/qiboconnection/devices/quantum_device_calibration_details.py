# quantum_device_calibration_details.py
from abc import ABC
from typeguard import typechecked
import json

from qiboconnection.typings.device import CalibrationDetailsInput


class CalibrationDetails(ABC):
    """Class representation of Quantum Calibration Details"""

    @typechecked
    def __init__(self, characteristics_input: CalibrationDetailsInput):

        self._elapsed_time = characteristics_input.get("elapsed_time")
        self._t1 = characteristics_input.get("t1")
        self._frequency = characteristics_input.get("frequency")

        self._str = f"<CalibrationDetails:"
        if self._elapsed_time:
            self._str += f" elapsed_time='{self._elapsed_time}'"
        if self._t1:
            self._str += f" t1='{self._t1}'"
        if self._frequency:
            self._str += f" frequency='{self._frequency}'"
        self._str += ">"

    def __str__(self) -> str:
        """String representation of SimulatorDeviceCharacteristics

        Returns:
            str: String representation SimulatorDeviceCharacteristics
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of SimulatorDeviceCharacteristics

        Returns:
            dict: Output dictionary of SimulatorDeviceCharacteristics object
        """
        calibration_dict = {}

        if self._elapsed_time:
            calibration_dict |= {"elapsed_time": self._elapsed_time}
        if self._t1:
            calibration_dict |= {"t1": self._t1}
        if self._frequency:
            calibration_dict |= {"frequency": self._frequency}
        return calibration_dict

    def toJSON(self) -> str:
        """JSON representation of SimulatorDeviceCharacteristics

        Returns:
            str: JSON serialization of SimulatorDeviceCharacteristics object
        """

        return json.dumps(self.__dict__(), indent=2)
