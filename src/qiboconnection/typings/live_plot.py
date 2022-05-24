""" Live Plot Typing """
import json
from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional, TypedDict, cast


class LivePlotType(str, Enum):
    """
    Class for type
    """

    LINES = "LINES"
    SCATTER3D = "SCATTER3D"


class UnitPoint(TypedDict):
    """Basic point"""

    x: float
    y: float
    z: Optional[float]


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


class LivePlotPoints(ABC):
    """Information about the points we intend to plot in each message we sent over the live-plotting ws."""

    def __init__(self, x: float | list[float], y: float | list[float], z: Optional[float | list[float]] = None):
        self._x = x
        self._y = y
        self._z = z
        self._points: list[UnitPoint] = []
        self._parse_to_points(x=x, y=y, z=z)

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

    def _parse_to_points(self, x: float | list[float], y: float | list[float], z: Optional[float | list[float]] = None):
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
        if all((isinstance(arg, float) or arg is None) for arg in [x, y, z]):
            point = UnitPoint(x=cast(float, x), y=cast(float, y), z=None)
            if z is not None:
                point["z"] = cast(float, z)
            self._points.append(point)
        elif all((isinstance(arg, list) or arg is None) for arg in [x, y, z]):
            x, y = cast(list, x), cast(list, y)
            for i, _ in enumerate(x):
                point = UnitPoint(x=x[i], y=y[i], z=None)
                if z is not None:
                    point["z"] = cast(list, z)[i]
                self._points.append(point)
        else:
            raise ValueError("Arguments provided must be of the same type: floats or lists")

    def to_scatter(self):
        """Returns the points in the shape of [{x:x0, y:y0, f:f0}, {x:x1, y:y1, f:f1}, ...]"""
        return self._points


@dataclass
class LivePlotPacket(ABC):
    """Packet with the needed information for sending in each message we want to throw over the live-plotting ws."""

    plot_id: int
    plot_type: LivePlotType
    data: LivePlotPoints
    labels: LivePlotLabels

    @classmethod
    def build_packet(
        cls,
        plot_id: int,
        plot_type: LivePlotType,
        labels: LivePlotLabels,
        x: list[float] | float,
        y: list[float] | float,
        z: Optional[list[float] | float],
    ):
        """Convenience constructor"""
        return cls(plot_id=plot_id, plot_type=plot_type, labels=labels, data=LivePlotPoints(x=x, y=y, z=z))

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
