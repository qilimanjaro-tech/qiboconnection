""" Tests methods for live_plot """

import json
from dataclasses import asdict
from typing import cast

import pytest
import websocket

from qiboconnection.live_plot import LivePlot
from qiboconnection.live_plots import LivePlots
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotPoints,
    LivePlotType,
)
from qiboconnection.user import User

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


def test_live_plots_constructor():
    live_plots = LivePlots()
    assert isinstance(live_plots, LivePlots)


def test_live_plots_add_plot(
    live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    live_plots = LivePlots()
    expected_live_plot = LivePlot(
        plot_id=1,
        plot_type=live_plot_type,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )
    live_plots.create_live_plot(
        plot_id=1,
        plot_type=live_plot_type,
        websocket_url="server/demo-url",
        labels=live_plot_labels,
        axis=live_plot_axis,
    )

    assert expected_live_plot.__dict__ == live_plots._get_live_plot(plot_id=1).__dict__


def test_check_data_and_plot_type_compatibility_with_ok_case(
    live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):

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

    def ok_method(*args, **kwargs):
        return "OK"

    test_result = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
        live_plot=live_plot, data_packet=data_packet
    )

    assert test_result == "OK"


def test_check_data_and_plot_type_compatibility_rises_attribute_error(
    live_plot_type: LivePlotType, live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):
    def ok_method(*args, **kwargs):
        return "OK"

    with pytest.raises(AttributeError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(live_plot=None, data_packet=None)

    assert e_info.value.args[0] == "live_plot and point info are required."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_lines(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):

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

    def ok_method(*args, **kwargs):
        return "OK"

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "LINES and SCATTER plots accept exactly x and y values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_scatter3d(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):

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

    def ok_method(*args, **kwargs):
        return "OK"

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "SCATTER3D plots accept exactly x, y and z values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_heatmap(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):

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

    def ok_method(*args, **kwargs):
        return "OK"

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "HEATMAP plots accept exactly x, y and z values."


def test_check_data_and_plot_type_compatibility_rises_value_error_for_heatmap_axis(
    live_plot_labels: LivePlotLabels, live_plot_axis: LivePlotAxis
):

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

    def ok_method(*args, **kwargs):
        return "OK"

    with pytest.raises(ValueError) as e_info:
        _ = LivePlots.CheckDataAndPlotTypeCompatibility(method=ok_method).__call__(
            live_plot=live_plot, data_packet=data_packet
        )

    assert e_info.value.args[0] == "HEATMAP plots need to have axis provided on live-plot creation."
