""" Offline Device """

from typeguard import typechecked

from qiboconnection.typings.device import OfflineDeviceInput

from .device import Device


class OfflineDevice(Device):
    """Offline Device class"""

    @typechecked
    def __init__(self, device_input: OfflineDeviceInput):
        super().__init__(device_input)

        self._str = (
            f"<Offline Device: device_id={self._device_id},"
            f" device_name='{self._device_name}',"
            f" status='{self._status.value}>"
        )
