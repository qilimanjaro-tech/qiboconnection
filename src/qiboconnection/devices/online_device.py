""" Online Device """

from typeguard import typechecked

from qiboconnection.typings.device import OnlineDeviceInput

from .device import Device


class OnlineDevice(Device):
    """Online Device class"""

    @typechecked
    def __init__(self, device_input: OnlineDeviceInput):
        self._number_pending_jobs = None

        super().__init__(device_input)

        self._str = (
            f"<Online Device: device_id={self._device_id},"
            f" device_name='{self._device_name}',"
            f" status='{self._status.value}"
        )
        if self._number_pending_jobs is not None:
            self._str += f", number_pending_jobs={self._number_pending_jobs}"
        self._str += ">"
