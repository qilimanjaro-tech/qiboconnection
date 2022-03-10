# quantum_device.apy
from .device import Device
from typeguard import typechecked
import json

from qiboconnection.typings.device import OfflineDeviceInput
from .quantum_device_characteristics import QuantumDeviceCharacteristics
from .quantum_device_calibration_details import CalibrationDetails


class OfflineDevice(Device):
    """Offline Device class"""

    @typechecked
    def __init__(self, device_input: OfflineDeviceInput):
        super().__init__(device_input)

        self._str = (f"<Offline Device: device_id={self._device_id},"
                     f" device_name='{self._device_name}',"
                     f" status='{self._status.value}>")

    def __str__(self) -> str:
        """String representation of an OfflineDevice

        Returns:
            str: String representation of a OfflineDevice
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of a OfflineDevice

        Returns:
            dict: Output dictionary of a OfflineDevice object
        """
        return super().__dict__()
