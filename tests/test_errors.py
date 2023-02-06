""" Test Error rising and utils """

import pytest
from requests.models import HTTPError, Response

from qiboconnection.errors import (
    ConnectionException,
    RemoteExecutionException,
    custom_raise_for_status,
)


@pytest.fixture(name="response_400")
def fixture_response_400():
    """Build the response object associated to a 400 Error Response

    Returns:
        Response: response object
    """
    response = Response()
    response.status_code = 400
    response.url = "server/api"
    response._content = b'{"DEMO": "400"}'
    response.reason = "expired"
    return response


@pytest.fixture(name="response_500")
def fixture_response_500():
    """Build the response object associated to a 500 Error Response

    Returns:
        Response: response object
    """
    response = Response()
    response.status_code = 500
    response.url = "server/api"
    response._content = b'{"DEMO": "500"}'
    response.reason = "internal server error"
    return response


def test_remote_execution_exception():
    """Test the RemoteExecutionException is raised properly when explicitly raised."""
    with pytest.raises(RemoteExecutionException) as e_info:
        raise RemoteExecutionException("DEMO", status_code=500)
    assert e_info.type == RemoteExecutionException
    assert e_info.value.args[0] == "DEMO"
    assert e_info.value.status_code == 500


def test_connection_exception():
    """Test the ConnectionException is raised properly when explicitly raised."""
    with pytest.raises(ConnectionException) as e_info:
        raise ConnectionException
    assert e_info.type == ConnectionException


def test_custom_raise_for_status_400(response_400: Response):
    """Test custom_raise_for_status() raises the proper exception when meeting a status_code 400 response."""
    with pytest.raises(HTTPError) as e_info:
        custom_raise_for_status(response_400)
    assert e_info.type == HTTPError
    assert e_info.value.response == response_400


def test_custom_raise_for_status_500(response_500: Response):
    """Test custom_raise_for_status() raises the proper exception when meeting a status_code 500 response."""
    with pytest.raises(HTTPError) as e_info:
        custom_raise_for_status(response_500)
    assert e_info.type == HTTPError
    assert e_info.value.response == response_500
