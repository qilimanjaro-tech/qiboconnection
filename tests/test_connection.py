""" Test methods for Connection """
from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest
from requests import Response, delete, get, post, put

from qiboconnection.connection import Connection, refresh_token_if_unauthorised
from qiboconnection.errors import ConnectionException, HTTPError
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


@patch("qiboconnection.connection.requests.post", autospec=True)
def test_update_authorisation_using_refresh_token_no_server_refresh_api_call(
    mocked_rest_call: MagicMock, mocked_connection: Connection
):
    """test Connection's update_authorisation_using_refresh_token, with no refresh api call defined"""

    mocked_connection_copy = deepcopy(mocked_connection)

    mocked_rest_call.return_value = web_responses.auth.raw_retrieve_response

    mocked_connection_copy._authorisation_server_refresh_api_call = None

    with pytest.raises(ValueError, match="Authorisation server api call is required"):
        mocked_connection_copy.update_authorisation_using_refresh_token()


@patch("qiboconnection.connection.requests.post", autospec=True)
def test_update_authorisation_using_refresh_token_unsuccessful(
    mocked_rest_call: MagicMock, mocked_connection: Connection
):
    """test Connection's update_authorisation_using_refresh_token"""

    mocked_rest_call.return_value = web_responses.raw.response_400

    mocked_connection._authorisation_refresh_token = (
        "eyJhbGciOiJFZERTQSIsImtpZCI6InlYaG5lSUtxUEV5UklSLXVyMHdGZUZzLTZ2VS01amJEY18wUFN0X2Etc1UiLCJ0eXAiOiJKV1QifQ"
        + ".eyJhdWQiOiJodHRwczovL3FpbGltYW5qYXJvZGV2LmRkbnMubmV0OjgwODAvYXBpL3YxIiwiZXhwIjoxNjg0NDk"
        + "yMDcxLCJpYXQiOjE2ODQ0MDU2NzEsImlzcyI6Imh0dHBzOi8vcWlsaW1hbmphcm9kZXYuZGRucy5uZXQ6ODA4MC8i"
        + "LCJ0eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjMsInVzZXJfcm9sZSI6ImFkbWluIn0"
        + ".4oSyRW9Ia7C-50x2yZxQAEXDZp-TLkFkPOtHBR4cCi9LnkREtYrJpDXufep_EYoRwDSJL_2z20moYMuMHy0QCg"
    )

    with pytest.raises(ValueError, match=f"Authorisation request failed: {web_responses.raw.response_400.reason}"):
        mocked_connection.update_authorisation_using_refresh_token()


@patch("qiboconnection.connection.requests.post", autospec=True)
def test_update_authorisation_using_refresh_token(mocked_rest_call: MagicMock, mocked_connection: Connection):
    """test Connection's update_authorisation_using_refresh_token"""

    mocked_rest_call.return_value = web_responses.auth.raw_retrieve_response

    mocked_connection._authorisation_refresh_token = (
        "eyJhbGciOiJFZERTQSIsImtpZCI6InlYaG5lSUtxUEV5UklSLXVyMHdGZUZzLTZ2VS01amJEY18wUFN0X2Etc1UiLCJ0eXAiOiJKV1QifQ"
        + ".eyJhdWQiOiJodHRwczovL3FpbGltYW5qYXJvZGV2LmRkbnMubmV0OjgwODAvYXBpL3YxIiwiZXhwIjoxNjg0NDk"
        + "yMDcxLCJpYXQiOjE2ODQ0MDU2NzEsImlzcyI6Imh0dHBzOi8vcWlsaW1hbmphcm9kZXYuZGRucy5uZXQ6ODA4MC8i"
        + "LCJ0eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjMsInVzZXJfcm9sZSI6ImFkbWluIn0"
        + ".4oSyRW9Ia7C-50x2yZxQAEXDZp-TLkFkPOtHBR4cCi9LnkREtYrJpDXufep_EYoRwDSJL_2z20moYMuMHy0QCg"
    )

    mocked_connection.update_authorisation_using_refresh_token()

    mocked_rest_call.assert_called_with(
        mocked_connection._authorisation_server_refresh_api_call,
        json={},
        headers={
            "Authorization": (
                "Bearer "
                + "eyJhbGciOiJFZERTQSIsImtpZCI6InlYaG5lSUtxUEV5Uk"
                + "lSLXVyMHdGZUZzLTZ2VS01amJEY18wUFN0X2Etc1UiLCJ0eXAiOiJKV1QifQ"
                + ".eyJhdWQiOiJodHRwczovL3FpbGltYW5qYXJvZGV2LmRkbnMubmV0OjgwODAvYXBpL3YxIiwiZXhwIjoxNjg0NDk"
                + "yMDcxLCJpYXQiOjE2ODQ0MDU2NzEsImlzcyI6Imh0dHBzOi8vcWlsaW1hbmphcm9kZXYuZGRucy5uZXQ6ODA4MC8i"
                + "LCJ0eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjMsInVzZXJfcm9sZSI6ImFkbWluIn0"
                + ".4oSyRW9Ia7C-50x2yZxQAEXDZp-TLkFkPOtHBR4cCi9LnkREtYrJpDXufep_EYoRwDSJL_2z20moYMuMHy0QCg"
            )
        },
    )
    assert (
        mocked_connection._authorisation_access_token == web_responses.auth.raw_retrieve_response.json()["accessToken"]
    ), "Value of saved access token does not coincide with the one provided in response."


def test_refresh_token_if_unauthorised_when_ok():
    """Tests the refresh_token_if_unauthorised with a valid response"""

    func = MagicMock()
    connection = MagicMock()

    refresh_token_if_unauthorised(func=func)(self=connection)

    func.assert_called_once_with(connection)
    connection.update_authorisation_using_refresh_token.assert_not_called()


def test_refresh_token_if_unauthorised_when_unauthorised():
    """Tests the refresh_token_if_unauthorised with a valid response"""

    func = MagicMock()
    func.side_effect = [HTTPError(response=web_responses.raw.response_401), func.DEFAULT]
    connection = MagicMock()

    refresh_token_if_unauthorised(func=func)(self=connection)

    assert func.call_count == 2
    connection.update_authorisation_using_refresh_token.assert_called_once_with()


def test_refresh_token_if_unauthorised_when_other_error():
    """Tests the refresh_token_if_unauthorised with a valid response"""

    func = MagicMock()
    func.side_effect = HTTPError(response=web_responses.raw.response_500)
    connection = MagicMock()

    with pytest.raises(HTTPError):
        refresh_token_if_unauthorised(func=func)(self=connection)

    func.assert_called_once_with(connection)
    connection.update_authorisation_using_refresh_token.assert_not_called()
