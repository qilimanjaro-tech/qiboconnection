""" Tests methods for live_plot """


import json
from dataclasses import asdict
from typing import cast

import pytest
import websocket

from qiboconnection.live_plot import LivePlot
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotPacket,
    LivePlotPoints,
    LivePlotType,
    PlottingResponse,
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


def test_live_plot_points(live_plot_points: LivePlotPoints):

    assert live_plot_points.x == unit_plot_point[0]["x"]
    assert live_plot_points.y == unit_plot_point[0]["y"]
    assert live_plot_points.to_scatter() == [unit_plot_point[0]]


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
    assert all([None not in point.values() for point in heatmap_unit_plot_points])
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
