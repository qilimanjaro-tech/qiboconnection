""" Tests methods for LivePlots """

import asyncio
from unittest.mock import MagicMock, patch

import pytest
import websockets

from qiboconnection.live_plot import LivePlot
from qiboconnection.live_plots import LivePlots
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotType,
)

from .utils import get_current_event_loop_or_create


def ok_method(*args, **kwargs):
    """returns `'ok'`"""
    return "OK"


@pytest.fixture(name="live_plot_type")
def fixture_plot_type():
    """return lines type"""
    return LivePlotType.LINES


@pytest.fixture(name="live_plot_labels")
def fixture_plot_labels():
    """return valid labels instance"""
    return LivePlotLabels()


@pytest.fixture(name="live_plot_axis")
def fixture_plot_axis():
    """return valid axis instance"""
    return LivePlotAxis()


def test_live_plots_constructor():
    """test live plot creation"""
    live_plots = LivePlots()
    assert isinstance(live_plots, LivePlots)


@patch("websockets.connect", autospec=True)
def test_live_plots_add_plot(
    mocked_websockets_connect: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """test live plot `create_live_plot`"""
    """Tests LivePlots add plot functionality"""

    loop = get_current_event_loop_or_create()

    mocked_connection_future = loop.create_future()
    mocked_connection_future.set_result(MagicMock())
    mocked_websockets_connect.return_value = mocked_connection_future

    live_plots = LivePlots()
    expected_live_plot = LivePlot(
        plot_id=1,
        plot_type=live_plot_type,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    asyncio.run(expected_live_plot.start_up())

    asyncio.run(
        live_plots.create_live_plot(
            plot_id=1,
            plot_type=live_plot_type,
            websocket_url="server/demo-url",
            labels=live_plot_labels,
            axis=live_plot_axis,
        )
    )
    created_live_plot = live_plots._get_live_plot(plot_id=1)

    mocked_websockets_connect.assert_called_with("server/demo-url")
    assert expected_live_plot == created_live_plot


@patch("qiboconnection.live_plot.LivePlot.send_data", autospec=True)
@patch("qiboconnection.live_plot.websockets.connect", autospec=True)
def test_live_plots_send_data(
    mocked_websockets_connect: MagicMock,
    live_plot_send_data: MagicMock,
    live_plot_type: LivePlotType,
    live_plot_labels: LivePlotLabels,
    live_plot_axis: LivePlotAxis,
):
    """Tests the LivePlots send_data functionality, mocking the inferior LivePlot layer."""

    loop = get_current_event_loop_or_create()

    mocked_connection_future = loop.create_future()
    mocked_connection_future.set_result(MagicMock())
    mocked_websockets_connect.return_value = mocked_connection_future

    live_plots = LivePlots()
    asyncio.run(
        live_plots.create_live_plot(
            plot_id=1,
            plot_type=live_plot_type,
            websocket_url="server/demo-url",
            labels=live_plot_labels,
            axis=live_plot_axis,
        )
    )

    asyncio.run(live_plots.send_data(plot_id=1, x=1, y=1, z=None))

    expected_sent_data_packet = LivePlotPacket.build_packet(
        plot_id=1, plot_type=live_plot_type, x=1, y=1, z=None, labels=live_plot_labels, axis=live_plot_axis
    )

    live_plot_send_data.assert_called_with(self=live_plots._get_live_plot(plot_id=1), data=expected_sent_data_packet)


def test_check_data_and_plot_type_compatibility_with_ok_case(
    live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works with base case"""
    live_plot = LivePlot(
        plot_id=1,
        plot_type=live_plot_type,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=live_plot_type,
        x=1,
        y=2,
        z=None,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    test_result = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
        live_plot=live_plot, data_packet=data_packet
    )

    assert test_result == "OK"


def test_check_data_and_plot_type_compatibility_rises_attribute_error(
    live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works as expected in wrong attr err case"""

    with pytest.raises(AttributeError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(live_plot=None, data_packet=None)

    assert e_info.value.args[0] == "live_plot and point info are required."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_lines(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works as expected in wrong val err case"""
    live_plot = LivePlot(
        plot_id=1,
        plot_type=LivePlotType.LINES,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.SCATTER3D,
        x=1,
        y=2,
        z=3,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "LINES and SCATTER plots accept exactly x and y values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_scatter3d(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works as expected in wrong val err case"""
    live_plot = LivePlot(
        plot_id=1,
        plot_type=LivePlotType.SCATTER3D,
        websocket_url="server/demo-url",
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

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "SCATTER3D plots accept exactly x, y and z values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_heatmap(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works as expected in wrong val err case"""
    live_plot = LivePlot(
        plot_id=1,
        plot_type=LivePlotType.HEATMAP,
        websocket_url="server/demo-url",
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

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "HEATMAP plots accept exactly x, y and z values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_heatmap_axis(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    """test live plot `CheckDataAndPlotTypeCompatibility` works as expected in wrong val err case"""
    live_plot = LivePlot(
        plot_id=1,
        plot_type=LivePlotType.HEATMAP,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    data_packet = LivePlotPacket.build_packet(
        plot_id=1,
        plot_type=LivePlotType.SCATTER3D,
        x=1,
        y=2,
        z=3,
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "HEATMAP plots need to have axis provided on live-plot creation."
