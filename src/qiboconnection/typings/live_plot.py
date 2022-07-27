""" Live Plot Typing """
import json
from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from functools import partial
from typing import Callable, List, TypedDict, cast

import numpy as np
import numpy.typing as npt


class LivePlotType(str, Enum):
    """
    Class for type
    """

    LINES = "LINES"
    SCATTER = "SCATTER"
    SCATTER3D = "SCATTER3D"
    HEATMAP = "HEATMAP"


class UnitPoint(TypedDict):
    """Basic point"""

    x: float
    y: float
    z: float | None
    idx: int | None
    idy: int | None


@dataclass
class PlottingResponse(ABC):
    """Class for typecasting the PlottingService responses for requesting the creation of new plots."""

    websocket_url: str
    plot_id: int

    @classmethod
    def from_response(cls, websocket_url: str, plot_id: str):
        """Builds a PlottingResponse from a response json, where everything could be a string."""
        return cls(websocket_url=websocket_url, plot_id=int(plot_id))

    def to_dict(self):
        """Casts the info of the class as a dict."""
        return {"websocket_url": self.websocket_url, "plot_id": self.plot_id}


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
