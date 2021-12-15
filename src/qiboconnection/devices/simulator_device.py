# simulator_device.apy
from .device import Device
from typeguard import typechecked
import json

from qiboconnection.typings.device import SimulatorDeviceInput
from .simulator_device_characteristics import SimulatorDeviceCharacteristics


class SimulatorDevice(Device):
    """Simulator Device class"""

    @typechecked
    def __init__(self, device_input: SimulatorDeviceInput):
        self._characteristics = None

        if "characteristics" in device_input:
            self._characteristics = SimulatorDeviceCharacteristics(
                device_input["characteristics"]
            )
            device_input.pop("characteristics")

        super().__init__(device_input=device_input)

        self._str = f"<Simulator Device: device_id={self._device_id}, device_name='{self._device_name}', status='{self._status.value}'"
        if self._characteristics:
            self._str += f", characteristics={str(self._characteristics)}"
        self._str += ">"

    def __str__(self) -> str:
        """String representation of a SimulatorDevice

        Returns:
            str: String representation of a SimulatorDevice
        """
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __dict__(self) -> dict:
        """Dictionary representation of a SimulatorDevice

        Returns:
            dict: Output dictionary of a SimulatorDevice object
        """
        device_dict = super().__dict__()
        if self._characteristics:
            device_dict |= {"characteristics": self._characteristics.__dict__()}
        return device_dict
