"""API testing"""
# pylint: disable=too-many-lines

import base64
import gzip
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
from qiboconnection.models.calibration import Calibration
from qiboconnection.models.devices.devices import Devices
from qiboconnection.models.devices.util import create_device
from qiboconnection.models.job_listing import JobListing
from qiboconnection.models.runcard import Runcard
from qiboconnection.typings.enums import JobStatus, JobType
from qiboconnection.typings.job_data import JobData
from qiboconnection.typings.vqa import VQA
from qiboconnection.util import compress_any

from .data import calibration_serialized, runcard_dict, web_responses
from .data.web_responses.job import JobResponse


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


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_last_calibration(mocked_web_call: MagicMock, mocked_api: API):
    """Test last_runcard property"""
    mocked_web_call.return_value = web_responses.calibrations.create_response

    assert mocked_api.last_calibration is None
    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    _ = mocked_api.save_calibration(
        name=name,
        description=description,
        calibration_serialized=calibration_serialized,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )
    assert isinstance(mocked_api.last_calibration, Calibration)


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
def test_get_runcard_by_name_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_runcard() method using runcard name"""
    mocked_web_call.return_value = web_responses.runcards.ise_response

    with pytest.raises(RemoteExecutionException, match="Runcard could not be retrieved."):
        _ = mocked_api.get_runcard(runcard_name="DEMO_RUNCARD")


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


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_results_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.get_results() method with non-existent job id."""

    # Define the behavior of the mocked function to raise the RemoteExecutionException
    mocked_api_call.side_effect = RemoteExecutionException("The job does not exist!", status_code=400)

    with pytest.raises(RemoteExecutionException, match="The job does not exist!"):
        # Call the function that should raise the exception
        mocked_api.get_results(job_ids=[0, -1])

    # Assert that the mocked function was called with correct arguments
    mocked_api_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/{0}")


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_calibration(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.save_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.create_response

    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"

    calibration_id = mocked_api.save_calibration(
        name=name,
        description=description,
        calibration_serialized=calibration_serialized,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    mocked_web_call.assert_called()
    assert calibration_id == web_responses.calibrations.create_response[0]["calibration_id"]


@patch("qiboconnection.connection.Connection.send_post_auth_remote_api_call", autospec=True)
def test_save_calibration_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.save_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.ise_response

    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.save_calibration(
            name=name,
            description=description,
            calibration_serialized=calibration_serialized,
            device_id=device_id,
            user_id=user_id,
            qililab_version=qililab_version,
        )

    mocked_web_call.assert_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method using calibration id"""
    mocked_web_call.return_value = web_responses.calibrations.retrieve_response

    calibration = mocked_api.get_calibration(calibration_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1")
    assert isinstance(calibration, Calibration)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration_by_name(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method using calibration name"""
    mocked_web_call.return_value = web_responses.calibrations.retrieve_response

    calibration = mocked_api.get_calibration(calibration_name="DEMO_CALIBRATION")

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/by_keys",
        params={"name": "DEMO_CALIBRATION"},
    )
    assert isinstance(calibration, Calibration)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration_by_name_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method using calibration name"""
    mocked_web_call.return_value = web_responses.calibrations.ise_response

    with pytest.raises(RemoteExecutionException, match="Calibration could not be retrieved."):
        _ = mocked_api.get_calibration(calibration_name="DEMO_CALIBRATION")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration_with_redundant_info(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method fails when providing name and id at the same time"""
    mocked_web_call.return_value = web_responses.calibrations.retrieve_response

    with pytest.raises(ValueError):
        _ = mocked_api.get_calibration(calibration_id=1, calibration_name="TEST_CALIBRATION")

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration_with_insufficient_info(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method fails if not name nor id are provided"""
    mocked_web_call.return_value = web_responses.calibrations.retrieve_response

    with pytest.raises(ValueError):
        _ = mocked_api.get_calibration()

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_get_calibration_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.get_calibration() method when server response raises an error"""
    mocked_web_call.return_value = web_responses.calibrations.ise_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.get_calibration(calibration_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_calibrations(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.retrieve_many_response

    calibrations = mocked_api.list_calibrations()

    mocked_web_call.assert_called()
    assert isinstance(calibrations[0], Calibration)


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call_all_pages", autospec=True)
def test_list_calibrations_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.list_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.ise_many_response

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.list_calibrations()

    mocked_web_call.assert_called()


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_update_calibration(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.update_response

    calibration_id = 1
    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_calibration = Calibration(
        id=calibration_id,
        name=name,
        description=description,
        calibration_serialized=calibration_serialized,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    updated_calibration = mocked_api.update_calibration(calibration=modified_calibration)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1",
        data=asdict(modified_calibration.calibration_request()),
    )
    assert isinstance(updated_calibration, Calibration)


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_update_calibration_with_no_id(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.update_response

    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_calibration = Calibration(
        id=None,
        name=name,
        description=description,
        calibration_serialized=calibration_serialized,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    with pytest.raises(ValueError):
        _ = mocked_api.update_calibration(calibration=modified_calibration)

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_update_calibration_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.update_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.ise_response

    calibration_id = 1
    name = "MyDemoCalibration"
    description = "A test calibration"
    device_id = 1
    user_id = 1
    qililab_version = "0.0.0"
    modified_calibration = Calibration(
        id=calibration_id,
        name=name,
        description=description,
        calibration_serialized=calibration_serialized,
        device_id=device_id,
        user_id=user_id,
        qililab_version=qililab_version,
    )

    with pytest.raises(RemoteExecutionException):
        _ = mocked_api.update_calibration(calibration=modified_calibration)

    mocked_web_call.assert_called_with(
        self=mocked_api._connection,
        path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1",
        data=asdict(modified_calibration.calibration_request()),
    )


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_calibration(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.delete_response

    mocked_api.delete_calibration(calibration_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1")


@patch("qiboconnection.connection.Connection.send_delete_auth_remote_api_call", autospec=True)
def test_delete_calibration_ise(mocked_web_call: MagicMock, mocked_api: API):
    """Tests API.delete_calibration() method"""
    mocked_web_call.return_value = web_responses.calibrations.ise_response

    with pytest.raises(RemoteExecutionException):
        mocked_api.delete_calibration(calibration_id=1)

    mocked_web_call.assert_called_with(self=mocked_api._connection, path=f"{mocked_api._CALIBRATIONS_CALL_PATH}/1")


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


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_cancel_job(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.cancel_job() method"""
    mocked_api_call.return_value = web_responses.job_response.cancel_job_response
    mocked_api.cancel_job(job_id=0)

    mocked_api_call.assert_called_with(
        self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/cancel/{0}", data={"job_id": 0}
    )


@patch("qiboconnection.connection.Connection.send_put_auth_remote_api_call", autospec=True)
def test_cancel_job_exception(mocked_api_call: MagicMock, mocked_api: API):
    """Tests API.cancel_job() method with non-existent job id"""
    # Define the behavior of the mocked function to raise the RemoteExecutionException
    mocked_api_call.return_value = web_responses.job_response.cancel_job_response_ise
    with pytest.raises(RemoteExecutionException, match="Job 0 could not be cancelled."):
        # Call the function that should raise the exception
        mocked_api.cancel_job(job_id=0)
    # Assert that the mocked function was called with correct arguments
    mocked_api_call.assert_called_with(
        self=mocked_api._connection, path=f"{mocked_api._JOBS_CALL_PATH}/cancel/{0}", data={"job_id": 0}
    )


class TestExecute:
    """Unit tests for the `API.execute` method."""

    r_mock: responses.RequestsMock

    circuit = Circuit(5)
    circuit.add(gates.X(0))
    circuit.add(gates.H(4))
    circuit.add(gates.M(0, 1, 2, 3, 4))

    vqa = VQA(
        vqa_dict={
            "_name": "VQA",
            "ansatz": {
                "_name": "HardwareEfficientAnsatz",
                "_circuit": {"_type": "QuantumCircuit", "_gates": [], "_init_state": None, "n_qubits": 4},
                "n_qubits": 4,
                "layers": 1,
                "connectivity": [(0, 1), (1, 2), (2, 3)],
                "structure": "grouped",
                "one_gate": "U2",
                "two_gate": "CNOT",
            },
            "backend": {"_type": "Qibo", "_circuit": None, "backend": "numpy", "platform": None},
            "cost_function": {
                "_name": "TSP_CostFunction",
                "instance": {
                    "_name": "TSP_Instance",
                    "n_nodes": 2,
                    "start": None,
                    "loop": True,
                    "_distances": [[0.0, 0.5974254293307999], [0.18562253513856275, 0.0]],
                },
                "parameters": [],
                "encoding": "one_hot",
                "lagrange_multiplier": 10,
            },
            "instance": {
                "_name": "TSP_Instance",
                "n_nodes": 2,
                "start": None,
                "loop": True,
                "_distances": [[0.0, 0.5974254293307999], [0.18562253513856275, 0.0]],
            },
            "optimizer": {"_name": "GradientDescent"},
            "sampler": {
                "_name": "Sampler",
                "_circuit": None,
                "_parameters": [],
                "_quantum_state": None,
                "_probability_dict": None,
                "_required_qubits": None,
            },
            "n_shots": 1000,
        },
        init_params=[0 for __name__ in range(18)],
    )

    def setup_method(self):
        """Method executed before each test contained in this class.

        This method mocks the `requests` calls used inside the API.execute method.
        """
        # TODO: add assert_all_requests_are_fired once device_ids argument is removed from execute
        self.r_mock = responses.RequestsMock(assert_all_requests_are_fired=False)
        self.r_mock.start()
        self.r_mock.add(
            method="GET",
            url="https://qilimanjaroqaas.ddns.net:8080/api/v1/devices/9",
            status=200,
            json={
                "status": "offline",
                "device_id": 9,
                "device_name": "Dummy Device",
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

    def test_execute_vqa(self, mocked_api: API):
        """Test api.execute for a vqa"""
        job_id = mocked_api.execute(vqa=self.vqa, device_id=9, name="test", summary="test")
        assert isinstance(job_id, int)

    # TODO: delete when removing device_ids argument
    def test_execute_with_one_circuit_device_ids(self, mocked_api: API):
        """Test the API.execute method for a single circuit."""
        job_ids = mocked_api.execute(circuit=self.circuit, nshots=1000, device_ids=[9], name="test", summary="test")

        assert job_ids == [0]
        assert len(self.r_mock.calls) == 2
        body = json.loads(self.r_mock.calls[1].request.body.decode())
        assert body["device_id"] == 9
        assert body["number_shots"] == 1000
        assert body["job_type"] == "circuit"
        decoded_description = base64.urlsafe_b64decode(json.loads(body["description"])["data"])
        description_data = json.loads(gzip.decompress(decoded_description))
        assert len(description_data) == 1
        assert description_data[0] == self.circuit.to_qasm()  # make sure we posted the correct circuit
        assert body["summary"] == body["name"] == "test"

    # TODO: delete when removing device_ids argument
    def test_execute_with_one_circuit_ValueError(self, mocked_api: API):
        """Test the API.execute method for a single circuit."""
        with pytest.raises(ValueError) as e:
            mocked_api.execute(
                circuit=self.circuit, nshots=1000, device_ids=[9], device_id=9, name="test", summary="test"
            )
        assert (
            e.value.args[0]
            == "Use only device_id argument, device_ids is deprecated and will be removed in a following qiboconnection version."
        )

    def test_execute_with_one_circuit_device_id(self, mocked_api: API):
        """Test the API.execute method for a single circuit."""
        job_ids = mocked_api.execute(circuit=self.circuit, nshots=1000, device_id=9, name="test", summary="test")

        assert job_ids == 0
        assert len(self.r_mock.calls) == 2
        body = json.loads(self.r_mock.calls[1].request.body.decode())
        assert body["device_id"] == 9
        assert body["number_shots"] == 1000
        assert body["job_type"] == "circuit"
        decoded_description = base64.urlsafe_b64decode(json.loads(body["description"])["data"])
        description_data = json.loads(gzip.decompress(decoded_description))
        assert len(description_data) == 1
        assert description_data[0] == self.circuit.to_qasm()  # make sure we posted the correct circuit
        assert body["summary"] == body["name"] == "test"

    def test_execute_with_multiple_circuits(self, mocked_api: API):
        """Test the API.execute method for multiple circuits."""
        job_ids = mocked_api.execute(circuit=[self.circuit] * 10, nshots=1000, device_ids=[9])

        assert job_ids == [0]
        assert len(self.r_mock.calls) == 2
        body = json.loads(self.r_mock.calls[1].request.body.decode())
        assert body["device_id"] == 9
        assert body["number_shots"] == 1000
        assert body["job_type"] == "circuit"
        decoded_description = base64.urlsafe_b64decode(json.loads(body["description"])["data"])
        description_data = json.loads(gzip.decompress(decoded_description))
        assert len(description_data) == 10
        assert all(d == self.circuit.to_qasm() for d in description_data)  # make sure we posted the correct circuits

    # TODO: delete
    @patch("qiboconnection.api.API._get_job", autospec=True)
    def test_execute_and_return_results_device_ids(self, mocked_get_job: MagicMock, mocked_api: API):
        mocked_get_job.return_value = JobData(
            user_id=1,
            job_type=JobType.OTHER,
            queue_position=0,
            job_id=0,
            result={},
            device_id=9,
            status=JobStatus.COMPLETED,
            number_shots=1000,
            description=json.dumps(compress_any({"data": "unknown description"})),
            name="test",
            summary="test",
        )
        result = mocked_api.execute_and_return_results(
            circuit=[self.circuit] * 10, nshots=1000, device_ids=[9], timeout=10, interval=1
        )
        assert isinstance(result, list | dict)

    @patch("qiboconnection.api.API._get_job", autospec=True)
    def test_execute_and_return_results_device_id(self, mocked_get_job: MagicMock, mocked_api: API):
        mocked_get_job.return_value = JobData(
            user_id=1,
            job_type=JobType.OTHER,
            queue_position=0,
            job_id=0,
            result={},
            device_id=9,
            status=JobStatus.COMPLETED,
            number_shots=1000,
            description=json.dumps(compress_any({"data": "unknown description"})),
            name="test",
            summary="test",
        )
        result = mocked_api.execute_and_return_results(
            circuit=[self.circuit] * 10, nshots=1000, device_id=9, timeout=10, interval=1
        )
        assert isinstance(result, list | dict)

    @patch("qiboconnection.api.API._get_job", autospec=True)
    def test_execute_and_return_results_timeout(self, mocked_get_job: MagicMock, mocked_api: API):
        mocked_get_job.return_value = JobData(
            user_id=1,
            job_type=JobType.OTHER,
            queue_position=0,
            job_id=0,
            result={},
            device_id=9,
            status=JobStatus.PENDING,
            number_shots=1000,
            description=json.dumps(compress_any({"data": "unknown description"})),
            name="test",
            summary="test",
        )

        with pytest.raises(TimeoutError) as e_info:
            _ = mocked_api.execute_and_return_results(
                circuit=[self.circuit] * 10, nshots=1000, device_ids=[9], timeout=1, interval=1
            )
        assert e_info.value.args[0] == "Server did not execute the jobs in time."
