# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Live Plot Typing """
import json
from abc import ABC
from dataclasses import asdict, dataclass
from functools import partial
from typing import Callable, List, TypedDict, cast

import numpy as np
import numpy.typing as npt

from .enums import LivePlotType


class UnitPoint(TypedDict):
    """Basic point"""

    x: float
    y: float
    z: float | None
    idx: int | None
    idy: int | None


@dataclass
class LivePlotLabels(ABC):
    """Class for holding different labels for the plots: title, axis names, etc."""

    title: str | None = None
    x_label: str | None = None
    y_label: str | None = None
    z_label: str | None = None


@dataclass
class LivePlotAxis(ABC):
    """Class for holding different axis marks for the plots"""

    x_axis: npt.NDArray | List | None = None
    y_axis: npt.NDArray | List | None = None


class LivePlotPoints(ABC):
    """Information about the points we intend to plot in each message we sent over the live-plotting ws."""

    def __init__(
        self,
        x: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_],
        y: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_],
        z: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_] | None = None,
        idx: int | list[int] | npt.NDArray[np.int_] | None = None,
        idy: int | list[int] | npt.NDArray[np.int_] | None = None,
    ):
        self._x = x
        self._y = y
        self._z = z
        self._idx = idx
        self._idy = idy
        self._points: list[UnitPoint] = []
        self._parse_to_points(x=x, y=y, z=z, idx=idx, idy=idy)

    @property
    def x(self):
        """x getter."""
        return self._x

    @property
    def y(self):
        """y getter."""
        return self._y

    @property
    def z(self):
        """z getter."""
        return self._z

    @property
    def idx(self):
        """idx getter."""
        return self._idx

    @property
    def idy(self):
        """idy getter."""
        return self._idy

    def _parse_to_points(
        self,
        x: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_],
        y: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_],
        z: int | float | list[int] | list[float] | npt.NDArray[np.int_ | np.float_] | None = None,
        idx: int | list[int] | npt.NDArray[np.int_] | None = None,
        idy: int | list[int] | npt.NDArray[np.int_] | None = None,
    ):
        """
        Gets a point or a list of points for x, y, and z and parses them to a list of dicts each containing ONE value
         for each of x, y, z.
        Args:
            x: x value of the point(s) to draw
            y: y value of the point(s) to draw
            z: z value of the point(s) to draw
        Raises:
            ValueError: Arguments provided must be of the same type: floats or lists
        """
        if all(isinstance(arg, int | float | None) for arg in [x, y, z]):
            point = UnitPoint(x=cast(float, x), y=cast(float, y), z=None, idx=None, idy=None)
            if z is not None:
                point["z"] = cast(float, z)
            if idx is not None:
                point["idx"] = cast(int, idx)
            if idy is not None:
                point["idy"] = cast(int, idy)
            self._points.append(point)
        elif all(isinstance(arg, np.ndarray | list | None) for arg in [x, y, z]):
            x, y = cast(list, x), cast(list, y)
            for i, _ in enumerate(x):
                # pylint: disable=unnecessary-list-index-lookup
                point = UnitPoint(x=x[i], y=y[i], z=None, idx=None, idy=None)
                if z is not None:
                    point["z"] = cast(list, z)[i]
                if idx is not None:
                    point["idx"] = cast(list, idx)[i]
                if idy is not None:
                    point["idy"] = cast(list, idy)[i]
                self._points.append(point)
        else:
            raise ValueError("Arguments provided must be of the same type: floats or lists")

    def to_scatter(self):
        """Returns the points in the shape of [{x:x0, y:y0, f:f0}, {x:x1, y:y1, f:f1}, ...]"""
        return self._points

    def __eq__(self, other):
        if isinstance(other, LivePlotPoints):
            return all(
                [
                    self.x == other.x,
                    self.y == other.y,
                    self.z == other.z,
                    self._idx == other._idx,
                    self._idy == other._idy,
                ]
            )
        return False


def _ensure_packet_types(packets: List):
    """Ensures all elements are valid LivePlotPackets"""
    if not all(isinstance(packet, LivePlotPacket) for packet in packets):
        raise ValueError("Not all packets were LivePlotPackets")


def _ensure_packet_compatibility(packets: List):
    """Ensures all elements of packets are from a same compatible Liveplot"""
    same_plot_id = (packet.plot_id == packets[0].plot_id for packet in packets)
    same_plot_type = (packet.plot_type == packets[0].plot_type for packet in packets)
    same_labels = (packet.labels == packets[0].labels for packet in packets)
    same_axis = (packet.axis == packets[0].axis for packet in packets)
    if not (all(same_plot_id) and all(same_plot_type) and all(same_labels) and all(same_axis)):
        raise ValueError("Trying to agglutinate data packets with different information")


@dataclass
class LivePlotPacket(ABC):
    """Packet with the needed information for sending in each message we want to throw over the live-plotting ws."""

    plot_id: int
    plot_type: LivePlotType
    data: LivePlotPoints
    labels: LivePlotLabels
    axis: LivePlotAxis

    class ParseDataIfNeeded:
        """Function decorator used to add extra kwargs to the provided points before sending them, and to downcast
        provided data into json-serializable datatypes."""

        def __init__(self, method: Callable):
            self._method = method

        def __get__(self, obj, objtype):
            """Support instance methods."""
            return partial(self.__call__, obj)

        def __call__(self, *args, **kwargs):
            """
            Args:
                method (Callable): Class method.
            """

            downcasted_kwargs = self._downcast_ndarrays_to_lists(**kwargs)
            extended_kwargs = self._add_index_args_for_heatmaps(**downcasted_kwargs)

            return self._method(*args, **extended_kwargs)

        def _downcast_ndarrays_to_lists(self, **kwargs):
            """Downcasts all provided numpy arrays to lists"""
            for key, value in kwargs.items():
                if isinstance(value, np.ndarray):
                    kwargs[key] = value.tolist()

            return kwargs

        def _add_index_args_for_heatmaps(self, **kwargs):
            plot_type: LivePlotAxis = kwargs.get("plot_type")
            if plot_type == LivePlotType.HEATMAP:
                axis: LivePlotAxis = kwargs.get("axis")

                x: List[float | int] | float | int = kwargs.get("x")
                y: List[float | int] | float | int = kwargs.get("y")
                idx = None
                idy = None

                if isinstance(x, list) and isinstance(y, list):
                    idx = [int(np.where(np.unique(axis.x_axis) == i)[0][0]) for i in x]
                    idy = [int(np.where(np.unique(axis.y_axis) == i)[0][0]) for i in y]
                if isinstance(x, (float, int)) and isinstance(y, (float, int)):
                    idx = int(np.where(np.unique(axis.x_axis) == x)[0][0])
                    idy = int(np.where(np.unique(axis.y_axis) == y)[0][0])

                return {**kwargs, "idx": idx, "idy": idy}
            return kwargs

    @classmethod
    @ParseDataIfNeeded
    def build_packet(
        cls,
        plot_id: int,
        plot_type: LivePlotType,
        labels: LivePlotLabels,
        axis: LivePlotAxis,
        x: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        y: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        z: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int | None,
        idx: npt.NDArray[np.int_] | list[int] | int | None = None,
        idy: npt.NDArray[np.int_] | list[int] | int | None = None,
    ):
        """Convenience constructor"""
        return cls(
            plot_id=plot_id,
            plot_type=plot_type,
            labels=labels,
            axis=axis,
            data=LivePlotPoints(x=x, y=y, z=z, idx=idx, idy=idy),
        )

    def to_dict(self) -> dict:
        """
        Serializes the information of the class to a dict ready to be sent via ws.
        """
        return {
            "plot_id": self.plot_id,
            "plot_type": self.plot_type.value,
            "labels": asdict(self.labels),
            "data": self.data.to_scatter(),
        }

    def to_json(self) -> str:
        """
        Serializes the info of the class in a json-formatted string
        """
        return json.dumps(self.to_dict())

    @classmethod
    def agglutinate(cls, packets: List):
        """Build a single LivePlotPacket from a list of LivePlotPackets with the data merged"""

        if not packets:
            return None

        _ensure_packet_types(packets=packets)
        _ensure_packet_compatibility(packets=packets)

        extended_x: list[int] | list[float] = list[float]()
        extended_y: list[int] | list[float] = list[float]()
        extended_z: list[int] | list[float] = list[float]()
        extended_idx: list[int] = list[int]()
        extended_idy: list[int] = list[int]()
        extended_x.extend((packet.data.x for packet in packets))
        extended_y.extend((packet.data.y for packet in packets))
        extended_z.extend((packet.data.z for packet in packets))
        extended_idx.extend((packet.data.idx for packet in packets))
        extended_idy.extend((packet.data.idy for packet in packets))
        return cls(
            plot_id=packets[0].plot_id,
            plot_type=packets[0].plot_type,
            data=LivePlotPoints(x=extended_x, y=extended_y, z=extended_z, idx=extended_idx, idy=extended_idy),
            labels=packets[0].labels,
            axis=packets[0].axis,
        )
