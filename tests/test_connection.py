""" Test methods for Connection """

from qiboconnection.connection import Connection


def test_connection_constructor(mocked_connection: Connection):
    """Test Connection class constructor"""
    assert isinstance(mocked_connection, Connection)
