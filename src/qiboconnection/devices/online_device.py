# quantum_device.apy
from .device import Device
from typeguard import typechecked
import json

from qiboconnection.typings.device import OnlineDeviceInput


class OnlineDevice(Device):
    """Online Device class"""

    @typechecked
    def __init__(self, device_input: OnlineDeviceInput):
        self._number_pending_jobs = None

        if 'number_pending_jobs' in device_input:
            self._number_pending_jobs = device_input['number_pending_jobs']
            device_input.pop('number_pending_jobs')

        super().__init__(device_input)

        self._str = (f"<Online Device: device_id={self._device_id},"
                     f" device_name='{self._device_name}',"
                     f" status='{self._status.value}")
        if self._number_pending_jobs is not None:
            self._str += f", number_pending_jobs={self._number_pending_jobs}"
        self._str += '>'

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
