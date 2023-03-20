"""API testing"""
import asyncio
from dataclasses import asdict
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from qiboconnection.api import API
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.util import create_device
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.runcard import Runcard
from qiboconnection.saved_experiment import SavedExperiment
from qiboconnection.saved_experiment_listing import SavedExperimentListing
from qiboconnection.typings.live_plot import PlottingResponse

from .data import experiment_dict, results_dict, runcard_dict, web_responses
from .utils import get_current_event_loop_or_create


def test_api_constructor(mocked_api: API):
    """Test API class constructor"""
    assert isinstance(mocked_api, API)


def test_jobs(mocked_api: API):
    """Test jobs property"""
    assert mocked_api.jobs == []


def test_last_job(mocked_api: API):
    """Test last_job property"""
    with pytest.raises(IndexError):
        _ = mocked_api.last_job


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_last_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Test last_saved_experiment property"""
    mocked_web_call.return_value = web_responses.saved_experiments.create_response

    assert mocked_api.last_saved_experiment is None
    name = "MyDemoExperiment"
    description = "A test saved experiment"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    favourite = True
    _ = mocked_api.save_experiment(
        name=name,
        description=description,
        experiment_dict=experiment_dict,
        results_dict=results_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
        favourite=favourite,
    )
    assert isinstance(mocked_api.last_saved_experiment, SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_last_saved_experiment_listing(mocked_web_call: MagicMock, mocked_api: API):
    """Test last_saved_experiment_listing property"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_listing_response

    assert mocked_api.last_saved_experiment_listing is None
    saved_experiments_list = mocked_api.list_saved_experiments()
    assert isinstance(mocked_api.last_saved_experiment_listing, SavedExperimentListing)
    assert mocked_api.last_saved_experiment_listing == saved_experiments_list


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_last_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Test last_runcard property"""
    mocked_web_call.return_value = web_responses.runcards.create_response

    assert mocked_api.last_runcard is None
    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    _ = mocked_api.save_runcard(
        name=name,
        description=description,
        runcard_dict=runcard_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )
    assert isinstance(mocked_api.last_runcard, Runcard)


def test_user_id(mocked_api: API):
    """Test last_runcard property"""
    assert mocked_api.user_id == 666


@patch("qiboconnection.connection.Connection.send_get_remote_call", autospec=True)
def test_ping(mocked_web_call: MagicMock, mocked_api: API):
    """Test ping function"""
    mocked_web_call.return_value = web_responses.ping.success_response

    mocked_api.ping()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_remote_call", autospec=True)
def test_ping_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test ping function with failing"""
    mocked_web_call.return_value = web_responses.ping.ise_response

    with pytest.raises(ConnectionException):
        mocked_api.ping()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_many_response

    device_listing = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.DEVICES_CALL_PATH)
    assert isinstance(device_listing, Devices)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_many_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.DEVICES_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_id(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_response

    mocked_api.select_device_id(device_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(web_responses.devices.retrieve_response[0])


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_id_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.select_device_id(device_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices == []


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_ids(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_response

    mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(web_responses.devices.retrieve_response[0])


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_ids_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices == []


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
    """Tests API.save_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.create_response

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
    assert saved_experiment_id == web_responses.saved_experiments.create_response[0]["saved_experiment_id"]


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.save_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    name = "MyDemoExperiment"
    description = "A test saved experiment"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    favourite = True
    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.save_experiment(
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


@pytest.mark.parametrize("favourites", [False, True])
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_saved_experiments(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_listing_response

    saved_experiments_list = mocked_api.list_saved_experiments(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api.SAVED_EXPERIMENTS_CALL_PATH, params={"favourites": favourites}
    )
    assert isinstance(saved_experiments_list, SavedExperimentListing)
    assert isinstance(saved_experiments_list.dataframe, pd.DataFrame)


@pytest.mark.parametrize("favourites", [False, True])
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_saved_experiments_ise(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_listing_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.list_saved_experiments(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api.SAVED_EXPERIMENTS_CALL_PATH, params={"favourites": favourites}
    )


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api.get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment, SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api.get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment[0], SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiment() with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiment() with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiment() method with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiment() method with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.save_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.create_response

    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"

    runcard_id = mocked_api.save_runcard(
        name=name,
        description=description,
        runcard_dict=runcard_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    mocked_web_call.assert_called()
    assert runcard_id == web_responses.runcards.create_response[0]["runcard_id"]


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_runcard_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.save_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.save_runcard(
            name=name,
            description=description,
            runcard_dict=runcard_dict,
            device_id=device_id,
            user_id=user_id,
            qililab_version=qililab_version,
        )

    mocked_web_call.assert_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method using runcard id"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    runcard = mocked_api.get_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")
    assert isinstance(runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard_by_name(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method using runcard name"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    runcard = mocked_api.get_runcard(runcard_name="DEMO_RUNCARD")

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/by_keys", params={"name": "DEMO_RUNCARD"}
    )
    assert isinstance(runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard_with_redundant_info(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method fails when providing name and id at the same time"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    with pytest.raises(ValueError):
        _ = mocked_api.get_runcard(runcard_id=1, runcard_name="TEST_RUNCARD")

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard_with_insufficient_info(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method fails if not name nor id are provided"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    with pytest.raises(ValueError):
        _ = mocked_api.get_runcard()

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method when server response raises an error"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.get_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_runcards(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_many_response

    runcards = mocked_api.list_runcards()

    mocked_web_call.assert_called()
    assert isinstance(runcards[0], Runcard)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_runcards_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.ise_many_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.list_runcards()

    mocked_web_call.assert_called()


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_update_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.update_response

    runcard_id = 1
    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_runcard = Runcard(
        id=runcard_id,
        name=name,
        description=description,
        runcard=runcard_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    updated_runcard = mocked_api.update_runcard(runcard=modified_runcard)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.RUNCARDS_CALL_PATH}/1",
        data=asdict(modified_runcard.runcard_request()),
    )
    assert isinstance(updated_runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_update_runcard_with_no_id(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.update_response

    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_runcard = Runcard(
        id=None,
        name=name,
        description=description,
        runcard=runcard_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    with pytest.raises(ValueError):
        _ = mocked_api.update_runcard(runcard=modified_runcard)

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_update_runcard_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    runcard_id = 1
    name = "MyDemoRuncard"
    description = "A test runcard"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_runcard = Runcard(
        id=runcard_id,
        name=name,
        description=description,
        runcard=runcard_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.update_runcard(runcard=modified_runcard)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.RUNCARDS_CALL_PATH}/1",
        data=asdict(modified_runcard.runcard_request()),
    )


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.delete_response

    mocked_api.delete_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_runcard_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.delete_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")
