"""Simulator Device"""

from typeguard import typechecked

from qiboconnection.typings.device import SimulatorDeviceInput

from .online_device import OnlineDevice
from .simulator_device_characteristics import SimulatorDeviceCharacteristics


class SimulatorDevice(OnlineDevice):
    """Simulator Device class"""

    @typechecked
    def __init__(self, device_input: SimulatorDeviceInput):
        self._characteristics = (
            SimulatorDeviceCharacteristics(device_input.s_characteristics)
            if device_input.s_characteristics is not None
            else None
        )

        super().__init__(device_input=device_input)

        self._str = (
            f"<Simulator Device: device_id={self._device_id}, device_name='{self._device_name}'"
            f", status='{self._status.value}'"
        )
        if self._characteristics:
            self._str += f", characteristics={str(self._characteristics)}"
        self._str += ">"

    @property
    def __dict__(self):
        """Dictionary representation of a SimulatorDevice

        Returns:
            dict: Output dictionary of a SimulatorDevice object
        """
        device_dict = super().__dict__
        if self._characteristics:
            device_dict |= {"characteristics": self._characteristics.__dict__}
        return device_dict
