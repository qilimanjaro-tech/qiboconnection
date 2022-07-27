""" LivePlots class """
from abc import ABC
from dataclasses import dataclass, field
from functools import partial
from typing import Callable

import numpy as np
import numpy.typing as npt

from qiboconnection.live_plot import LivePlot
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotType,
)


@dataclass
class LivePlots(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    _live_plots: dict = field(default_factory=dict)

    def create_live_plot(
        self, plot_id: int, plot_type: LivePlotType, websocket_url: str, labels: LivePlotLabels, axis: LivePlotAxis
    ):
        """Creates a new LivePlot with the provided information and appends it to the internal _live_plots dict"""
        self._live_plots[plot_id] = LivePlot(
            plot_id=plot_id,
            plot_type=plot_type,
            websocket_url=websocket_url,
            labels=labels,
            axis=axis,
        )

    def _get_live_plot(self, plot_id: int) -> LivePlot:
        """
        Internal getter that returns the liveplot instance associatied to the provided plot_id
        Args:
            plot_id: id of the plot to be retrieved.
        """
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
            if (
                "live_plot" not in kwargs
                or kwargs["live_plot"] is None
                or "data_packet" not in kwargs
                or kwargs["data_packet"] is None
            ):
                raise AttributeError("live_plot and point info are required.")
            live_plot: LivePlot = kwargs.get("live_plot")
            data_packet: LivePlotPacket = kwargs.get("data_packet")
            if live_plot.plot_type in (LivePlotType.LINES, LivePlotType.SCATTER) and (
                data_packet.data.z is not None or data_packet.data.x is None or data_packet.data.y is None
            ):
                raise ValueError("LINES and SCATTER plots accept exactly x and y values.")
            if live_plot.plot_type == LivePlotType.SCATTER3D and (
                data_packet.data.x is None or data_packet.data.y is None or data_packet.data.z is None
            ):
                raise ValueError("SCATTER3D plots accept exactly x, y and z values.")

            if live_plot.plot_type == LivePlotType.HEATMAP and (
                data_packet.data.x is None or data_packet.data.y is None or data_packet.data.z is None
            ):
                raise ValueError("HEATMAP plots accept exactly x, y and z values.")

            if live_plot.plot_type == LivePlotType.HEATMAP and (
                live_plot.axis.x_axis is None or live_plot.axis.y_axis is None
            ):
                raise ValueError("HEATMAP plots need to have axis provided on live-plot creation.")

            return self._method(*args, **kwargs)

    def send_data(
        self,
        plot_id: int,
        x: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        y: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        z: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int | None,
    ):
        """
        Send the data corresponding to one or more points over the ws connection associated to the plot represented by
        the provided plot_id
        Args:
            plot_id: id of the plot to send points to
            x: x value of the point(s) to be drawn
            y: y value of the point(s) to be drawn
            z: z value of the point(s) to be drawn
        """
        live_plot = self._get_live_plot(plot_id=plot_id)
        data_packet = LivePlotPacket.build_packet(
            plot_id=live_plot.plot_id,
            plot_type=live_plot.plot_type,
            x=x,
            y=y,
            z=z,
            labels=live_plot.labels,
            axis=live_plot.axis,
        )
        self._send_data(live_plot=live_plot, data_packet=data_packet)

    @CheckDataAndPlotTypeCompatibility
    def _send_data(self, live_plot: LivePlot, data_packet: LivePlotPacket):
        return live_plot.send_data(data=data_packet)
