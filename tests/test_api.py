import asyncio
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from qiboconnection.api import API
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.util import create_device
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.saved_experiment import SavedExperiment
from qiboconnection.saved_experiment_listing import SavedExperimentListing
from qiboconnection.typings.live_plot import PlottingResponse

from .data import WebResponses, experiment_dict, results_dict
from .utils import get_current_event_loop_or_create


def test_api_constructor(mocked_api: API):
    """Test API class constructor"""
    assert isinstance(mocked_api, API)


@patch("qiboconnection.connection.Connection.send_get_remote_call", autospec=True)
def test_ping(mocked_web_call: MagicMock, mocked_api: API):
    """Test ping function"""
    mocked_web_call.return_value = WebResponses.ping_rest_response

    mocked_api.ping()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = WebResponses.list_devices_response

    device_listing = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.DEVICES_CALL_PATH)
    assert isinstance(device_listing, Devices)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_id(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = WebResponses.get_device_response

    mocked_api.select_device_id(device_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(WebResponses.get_device_response[0])


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_ids(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = WebResponses.get_device_response

    mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(WebResponses.get_device_response[0])


@patch("websockets.connect", autospec=True)
@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_create_live_plot(mocked_web_call: MagicMock, mocked_websockets_connect: MagicMock, mocked_api: API):
    """Test the creation of a liveplot using the api"""

    loop = get_current_event_loop_or_create()
    mocked_connection_future = loop.create_future()
    mocked_connection_future.set_result(MagicMock())
    mocked_websockets_connect.return_value = mocked_connection_future

    mocked_web_call.return_value = PlottingResponse(websocket_url="test_url", plot_id=1).to_dict(), 200

    plot_id = asyncio.run(mocked_api.create_liveplot())

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.LIVE_PLOTTING_PATH, data={})
    mocked_websockets_connect.assert_called_with("test_url")
    assert plot_id == 1


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_create_live_plot_with_unexpected_response(mocked_web_call: MagicMock, mocked_api: API):
    """Test the creation of a liveplot using the api"""

    mocked_web_call.return_value = {}, 400

    with pytest.raises(RemoteExecutionException):
        _ = asyncio.run(mocked_api.create_liveplot())


@patch("qiboconnection.live_plot.LivePlot.send_data", autospec=True)
@patch("websockets.connect", autospec=True)
@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_send_plot_points(
    mocked_web_call: MagicMock,
    mocked_websockets_connect: MagicMock,
    mocked_live_plot_send_data: MagicMock,
    mocked_api: API,
):
    """Test the creation of a liveplot using the api"""

    loop = get_current_event_loop_or_create()
    mocked_connection_future = loop.create_future()
    mocked_connection_future.set_result(MagicMock())
    mocked_websockets_connect.return_value = mocked_connection_future

    mocked_web_call.return_value = PlottingResponse(websocket_url="test_url", plot_id=1).to_dict(), 200

    plot_id = asyncio.run(mocked_api.create_liveplot())

    asyncio.run(mocked_api.send_plot_points(plot_id=plot_id, x=0, y=0))

    mocked_live_plot_send_data.assert_called()


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.save_experiment_rest_response

    name = "MyDemoExperiment"
    description = "A test saved experiment"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    favourite = True

    saved_experiment_id = mocked_api.save_experiment(
        name=name,
        description=description,
        experiment_dict=experiment_dict,
        results_dict=results_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
        favourite=favourite,
    )

    mocked_web_call.assert_called()
    assert saved_experiment_id == WebResponses.save_experiment_rest_response[0]["saved_experiment_id"]


@pytest.mark.parametrize("favourites", [False, True])
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_saved_experiments(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiments_listing_rest_response

    saved_experiments_list = mocked_api.list_saved_experiments(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api.SAVED_EXPERIMENTS_CALL_PATH, params={"favourites": favourites}
    )
    assert isinstance(saved_experiments_list, SavedExperimentListing)
    assert isinstance(saved_experiments_list.dataframe, pd.DataFrame)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    saved_experiment = mocked_api.get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment, SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    saved_experiment = mocked_api.get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment[0], SavedExperiment)


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    mocked_api.fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    mocked_api.fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    mocked_api.unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = WebResponses.saved_experiment_rest_response

    mocked_api.unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )
