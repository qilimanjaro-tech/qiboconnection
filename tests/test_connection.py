""" Test methods for Connection """
from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest
from requests import Response, delete, get, post, put

from qiboconnection.connection import Connection
from qiboconnection.user import User

from .data import web_responses


def test_constructor(mocked_connection: Connection):
    """Test Connection class constructor"""
    assert isinstance(mocked_connection, Connection)


def test_user(mocked_connection: Connection):
    """Test Connection user property"""
    assert isinstance(mocked_connection.user, User)


def test_user_when_not_defined(mocked_connection_no_user: Connection):
    """Test Connection user property"""

    with pytest.raises(ValueError):
        _ = mocked_connection_no_user.user


def test_username(mocked_connection: Connection):
    """Test Connection user property"""
    assert isinstance(mocked_connection.username, str)


def test_username_when_user_not_defined(mocked_connection_no_user: Connection):
    """Test Connection user property"""

    with pytest.raises(ValueError):
        _ = mocked_connection_no_user.username


def test_user_id(mocked_connection: Connection):
    """Test Connection user property"""
    assert isinstance(mocked_connection._user_id, int)


def test_connection_user_id_when_user_not_defined(mocked_connection_no_user: Connection):
    """Test Connection user property"""
    with pytest.raises(ValueError):
        _ = mocked_connection_no_user._user_id


def test_connection_user_id_setter(mocked_connection: Connection):
    """Test Connection user property"""
    mocked_connection._user_id = 555
    assert mocked_connection._user_id == 555


def test_connection_user_id_setter_when_user_not_defined(mocked_connection_no_user: Connection):
    """Test Connection user property"""
    with pytest.raises(ValueError):
        mocked_connection_no_user._user_id = 555


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_user_slack_id_local(mocked_web_call: MagicMock, mocked_connection: Connection):
    """Test Connection user_slack_id property"""
    mocked_web_call.return_value = web_responses.users.retrieve_response
    connection = deepcopy(mocked_connection)
    connection._user_slack_id = "Random ID"

    slack_id = connection.user_slack_id

    mocked_web_call.assert_not_called()
    assert slack_id == "Random ID"


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_user_slack_id(mocked_web_call: MagicMock, mocked_connection: Connection):
    """Test Connection user_slack_id property"""
    mocked_web_call.return_value = web_responses.users.retrieve_response
    connection = deepcopy(mocked_connection)
    connection._user_slack_id = None

    slack_id = connection.user_slack_id

    mocked_web_call.assert_called_with(self=connection, path=f"/users/{connection.user.user_id}")
    assert slack_id == web_responses.users.retrieve_response[0]["slack_id"]


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_user_slack_id_ise(mocked_web_call: MagicMock, mocked_connection: Connection):
    """Test Connection user_slack_id property fails with failing response"""
    mocked_web_call.return_value = web_responses.users.ise_response
    connection = deepcopy(mocked_connection)

    with pytest.raises(ValueError):
        _ = connection.user_slack_id

    mocked_web_call.assert_called_with(self=connection, path=f"/users/{connection.user.user_id}")


@patch("qiboconnection.connection.Connection.send_get_auth_remote_api_call", autospec=True)
def test_user_slack_id_without_user(mocked_web_call: MagicMock, mocked_connection_no_user: Connection):
    """Test Connection user_slack_id property fails without local user"""
    mocked_web_call.return_value = web_responses.users.retrieve_response

    with pytest.raises(ValueError):
        _ = mocked_connection_no_user.user_slack_id

    mocked_web_call.assert_not_called()


@patch("qiboconnection.connection.requests.put", autospec=True)
def test_send_put_auth_remote_api_call(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """tests send_put_auth_remote_api_call"""
    mocked_rest_call.return_value = web_responses.raw.response_200

    response, code = mocked_connection.send_put_auth_remote_api_call(path="/PATH", data={"demo": "demo"})

    mocked_rest_call.assert_called_with(
        f"{mocked_connection._remote_server_api_url}/PATH",
        json={"demo": "demo"},
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        },
    )
    assert response == web_responses.raw.response_200.json()
    assert code == web_responses.raw.response_200.status_code


@patch("qiboconnection.connection.requests.post", autospec=True)
def test_send_post_auth_remote_api_call(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """tests send_post_auth_remote_api_call"""
    mocked_rest_call.return_value = web_responses.raw.response_201

    response, code = mocked_connection.send_post_auth_remote_api_call(path="/PATH", data={"demo": "demo"})

    mocked_rest_call.assert_called_with(
        f"{mocked_connection._remote_server_api_url}/PATH",
        json={"demo": "demo"},
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        },
    )
    assert response == web_responses.raw.response_201.json()
    assert code == web_responses.raw.response_201.status_code


@patch("qiboconnection.connection.requests.get", autospec=True)
def test_send_get_auth_remote_api_call(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """tests send_get_auth_remote_api_call"""
    mocked_rest_call.return_value = web_responses.raw.response_200

    response, code = mocked_connection.send_get_auth_remote_api_call(path="/PATH", params={"demo": "demo"})

    mocked_rest_call.assert_called_with(
        f"{mocked_connection._remote_server_api_url}/PATH",
        params={"demo": "demo"},
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        },
    )
    assert response == web_responses.raw.response_200.json()
    assert code == web_responses.raw.response_200.status_code


@patch("qiboconnection.connection.requests.delete", autospec=True)
def test_send_delete_auth_remote_api_call(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """tests send_delete_auth_remote_api_call"""
    mocked_rest_call.return_value = web_responses.raw.response_204

    response, code = mocked_connection.send_delete_auth_remote_api_call(path="/PATH")

    mocked_rest_call.assert_called_with(
        f"{mocked_connection._remote_server_api_url}/PATH",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        },
    )
    assert response == web_responses.raw.response_204.json()
    assert code == web_responses.raw.response_204.status_code


@patch("qiboconnection.connection.requests.get", autospec=True)
def test_send_get_remote_call(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """tests send_get_remote_call"""
    mocked_rest_call.return_value = web_responses.raw.response_200

    response, code = mocked_connection.send_get_remote_call(path="/PATH")

    mocked_rest_call.assert_called_with(
        f"{mocked_connection._remote_server_base_url}/PATH",
    )
    assert response == web_responses.raw.response_200.json()
    assert code == web_responses.raw.response_200.status_code
