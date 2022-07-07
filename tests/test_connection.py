""" Test methods for Connection """

import pytest

from qiboconnection.connection import Connection, ConnectionConfiguration


@pytest.fixture(name="wrong_connection_configuration")
def fixture_wrong_connection_configuration():
    """Creates a login info object with wrong credentials

    Returns:
       ConnectionConfiguration: object containing wrong login data."""
    return ConnectionConfiguration(username="wrong_username", api_key="wrong_key")


def test_connection_wrong_login(wrong_connection_configuration: ConnectionConfiguration):
    """Tries to instance a Connection object with wrong login data expecting to get a ValueError.

    Args:
        wrong_connection_configuration: login credentials
    """
    with pytest.raises(ValueError) as e_info:
        Connection(configuration=wrong_connection_configuration, api_path="/api/v1")

    assert "Authorisation request failed:" in e_info.value.args[0]
