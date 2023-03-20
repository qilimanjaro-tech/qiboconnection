""" LivePlot class """

import asyncio
import contextlib
import datetime
import os
import threading
import time
from abc import ABC
from dataclasses import asdict
from queue import Queue
from ssl import SSLError
from typing import List

import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException

from qiboconnection.config import logger
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotType,
)

WEBSOCKET_CONNECTION_LIFETIME = int(os.getenv("QIBOCONNECTION_WEBSOCKET_CONNECTION_LIFETIME", default="5"))
PACKET_POINT_NUMBER_LIMIT = int(os.getenv("QIBOCONNECTION_PACKET_POINT_NUMBER_LIMIT", default="1000"))


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
        # pylint: disable=no-member
        self._connection: websockets.WebSocketClientProtocol | None = None  # type: ignore [name-defined]
        self._connection_open = False
        self._send_queue: Queue | None = None
        self._send_queue_thread: threading.Thread | None = None
        self._connection_started_at: datetime.datetime | None = None

    async def start_up(self):
        """Sets up the queue, opens the connection and creates and starts the sending data thread"""
        self._setup_queue()
        await self._open_connection()
        self._setup_sending_thread()

    def _setup_queue(self):
        """Sets up an empty queue"""
        self._send_queue = Queue()

    def _setup_sending_thread(self):
        """Sets up and starts the sending thread"""
        self._send_queue_thread = threading.Thread(target=asyncio.run, args=(self._sending_loop(),))
        self._send_queue_thread.daemon = True
        self._send_queue_thread.start()

    async def _reset_connection_if_opened_for_too_long(self):
        """Resets the connection if it has been up for too long"""
        elapsed_time = datetime.datetime.now() - self._connection_started_at
        if elapsed_time.seconds > WEBSOCKET_CONNECTION_LIFETIME:
            await self._reset_connection()

    def _consume_and_agglutinate_all_packets_in_queue(self):
        """Consumes all packets in queue into a list and agglutinates them into a single packet"""

        packet_list: List[LivePlotPacket] = []
        while not self._send_queue.empty() and len(packet_list) < PACKET_POINT_NUMBER_LIMIT:
            packet_list.append(self._send_queue.get())
        return LivePlotPacket.agglutinate(packets=packet_list)

    @property
    def connection_open(self):
        """Return true if the connection is open"""
        return self._connection.open if self._connection else False

    def ensure_connection_open(self):
        """Raises ValueError if the connection is not open

        Raises:
           ValueError: The connection is not open
        """
        if not self.connection_open:
            raise ValueError("The connection is not open")

    async def _sending_loop(self):
        """Main loop, where we send over the socket whatever there is in the _send_queue"""
        while True:
            await self._reset_connection_if_opened_for_too_long()

            if agglutinated_packet := self._consume_and_agglutinate_all_packets_in_queue():
                agglutinated_message = agglutinated_packet.to_json()
                try:
                    self.ensure_connection_open()
                    await self._connection.send(agglutinated_message)
                except (
                    AssertionError,
                    AttributeError,
                    ValueError,
                    SSLError,
                    WebSocketException,
                    ConnectionClosed,
                ) as ex:
                    logger.debug(f"Found error {ex} ({type(ex)}) while plotting. Resetting connection")
                    await self._reset_connection()
                    await self._connection.send(agglutinated_message)
            else:
                time.sleep(0.2)

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
        if self._send_queue is None:
            self._setup_queue()
        if isinstance(self._send_queue, Queue):
            self._send_queue.put(data)
            return
        raise ValueError("Queue was not properly set up")

    async def _close_connection(self):
        """
        Closes the created connection and restores the variable to None.
        """
        logger.debug("Closing connection")
        if self._connection is not None:
            with contextlib.suppress(AttributeError, ValueError, SSLError, WebSocketException, ConnectionClosed):
                await self._connection.close()
            self._connection = None
            self._connection_started_at = None

    async def _open_connection(self):
        """
        Creates connection using self._websocket_url and saves it to self._connection.
        """
        logger.debug("Opening connection")
        try:
            self._connection = await websockets.connect(self._websocket_url)  # pylint: disable=no-member
            self._connection_started_at = datetime.datetime.now()
        except Exception as ex:
            raise ValueError("Server is refusing connections") from ex

    async def _reset_connection(self):
        """
        Resets the connection.
        """
        logger.debug("Resetting connection")
        await self._close_connection()
        await self._open_connection()

    def __eq__(self, other):
        return (
            (
                other.plot_id == self.plot_id
                and other.plot_type == self.plot_type
                and asdict(other.axis) == asdict(self.axis)
                and asdict(self.labels) == asdict(self.labels)
                and other._websocket_url == self._websocket_url
            )
            if isinstance(other, LivePlot)
            else False
        )
