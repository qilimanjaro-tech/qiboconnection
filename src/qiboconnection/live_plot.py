""" LivePlot class """
import asyncio
import multiprocessing
import threading
from abc import ABC
from asyncio import create_task, run, subprocess
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
        self._send_queue_thread: threading.Thread | None = None

    async def start_up(self):
        """Sets up the queue, opens the connection and creates and starts the sending data thread"""
        self._send_queue = Queue()
        await self._open_connection()
        self._send_queue_thread = threading.Thread(target=asyncio.run, args=(self._sending_loop(),))
        self._send_queue_thread.start()

    def _setup_queue(self):
        self._send_queue = Queue()

    async def _sending_loop(self):
        """Main loop, where we send over the socket whatever there is in the _send_queue"""
        while True:
            print(f"queue size ({self._send_queue.qsize()}), consiming (1)")
            # packet: LivePlotPacket = self._send_queue.get()
            packet_list: List[LivePlotPacket] = []
            while not self._send_queue.empty():
                packet_list.append(self._send_queue.get())
            if agglutinated_packet := LivePlotPacket.agglutinate(packets=packet_list):
                try:
                    assert self._connection.open
                    await self._connection.send(agglutinated_packet.to_json())
                # except (AssertionError, AttributeError, ValueError,
                #         SSLError, WebSocketException, ConnectionClosed,
                #         Exception) as e:
                except Exception as e:
                    print(f"Found {e} {type(e)}, reopening")
                    await self._close_connection()
                    await self._open_connection()
                    await self._connection.send(agglutinated_packet.to_json())
            else:
                print("oops, no one home")
                await asyncio.sleep(0.1)

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
        if self._connection is not None:
            try:
                await self._connection.close()
            except (AttributeError, ValueError, SSLError, WebSocketException, ConnectionClosed):
                self._connection = None

    async def _open_connection(self):
        """
        Creates connection using self._websocket_url and saves it to self._connection.
        """
        try:
            self._connection = await websockets.connect(self._websocket_url)  # pylint: disable=no-member
            self._connection_open = True
        except Exception as e:
            raise ValueError("Server is refusing connections") from e
