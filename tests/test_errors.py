import pytest
from requests.models import HTTPError, Response

from qiboconnection.errors import (
    ConnectionException,
    RemoteExecutionException,
    custom_raise_for_status,
)


@pytest.fixture(name="response_400")
def fixture_response_400():
    response = Response()
    response.code = "expired"
    response.error_type = "expired"
    response.status_code = 400
    response.url = "server/api"
    response._content = b'{"DEMO": "400"}'
    response.reason = b"expired"
    return response


@pytest.fixture(name="response_500")
def fixture_response_500():
    response = Response()
    response.code = "internal server error"
    response.error_type = "internal server error"
    response.status_code = 500
    response.url = "server/api"
    response._content = b'{"DEMO": "500"}'
    response.reason = "internal server error"
    return response


def test_remote_execution_exception():
    with pytest.raises(Exception) as e_info:
        raise RemoteExecutionException("DEMO", status_code=500)
    assert e_info.type == RemoteExecutionException
    assert e_info.value.args[0] == "DEMO"
    assert e_info.value.status_code == 500


def test_connection_exception():
    with pytest.raises(Exception) as e_info:
        raise ConnectionException
    assert e_info.type == ConnectionException


def test_custom_raise_for_status_400(response_400: Response):
    with pytest.raises(Exception) as e_info:
        custom_raise_for_status(response_400)
    assert e_info.type == HTTPError
    assert e_info.value.response == response_400


def test_custom_raise_for_status_500(response_500: Response):
    with pytest.raises(Exception) as e_info:
        custom_raise_for_status(response_500)
    assert e_info.type == HTTPError
    assert e_info.value.response == response_500
