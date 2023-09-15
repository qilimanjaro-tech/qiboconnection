""" PlottingResponse class """
from abc import ABC
from dataclasses import dataclass


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
