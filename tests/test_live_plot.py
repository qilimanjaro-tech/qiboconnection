""" Tests methods for LivePlot """

import asyncio
import datetime
import json
import threading
import time
from dataclasses import asdict
from queue import Queue
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import websockets

from qiboconnection.live_plot import WEBSOCKET_CONNECTION_LIFETIME, LivePlot
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotPoints,
    LivePlotType,
    PlottingResponse,
)

from .data import heatmap_unit_plot_points, unit_plot_point


@pytest.fixture(name="live_plot_type")
def fixture_plot_type():
    return LivePlotType.LINES


@pytest.fixture(name="live_plot_labels")
def fixture_plot_labels():
    return LivePlotLabels()


@pytest.fixture(name="live_plot_axis")
def fixture_plot_axis():
    return LivePlotAxis()


def test_live_plot(live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis):
    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    assert live_plot.plot_id == plot_id
    assert live_plot.plot_type == live_plot_type
    assert live_plot.labels == live_plot_labels
    assert live_plot.axis == live_plot_axis


@pytest.fixture(name="live_plot_points")
def fixture_live_plot_points() -> LivePlotPoints:
    return LivePlotPoints(x=unit_plot_point[0]["x"], y=unit_plot_point[0]["y"])


def test_live_plot_points_constructor(live_plot_points: LivePlotPoints):
    assert isinstance(live_plot_points, LivePlotPoints)
    assert live_plot_points.x == unit_plot_point[0]["x"]
    assert live_plot_points.y == unit_plot_point[0]["y"]
    assert live_plot_points.to_scatter() == [unit_plot_point[0]]


def test_live_plot_points_equality(live_plot_points: LivePlotPoints):
    live_plot_points_1 = LivePlotPoints(x=0, y=0)
    live_plot_points_2 = LivePlotPoints(x=0, y=0)
    assert live_plot_points_1 == live_plot_points_2

    live_plot_points_3 = LivePlotPoints(x=0, y=0, z=0)
    assert live_plot_points_1 != live_plot_points_3

    live_plot_points_4 = "ThisIsNotALivePointsObject"
    assert live_plot_points_1 != live_plot_points_4


def test_live_plot_points_raises_value_error_for_mixed_array_like_with_number_like_input():
    with pytest.raises(ValueError) as e_info:
        _ = LivePlotPoints(x=0, y=[0])

    assert e_info.value.args[0] == "Arguments provided must be of the same type: floats or lists"


@pytest.fixture(name="heatmap_plot_type")
def fixture_heatmap_plot_type() -> LivePlotType:
    return LivePlotType.HEATMAP


@pytest.fixture(name="heatmap_plot_axis")
def fixture_heatmap_plot_axis() -> LivePlotAxis:
    return LivePlotAxis(
        x_axis=[point["x"] for point in heatmap_unit_plot_points],
        y_axis=[point["y"] for point in heatmap_unit_plot_points],
    )


@pytest.fixture(name="heatmap_plot_points")
def fixture_heatmap_plot_points() -> LivePlotPoints:
    assert all(None not in point.values() for point in heatmap_unit_plot_points)
    x = [int(point["x"]) for point in heatmap_unit_plot_points]  # type: ignore
    y = [int(point["y"]) for point in heatmap_unit_plot_points]  # type: ignore
    z = [int(point["z"]) for point in heatmap_unit_plot_points]  # type: ignore
    idx = [int(point["idx"]) for point in heatmap_unit_plot_points]  # type: ignore
    idy = [int(point["idy"]) for point in heatmap_unit_plot_points]  # type: ignore

    return LivePlotPoints(x=x, y=y, z=z, idx=idx, idy=idy)


def test_heatmap_data_packet(
    heatmap_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    heatmap_plot_axis: LivePlotAxis,
    heatmap_plot_points: LivePlotPoints,
):
    plot_id = 1
    live_plot_packet = LivePlotPacket.build_packet(
        plot_id=plot_id,
        plot_type=heatmap_plot_type,
        labels=live_plot_labels,
        axis=heatmap_plot_axis,
        x=[point["x"] for point in heatmap_unit_plot_points],
        y=[point["y"] for point in heatmap_unit_plot_points],
        z=[point["z"] for point in heatmap_unit_plot_points],
    )

    assert live_plot_packet.plot_id == plot_id
    assert live_plot_packet.plot_type == heatmap_plot_type
    assert live_plot_packet.labels == live_plot_labels
    assert live_plot_packet.axis == heatmap_plot_axis
    assert live_plot_packet.data == heatmap_plot_points
    assert live_plot_packet == LivePlotPacket(
        plot_id=plot_id,
        plot_type=heatmap_plot_type,
        labels=live_plot_labels,
        axis=heatmap_plot_axis,
        data=heatmap_plot_points,
    )
    assert live_plot_packet.to_json() == json.dumps(
        {
            "plot_id": plot_id,
            "plot_type": heatmap_plot_type.value,
            "labels": asdict(live_plot_labels),
            "data": heatmap_plot_points.to_scatter(),
        }
    )


def test_heatmap_data_packet_with_numpy_arrays(
    heatmap_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    heatmap_plot_axis: LivePlotAxis,
    heatmap_plot_points: LivePlotPoints,
):
    plot_id = 1
    live_plot_packet = LivePlotPacket.build_packet(
        plot_id=plot_id,
        plot_type=heatmap_plot_type,
        labels=live_plot_labels,
        axis=heatmap_plot_axis,
        x=np.array([point["x"] for point in heatmap_unit_plot_points]),
        y=np.array([point["y"] for point in heatmap_unit_plot_points]),
        z=np.array([point["z"] for point in heatmap_unit_plot_points]),
    )

    assert live_plot_packet.to_json() == json.dumps(
        {
            "plot_id": plot_id,
            "plot_type": heatmap_plot_type.value,
            "labels": asdict(live_plot_labels),
            "data": heatmap_plot_points.to_scatter(),
        }
    )


def test_heatmap_data_packet_parsing_with_point_single_values(
    heatmap_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    heatmap_plot_axis: LivePlotAxis,
    heatmap_plot_points: LivePlotPoints,
):
    plot_id = 1
    live_plot_packets = [
        LivePlotPacket.build_packet(
            plot_id=plot_id,
            plot_type=heatmap_plot_type,
            labels=live_plot_labels,
            axis=heatmap_plot_axis,
            x=point["x"],
            y=point["y"],
            z=point["z"],
        )
        for point in heatmap_unit_plot_points
    ]

    for index, live_plot_packet in enumerate(live_plot_packets):
        assert live_plot_packet.to_json() == json.dumps(
            {
                "plot_id": plot_id,
                "plot_type": heatmap_plot_type.value,
                "labels": asdict(live_plot_labels),
                "data": LivePlotPoints(
                    x=heatmap_plot_points.x[index],
                    y=heatmap_plot_points.y[index],
                    z=heatmap_plot_points.z[index],
                    idx=heatmap_plot_points._idx[index],  # type: ignore
                    idy=heatmap_plot_points._idy[index],  # type: ignore
                ).to_scatter(),
            }
        )


def test_plotting_response_constructor():
    plotting_response = PlottingResponse(websocket_url="server/demo-url", plot_id=1)

    assert isinstance(plotting_response, PlottingResponse)
    assert plotting_response.plot_id == 1
    assert plotting_response.websocket_url == "server/demo-url"


def test_plotting_response_from_response():
    plotting_response_input = {"websocket_url": "server/demo-url", "plot_id": "1"}
    plotting_response = PlottingResponse.from_response(**plotting_response_input)

    assert isinstance(plotting_response, PlottingResponse)
    assert plotting_response.plot_id == int(plotting_response_input["plot_id"])
    assert plotting_response.websocket_url == str(plotting_response_input["websocket_url"])


def test_plotting_response_to_dict():
    plotting_response_dict = PlottingResponse(websocket_url="server/demo-url", plot_id=1).to_dict()

    assert isinstance(plotting_response_dict, dict)
    assert plotting_response_dict["plot_id"] == 1
    assert plotting_response_dict["websocket_url"] == "server/demo-url"


@patch("websockets.connect", autospec=True)
def test_start_up(
    mocked_websockets_connect: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests start-up method for the initialisation of a LivePlot"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_future = loop.create_future()
    mocked_connection_future.set_result(MagicMock())
    mocked_websockets_connect.return_value = mocked_connection_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot.start_up())

    mocked_websockets_connect.assert_called_with(websocket_url)
    assert isinstance(live_plot._send_queue_thread, threading.Thread)
    assert isinstance(live_plot._send_queue, Queue)


@patch("websockets.connect", autospec=True)
def test_open_connection_with_failing_connection(
    mocked_websockets_connect: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Test _open_connection and _close_connection work as intended"""

    mocked_connection_connect_return = MagicMock(side_effect=Exception("Test exception"))
    mocked_websockets_connect.return_value = mocked_connection_connect_return

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    with pytest.raises(ValueError):
        asyncio.run(live_plot._open_connection())
    assert live_plot._connection is None
    assert live_plot._connection_started_at is None


@patch("websockets.connect", autospec=True)
def test_open_and_close_connection(
    mocked_websockets_connect: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Test _open_connection and _close_connection work as intended"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_close = MagicMock()

    mocked_connection_close_future = loop.create_future()
    mocked_connection_close_future.set_result(mocked_connection_close)

    mocked_connection = MagicMock()
    mocked_connection.open = True
    mocked_connection.close.return_value = mocked_connection_close_future

    mocked_connection_connect_future = loop.create_future()
    mocked_connection_connect_future.set_result(mocked_connection)

    mocked_websockets_connect.return_value = mocked_connection_connect_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot._open_connection())
    mocked_websockets_connect.assert_called_with("test_url")
    assert live_plot._connection is not None
    assert isinstance(live_plot._connection_started_at, datetime.datetime)

    asyncio.run(live_plot._close_connection())
    mocked_connection.close.assert_called()
    assert live_plot._connection is None
    assert live_plot._connection_started_at is None


@patch("qiboconnection.live_plot.LivePlot._open_connection", autospec=True)
@patch("qiboconnection.live_plot.LivePlot._close_connection", autospec=True)
def test_reset_connection(
    mocked_open_connection: MagicMock,
    mocked_close_connection: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests _reset_connection method closes and opens a connection"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_open_connection_return = MagicMock()
    mocked_open_connection_future = loop.create_future()
    mocked_open_connection_future.set_result(mocked_open_connection_return)
    mocked_open_connection.return_value = mocked_open_connection_future

    mocked_close_connection_return = MagicMock()
    mocked_close_connection_future = loop.create_future()
    mocked_close_connection_future.set_result(mocked_close_connection_return)
    mocked_close_connection.return_value = mocked_close_connection_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot._reset_connection())
    mocked_close_connection.assert_called()
    mocked_open_connection.assert_called()


@patch("qiboconnection.live_plot.LivePlot._close_connection")
@patch("websockets.connect", autospec=True)
def test_send_data(
    mocked_websockets_connect: MagicMock,
    _mocked_close_connection: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests start-up method for the initialisation of a LivePlot"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_send_future = loop.create_future()
    mocked_connection_send_future.set_result("OK")

    mocked_connection = MagicMock()
    mocked_connection.open = True
    mocked_connection.send.return_value = mocked_connection_send_future

    mocked_connection_connect_future = loop.create_future()
    mocked_connection_connect_future.set_result(mocked_connection)

    mocked_websockets_connect.return_value = mocked_connection_connect_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot.start_up())

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.LINES,
        x=1,
        y=2,
        z=None,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    live_plot._connection_started_at = datetime.datetime.now()
    asyncio.run(live_plot.send_data(data=data_packet))

    time.sleep(1)
    mocked_connection.send.assert_called_with(data_packet.to_json())


@patch("qiboconnection.live_plot.LivePlot._reset_connection", autospec=True)
@patch("websockets.connect", autospec=True)
def test_send_data_with_too_log_lived_connection(
    mocked_websockets_connect: MagicMock,
    mocked_reset_connection: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests start-up method for the initialisation of a LivePlot"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_send_future = loop.create_future()
    mocked_connection_send_future.set_result("OK")
    mocked_connection_close_future = loop.create_future()
    mocked_connection_close_future.set_result("OK")
    mocked_connection = MagicMock()
    mocked_connection.open = True
    mocked_connection.send.return_value = mocked_connection_send_future
    mocked_connection.close.return_value = mocked_connection_close_future

    mocked_connection_connect_future = loop.create_future()
    mocked_connection_connect_future.set_result(mocked_connection)
    mocked_websockets_connect.return_value = mocked_connection_connect_future

    mocked_reset_connection_return = MagicMock()
    mocked_reset_connection_future = loop.create_future()
    mocked_reset_connection_future.set_result(mocked_reset_connection_return)
    mocked_reset_connection.return_value = mocked_reset_connection_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot.start_up())

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.LINES,
        x=1,
        y=2,
        z=None,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    live_plot._connection_started_at = datetime.datetime.now() - datetime.timedelta(
        seconds=WEBSOCKET_CONNECTION_LIFETIME + 1
    )
    asyncio.run(live_plot.send_data(data=data_packet))

    time.sleep(1)
    mocked_reset_connection.assert_called()
    mocked_connection.send.assert_called_with(data_packet.to_json())


@patch("qiboconnection.live_plot.LivePlot._reset_connection", autospec=True)
@patch("websockets.connect", autospec=True)
def test_send_data_with_closed_connection(
    mocked_websockets_connect: MagicMock,
    mocked_reset_connection: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests start-up method for the initialisation of a LivePlot"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_send_future = loop.create_future()
    mocked_connection_send_future.set_result("OK")
    mocked_connection = MagicMock()
    mocked_connection.open = False
    mocked_connection.send.return_value = mocked_connection_send_future

    mocked_connection_connect_future = loop.create_future()
    mocked_connection_connect_future.set_result(mocked_connection)
    mocked_websockets_connect.return_value = mocked_connection_connect_future

    mocked_reset_connection_return = MagicMock()
    mocked_reset_connection_future = loop.create_future()
    mocked_reset_connection_future.set_result(mocked_reset_connection_return)
    mocked_reset_connection.return_value = mocked_reset_connection_future

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    asyncio.run(live_plot.start_up())

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.LINES,
        x=1,
        y=2,
        z=None,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    live_plot._connection_started_at = datetime.datetime.now()
    asyncio.run(live_plot.send_data(data=data_packet))

    time.sleep(1)
    mocked_reset_connection.assert_called()


@patch("qiboconnection.live_plot.LivePlot._setup_queue", autospec=True)
@patch("websockets.connect", autospec=True)
def test_send_data_with_missbehaving_queue(
    mocked_websockets_connect: MagicMock,
    mocked_setup_queue: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests start-up method for the initialisation of a LivePlot"""

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    mocked_connection_send_future = loop.create_future()
    mocked_connection_send_future.set_result("OK")
    mocked_connection = MagicMock()
    mocked_connection.open = False
    mocked_connection.send.return_value = mocked_connection_send_future

    mocked_connection_connect_future = loop.create_future()
    mocked_connection_connect_future.set_result(mocked_connection)
    mocked_websockets_connect.return_value = mocked_connection_connect_future

    mocked_setup_queue.return_value = None

    plot_id = 1
    websocket_url = "test_url"
    live_plot = LivePlot(
        plot_id=plot_id,
        plot_type=live_plot_type,
        websocket_url=websocket_url,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.LINES,
        x=1,
        y=2,
        z=None,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    live_plot._connection_started_at = datetime.datetime.now()
    with pytest.raises(ValueError):
        asyncio.run(live_plot.send_data(data=data_packet))
