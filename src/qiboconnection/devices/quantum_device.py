# quantum_device.apy
from .device import Device
from typeguard import typechecked
import json

from qiboconnection.typings.device import QuantumDeviceInput
from .quantum_device_characteristics import QuantumDeviceCharacteristics
from .quantum_device_calibration_details import CalibrationDetails


class QuantumDevice(Device):
    """Quantum Device class"""

    @typechecked
    def __init__(self, device_input: QuantumDeviceInput):
        self._characteristics = None
        self._last_calibration_time = None
        self._calibration_details = None

        if "last_calibration_time" in device_input:
            self._last_calibration_time = device_input["last_calibration_time"]
            device_input.pop("last_calibration_time")
        if "characteristics" in device_input:
            self._characteristics = QuantumDeviceCharacteristics(
                device_input["characteristics"]
            )
            device_input.pop("characteristics")
        if "calibration_details" in device_input:
            self._calibration_details = CalibrationDetails(
                device_input["calibration_details"]
            )
            device_input.pop("calibration_details")

        super().__init__(device_input)

        self._str = f"<Quantum Device: device_id={self._device_id}, device_name='{self._device_name}', status='{self._status.value}'"
        if self._last_calibration_time:
            self._str += f", last_calibration_time={self._last_calibration_time}"
        if self._characteristics:
            self._str += f", characteristics={str(self._characteristics)}"
        if self._calibration_details:
            self._str += f", calibration_details={str(self._calibration_details)}"
        self._str += ">"

    def __str__(self) -> str:
        """String representation of a QuantumDevice

        Returns:
            str: String representation of a QuantumDevice
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of a QuantumDevice

        Returns:
            dict: Output dictionary of a QuantumDevice object
        """
        device_dict = super().__dict__()

        if self._last_calibration_time:
            device_dict |= {"last_calibration_time": self._last_calibration_time}
        if self._characteristics:
            device_dict |= {"characteristics": self._characteristics.__dict__()}
        if self._calibration_details:
            device_dict |= {"calibration_details": self._calibration_details.__dict__()}
        return device_dict
