""" LivePlot class """
from abc import ABC
from asyncio import Queue, create_task, run
from ssl import SSLError
from typing import Optional

import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException

from qiboconnection.config import logger
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotType,
)


class LivePlot(ABC):
    """Job class to manage the job experiment to be remotely sent"""

    def __init__(
        self, plot_id: int, plot_type: LivePlotType, websocket_url: str, labels: LivePlotLabels, axis: LivePlotAxis
    ):
        """Default constructor. _connection is left as None until it is tried to use"""
        self._plot_id: int = plot_id
        self._plot_type: LivePlotType = plot_type
        self._labels: LivePlotLabels = labels
        self._axis: LivePlotAxis = axis
        self._websocket_url: str = websocket_url
        self._connection = None
        self._connection_open = False
        self._send_queue: Queue | None = None

        create_task(self._start_up())

    async def _start_up(self):
        self._send_queue = Queue()
        await self._open_connection()
        await self._sending_loop()

    async def _sending_loop(self):
        """Main loop, where we send over the socket whatever there is in the _send_queue"""
        while True:
            packet: LivePlotPacket = await self._send_queue.get()
            try:
                await self._connection.send(packet.to_json())
            except (AttributeError, ValueError, SSLError, WebSocketException, ConnectionClosed):
                self._close_connection()
                await self._open_connection()
                await self._connection.send(packet.to_json())

    @property
    def plot_id(self) -> int:
        """Gets the plot_id."""
        return self._plot_id

    @property
    def plot_type(self) -> LivePlotType:
        """Gets the plot_type."""
        return self._plot_type

    @property
    def labels(self) -> LivePlotLabels:
        """Gets the plot_type."""
        return self._labels

    @property
    def axis(self) -> LivePlotAxis:
        """Gets the plot_type."""
        return self._axis

    async def send_data(self, data: LivePlotPacket):
        """Sends a LivePlotPacket over the websocket connection.
        Returns:
            Length of message sent.
        """
        if self._send_queue is not None:
            await self._send_queue.put(data)

    def _close_connection(self):
        """
        Closes the created connection and restores the variable to None.
        """
        if self._connection is not None:
            try:
                self._connection.close()
            except (AttributeError, ValueError, SSLError, WebSocketException, ConnectionClosed):
                self._connection = None

    async def _open_connection(self):
        """
        Creates connection using self._websocket_url and saves it to self._connection.
        """
        try:
            self._connection = await websockets.client.connect(self._websocket_url)
            self._connection_open = True
        except ConnectionRefusedError:
            self._close_connection()
