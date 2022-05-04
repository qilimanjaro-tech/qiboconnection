""" LivePlots class """
from abc import ABC
from dataclasses import dataclass, field
from qiboconnection.live_plot import LivePlot
from qiboconnection.typings.live_plot import LivePlotType, LivePlotPacket

from typing import Callable
from functools import partial


@dataclass
class LivePlots(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    _live_plots: dict = field(default_factory=dict)

    def create_live_plot(self, plot_id: int, plot_type: LivePlotType, websocket_url: str, ):
        """Creates a new LivePlot with the provided information and appends it to the internal _live_plots dict"""
        self._live_plots[plot_id] = LivePlot(plot_id=plot_id, plot_type=plot_type, websocket_url=websocket_url)

    def _get_live_plot(self, plot_id) -> LivePlot:
        return self._live_plots[plot_id]

    class CheckDataAndPlotTypeCompatibility:
        """Function decorator used to check if the points desired to add to a live-plot are compatible with that."""

        def __init__(self, method: Callable):
            self._method = method

        def __get__(self, obj, objtype):
            """Support instance methods."""
            return partial(self.__call__, obj)

        def __call__(self, *args, **kwargs):
            """
            Args:
                method (Callable): Class method.
            Raises:
                AttributeError: live_plot and data_point are required.
                ValueError: Line plots accept exactly x and f values.
                ValueError: Scatter3D plots accept exactly x, y and f values.
            """
            if "live_plot" not in kwargs or "data_packet" not in kwargs:
                raise AttributeError("live_plot and point info are required.")
            live_plot, data_packet = kwargs.get("live_plot"), kwargs.get("data_packet")
            if (live_plot.plot_type == LivePlotType.LINES.value
                    and (data_packet.y is not None or data_packet.x is None or data_packet.f is None)):
                raise ValueError("Line plots accept exactly x and f values.")
            if (live_plot.plot_type == LivePlotType.SCATTER3D.value
                    and (data_packet.x is None or data_packet.y is None or data_packet.f is None)):
                raise ValueError("Scatter3D plots accept exactly x, y and f values.")

    def send_data(self, plot_id: int, x: list[float] | float, f: float, y: float | None = None):
        live_plot = self._get_live_plot(plot_id=plot_id)
        data_packet = LivePlotPacket.build_packet(plot_id=plot_id, plot_type=live_plot.plot_type, x=x, y=y, f=f)
        self._send_data(live_plot=live_plot, data_packet=data_packet)

    @CheckDataAndPlotTypeCompatibility
    def _send_data(self, live_plot: LivePlot, data_packet: LivePlotPacket):
        live_plot.send_data(data=data_packet)
