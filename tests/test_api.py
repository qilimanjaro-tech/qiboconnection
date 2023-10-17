"""API testing"""
import ast
import asyncio
import base64
import json
from dataclasses import asdict
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import responses  # pylint: disable=import-error
from qibo import gates
from qibo.models import Circuit

from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.models.devices.devices import Devices
from qiboconnection.models.devices.util import create_device
from qiboconnection.models.job_listing import JobListing
from qiboconnection.models.runcard import Runcard
from qiboconnection.models.saved_experiment import SavedExperiment
from qiboconnection.models.saved_experiment_listing import SavedExperimentListing
from qiboconnection.typings.job_data import JobData
from qiboconnection.typings.responses import PlottingResponse
from tests.data.web_responses.job import JobResponse

from .data import experiment_dict, results_dict, runcard_dict, web_responses
from .utils import get_current_event_loop_or_create


def test_api_constructor(mocked_api: API):
    """Test API class constructor"""
    assert isinstance(mocked_api, API)


@patch("qiboconnection.api.API.__init__", autospec=True)
def test_api_login(mocked_api_init: MagicMock):
    """Tests user utility constructor Login calls __init__ with the correct information,"""
    mocked_api_init.return_value = None
    _USERNAME = "test-name"
    _API_KEY = "test-key"

    _ = API.login(username=_USERNAME, api_key=_API_KEY)

    provided_user_info = mocked_api_init.call_args_list[0][1]["configuration"]
    assert isinstance(provided_user_info, ConnectionConfiguration)
    assert provided_user_info.username == _USERNAME
    assert provided_user_info.api_key == _API_KEY


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

    assert mocked_api._last_saved_experiment is None
    name = "MyDemoExperiment"
    description = "A test saved experiment"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    favourite = True
    _ = mocked_api._save_experiment(
        name=name,
        description=description,
        experiment_dict=experiment_dict,
        results_dict=results_dict,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
        favourite=favourite,
    )
    assert isinstance(mocked_api._last_saved_experiment, SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_last_saved_experiment_listing(mocked_web_call: MagicMock, mocked_api: API):
    """Test last_saved_experiment_listing property"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_listing_response

    assert mocked_api._last_saved_experiment_listing is None
    saved_experiments_list = mocked_api._list_saved_experiments()
    assert isinstance(mocked_api._last_saved_experiment_listing, SavedExperimentListing)
    assert mocked_api._last_saved_experiment_listing == saved_experiments_list


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

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api._PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_remote_call", autospec=True)
def test_ping_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test ping function with failing"""
    mocked_web_call.return_value = web_responses.ping.ise_response

    with pytest.raises(ConnectionException):
        mocked_api.ping()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api._PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_many_response

    device_listing = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api._DEVICES_CALL_PATH)
    assert isinstance(device_listing, Devices)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_many_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api._DEVICES_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_id(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_response

    mocked_api.select_device_id(device_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(web_responses.devices.retrieve_response[0])


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_id_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.select_device_id(device_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices == []


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_ids(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_response

    mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(web_responses.devices.retrieve_response[0])


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_select_device_ids_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._DEVICES_CALL_PATH}/1")
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

    plot_id = asyncio.run(mocked_api._create_liveplot())

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api._LIVE_PLOTTING_PATH, data={})
    mocked_websockets_connect.assert_called_with("test_url")
    assert plot_id == 1


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_create_live_plot_with_unexpected_response(mocked_web_call: MagicMock, mocked_api: API):
    """Test the creation of a liveplot using the api"""

    mocked_web_call.return_value = {}, 400

    with pytest.raises(RemoteExecutionException):
        _ = asyncio.run(mocked_api._create_liveplot())


@patch("qiboconnection.models.live_plot.LivePlot.send_data", autospec=True)
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

    plot_id = asyncio.run(mocked_api._create_liveplot())

    asyncio.run(mocked_api._send_plot_points(plot_id=plot_id, x=0, y=0))

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

    saved_experiment_id = mocked_api._save_experiment(
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
        _ = mocked_api._save_experiment(
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
def test_list_jobs(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_jobs() method"""
    mocked_web_call.return_value = web_responses.job_response.retrieve_job_listing_response

    jobs_list = mocked_api.list_jobs(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api._JOBS_CALL_PATH, params={"favourites": favourites}
    )
    assert isinstance(jobs_list, JobListing)
    assert isinstance(jobs_list.dataframe, pd.DataFrame)


@pytest.mark.parametrize("favourites", [False, True])
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_saved_experiments(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_listing_response

    saved_experiments_list = mocked_api._list_saved_experiments(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api._SAVED_EXPERIMENTS_CALL_PATH, params={"favourites": favourites}
    )
    assert isinstance(saved_experiments_list, SavedExperimentListing)
    assert isinstance(saved_experiments_list.dataframe, pd.DataFrame)


@pytest.mark.parametrize("favourites", [False, True])
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_saved_experiments_ise(mocked_web_call: MagicMock, favourites: bool, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_listing_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api._list_saved_experiments(favourites=favourites)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=mocked_api._SAVED_EXPERIMENTS_CALL_PATH, params={"favourites": favourites}
    )


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api._get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment, SavedExperiment)


@pytest.mark.parametrize(
    "web_job_response",
    [JobResponse.retrieve_job_response_1, JobResponse.retrieve_job_response_2, JobResponse.retrieve_job_response_3],
)
@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_job(mocked_web_call: MagicMock, mocked_api: API, web_job_response: dict):
    """Tests API.get_job() method."""
    mocked_web_call.return_value = web_job_response

    job_data = mocked_api.get_job(job_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/1")
    assert isinstance(job_data, JobData)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_job_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.get_result() method with non-existent job id"""

    # Define the behavior of the mocked function to raise the RemoteExecutionException
    mocked_api_call.side_effect = RemoteExecutionException("The job does not exist!", status_code=400)

    with pytest.raises(RemoteExecutionException, match="The job does not exist!"):
        # Call the function that should raise the exception
        mocked_api.get_result(job_id=0)

    # Assert that the mocked function was called with correct arguments
    mocked_api_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/{0}")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiment() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api._get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api._get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment[0], SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api._get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiment() with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api._fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiment() with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api._fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api._fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.fav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api._fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiment() method with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api._unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiment() method with ONE experiment"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api._unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api._unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.unfav_saved_experiments() method with a LIST of experiments"""
    mocked_web_call.return_value = web_responses.saved_experiments.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api._unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._SAVED_EXPERIMENTS_CALL_PATH}/1",
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

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._RUNCARDS_CALL_PATH}/1")
    assert isinstance(runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard_by_name(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method using runcard name"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    runcard = mocked_api.get_runcard(runcard_name="DEMO_RUNCARD")

    mocked_web_call.assert_called_with(
        self=mocked_api._connection, path=f"{mocked_api._RUNCARDS_CALL_PATH}/by_keys", params={"name": "DEMO_RUNCARD"}
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

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._RUNCARDS_CALL_PATH}/1")


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


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
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
        path=f"{mocked_api._RUNCARDS_CALL_PATH}/1",
        data=asdict(modified_runcard.runcard_request()),
    )
    assert isinstance(updated_runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
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


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
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
        path=f"{mocked_api._RUNCARDS_CALL_PATH}/1",
        data=asdict(modified_runcard.runcard_request()),
    )


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.delete_response

    mocked_api.delete_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._RUNCARDS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_runcard_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.delete_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._RUNCARDS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_result_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.get_result() method with non-existent job id."""

    # Define the behavior of the mocked function to raise the RemoteExecutionException
    mocked_api_call.side_effect = RemoteExecutionException("The job does not exist!", status_code=400)

    with pytest.raises(RemoteExecutionException, match="The job does not exist!"):
        # Call the function that should raise the exception
        mocked_api.get_result(job_id=0)

    # Assert that the mocked function was called with correct arguments
    mocked_api_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/{0}")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_no_devices_selected_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.execute() method with no devices selected"""

    # Define the behavior of the mocked function to raise the ValueError
    mocked_api_call.side_effect = ValueError("No devices were selected for execution.")

    with pytest.raises(ValueError, match="No devices were selected for execution."):
        # Here, a circuit should be passed which will be ignored as the call is mocked
        mocked_api.execute(device_ids=None)

    # Check that the mocked function was not called
    mocked_api_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_job(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.delete_job() method"""
    mocked_api_call.return_value = web_responses.job_response.delete_job_response
    mocked_api.delete_job(job_id=0)

    mocked_api_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/{0}")


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_job_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.delete_job() method with non-existent job id"""
    # Define the behavior of the mocked function to raise the RemoteExecutionException
    mocked_api_call.return_value = web_responses.job_response.delete_job_response_ise
    with pytest.raises(RemoteExecutionException, match="Job could not be removed."):
        # Call the function that should raise the exception
        mocked_api.delete_job(job_id=0)
    # Assert that the mocked function was called with correct arguments
    mocked_api_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/{0}")


class TestExecute:
    """Unit tests for the `API.execute` method."""

    r_mock: responses.RequestsMock

    circuit = Circuit(5)
    circuit.add(gates.X(0))
    circuit.add(gates.H(4))
    circuit.add(gates.M(0, 1, 2, 3, 4))

    def setup_method(self):
        """Method executed before each test contained in this class.

        This method mocks the `requests` calls used inside the API.execute method.
        """
        self.r_mock = responses.RequestsMock(assert_all_requests_are_fired=True)
        self.r_mock.start()
        self.r_mock.add(
            method="GET",
            url="https://qilimanjaroqaas.ddns.net:8080/api/v1/devices/9",
            status=200,
            json={
                "status": "offline",
                "device_id": 9,
                "device_name": "Dummy Device",
                "availability": "available",
                "channel_id": 0,
            },
        )
        self.r_mock.add(
            method="POST", url="https://qilimanjaroqaas.ddns.net:8080/api/v1/circuits", status=201, json={"job_id": 0}
        )

    def teardown_method(self):
        """Method executed at the end of each test contained in this class.

        Stops and resets RequestsMock instance. If ``assert_all_requests_are_fired`` is set to ``True``, will raise an
        error if some requests were not processed.
        """
        self.r_mock.stop()
        self.r_mock.reset()

    def test_execute_with_one_circuit(self, mocked_api: API):
        """Test the API.execute method for a single circuit."""
        job_ids = mocked_api.execute(circuit=self.circuit, nshots=1000, device_ids=[9])

        assert job_ids == [0]
        assert len(self.r_mock.calls) == 2
        body = json.loads(self.r_mock.calls[1].request.body.decode())
        assert body["device_id"] == 9
        assert body["number_shots"] == 1000
        assert body["job_type"] == "circuit"
        description = ast.literal_eval(body["description"])
        assert len(description) == 1
        assert (
            base64.urlsafe_b64decode(description[0]).decode() == self.circuit.to_qasm()
        )  # make sure we posted the correct circuit

    def test_execute_with_multiple_circuits(self, mocked_api: API):
        """Test the API.execute method for multiple circuits."""
        job_ids = mocked_api.execute(circuit=[self.circuit] * 10, nshots=1000, device_ids=[9])

        assert job_ids == [0]
        assert len(self.r_mock.calls) == 2
        body = json.loads(self.r_mock.calls[1].request.body.decode())
        assert body["device_id"] == 9
        assert body["number_shots"] == 1000
        assert body["job_type"] == "circuit"
        description = ast.literal_eval(body["description"])
        assert len(description) == 10
        assert all(
            base64.urlsafe_b64decode(d).decode() == self.circuit.to_qasm() for d in description
        )  # make sure we posted the correct circuits
