""" Test API calls """

from unittest.mock import patch

from qiboconnection.api import API
from qiboconnection.typings.connection import ConnectionEstablished


class TestAPI:
    """Test API calls"""

    def test_api_constructor(self, mocked_connection_established: ConnectionEstablished):
        """Construct an API instance"""
        with patch(
            "qiboconnection.connection.load_config_file_to_disk",
            autospec=True,
            return_value=mocked_connection_established,
        ) as mock_config:
            api = API()
            assert isinstance(api, API)
            mock_config.assert_called()
