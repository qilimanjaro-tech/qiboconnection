import pytest

from qiboconnection.connection import Connection, ConnectionConfiguration


@pytest.fixture(name="wrong_connection_configuration")
def fixture_wrong_connection_configuration():
    return ConnectionConfiguration(username="wrong_username", api_key="wrong_key")


def test_connection_wrong_login(wrong_connection_configuration: ConnectionConfiguration):

    with pytest.raises(Exception) as e_info:
        Connection(configuration=wrong_connection_configuration, api_path="/api/v1")

    assert e_info.type == ValueError
    assert "Authorisation request failed:" in e_info.value.args[0]
