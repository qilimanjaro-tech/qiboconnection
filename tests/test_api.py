"""API testing"""
from dataclasses import asdict
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from qiboconnection.api import API
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.util import create_device
from qiboconnection.runcard import Runcard
from qiboconnection.saved_experiment import SavedExperiment
from qiboconnection.saved_experiment_listing import SavedExperimentListing

from .data import experiment_dict, results_dict, runcard_dict, web_responses


def test_api_constructor(mocked_api: API):
    """Test API class constructor"""
    assert isinstance(mocked_api, API)


@patch("qiboconnection.connection.Connection.send_get_remote_call", autospec=True)
def test_ping(mocked_web_call: MagicMock, mocked_api: API):
    """Test ping function"""
    mocked_web_call.return_value = web_responses.ping.success_response

    mocked_api.ping()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.PING_CALL_PATH)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_devices(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_many_response

    device_listing = mocked_api.list_devices()

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=mocked_api.DEVICES_CALL_PATH)
    assert isinstance(device_listing, Devices)


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
def test_select_device_ids(mocked_web_call: MagicMock, mocked_api: API):
    """Test list devices function"""
    mocked_web_call.return_value = web_responses.devices.retrieve_response

    mocked_api.select_device_ids(device_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.DEVICES_CALL_PATH}/1")
    assert mocked_api._selected_devices is not None
    assert len(mocked_api._selected_devices) == 1
    assert mocked_api._selected_devices[0] == create_device(web_responses.devices.retrieve_response[0])


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
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


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api.get_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment, SavedExperiment)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.retrieve_response

    saved_experiment = mocked_api.get_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1")
    assert isinstance(saved_experiment[0], SavedExperiment)


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.fav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_fav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.fav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": True, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiment(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.unfav_saved_experiment(saved_experiment_id=1)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_unfav_saved_experiments(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
    mocked_web_call.return_value = web_responses.saved_experiments.update_response

    mocked_api.unfav_saved_experiments(saved_experiment_ids=[1])

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api.SAVED_EXPERIMENTS_CALL_PATH}/1",
        data={"favourite": False, "user_id": mocked_api.user_id},
    )


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_saved_experiments() method"""
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


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_response

    runcard = mocked_api.get_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")
    assert isinstance(runcard, Runcard)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_runcards(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.retrieve_many_response

    runcards = mocked_api.list_runcards()

    mocked_web_call.assert_called()
    assert isinstance(runcards[0], Runcard)


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_update_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method"""
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


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_runcard(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method"""
    mocked_web_call.return_value = web_responses.runcards.delete_response

    mocked_api.delete_runcard(runcard_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api.RUNCARDS_CALL_PATH}/1")
