""" LivePlot class """
from abc import ABC
from ssl import SSLError
from websocket import create_connection, WebSocketException, WebSocket
from typing import Optional
from qiboconnection.typings.live_plot import LivePlotType, LivePlotPacket


class LivePlot(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    def __init__(self, plot_id: int, plot_type: LivePlotType, websocket_url: str):

        self._plot_id: int = plot_id
        self._plot_type: LivePlotType = plot_type
        self._websocket_url: str = websocket_url
        self._connection: Optional[WebSocket] = None

    @property
    def plot_id(self) -> int:
        """Gets the plot_id."""
        return self._plot_id

    @property
    def plot_type(self) -> LivePlotType:
        """Gets the plot_type."""
        return self._plot_type

    def send_data(self, data: LivePlotPacket):
        """Sends a LivePlotPacket over the websocket connection.
        Returns:
            Length of message sent.
        """
        try:
            return self._send_data_over_connection(data=data)
        except (AttributeError, SSLError, WebSocketException):
            self._open_connection()
            return self._send_data_over_connection(data=data)

    def _send_data_over_connection(self, data: LivePlotPacket):
        return self._connection.send(data.to_json())

    def _open_connection(self):
        self._connection = create_connection(url=self._websocket_url)
