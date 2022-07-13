"""Quantum Device """
from typeguard import typechecked

from qiboconnection.typings.device import QuantumDeviceInput

from .online_device import OnlineDevice
from .quantum_device_calibration_details import CalibrationDetails
from .quantum_device_characteristics import QuantumDeviceCharacteristics


class QuantumDevice(OnlineDevice):
    """Quantum Device class"""

    @typechecked
    def __init__(self, device_input: QuantumDeviceInput):
        self._characteristics = (
            QuantumDeviceCharacteristics(device_input.q_characteristics)
            if device_input.q_characteristics is not None
            else None
        )
        self._last_calibration_time = device_input.last_calibration_time
        self._calibration_details = (
            CalibrationDetails(device_input.q_calibration_details)
            if device_input.q_calibration_details is not None
            else None
        )

        super().__init__(device_input)

        self._str = (
            f"<Quantum Device: device_id={self._device_id}, device_name='{self._device_name}'"
            f", status='{self._status.value}'"
        )
        if self._last_calibration_time:
            self._str += f", last_calibration_time={self._last_calibration_time}"
        if self._characteristics:
            self._str += f", characteristics={str(self._characteristics)}"
        if self._calibration_details:
            self._str += f", calibration_details={str(self._calibration_details)}"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of a QuantumDevice

        Returns:
            dict: Output dictionary of a QuantumDevice object
        """
        device_dict = super().__dict__

        if self._last_calibration_time:
            device_dict |= {"last_calibration_time": self._last_calibration_time}
        if self._characteristics:
            device_dict |= {"characteristics": self._characteristics.__dict__}
        if self._calibration_details:
            device_dict |= {"calibration_details": self._calibration_details.__dict__}
        return device_dict
