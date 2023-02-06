""" Quantum Calibration Details """

from typeguard import typechecked

from qiboconnection.devices.device_details import DeviceDetails
from qiboconnection.typings.device import CalibrationDetailsInput


class CalibrationDetails(DeviceDetails):
    """Class representation of Quantum Calibration Details"""

    @typechecked
    def __init__(self, characteristics_input: CalibrationDetailsInput):
        super().__init__()

        self._elapsed_time = characteristics_input.elapsed_time
        self._t1 = characteristics_input.t1
        self._frequency = characteristics_input.frequency

        self._str = "<CalibrationDetails:"
        if self._elapsed_time:
            self._str += f" elapsed_time='{self._elapsed_time}'"
        if self._t1:
            self._str += f" t1='{self._t1}'"
        if self._frequency:
            self._str += f" frequency='{self._frequency}'"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of SimulatorDeviceCharacteristics

        Returns:
            dict: Output dictionary of SimulatorDeviceCharacteristics object
        """
        calibration_dict: dict = {}

        if self._elapsed_time:
            calibration_dict |= {"elapsed_time": self._elapsed_time}
        if self._t1:
            calibration_dict |= {"t1": self._t1}
        if self._frequency:
            calibration_dict |= {"frequency": self._frequency}
        return calibration_dict
