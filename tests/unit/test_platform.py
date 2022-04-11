""" Tests methods for platform calls """

from unittest.mock import MagicMock, patch

from qiboconnection.models.platform import Platform

from .data import platform_locations_sample


@patch("qiboconnection.models.platform.Path.mkdir", autospec=True, return_value=None)
@patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
class TestPlatform:
    """Test methods for platform calls"""

    def test_constructor_platform(self, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """Create a new platform"""
        platform = Platform()
        assert isinstance(platform, Platform)
        mock_mkdir.assert_not_called()
        mock_exists.assert_called_once()

    def test_create_platform(self, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """Create a new platform"""
        platform_data = Platform().create()
        assert "id" in platform_data
        assert "location" in platform_data
        mock_exists.assert_called_once()
        mock_mkdir.assert_called_once()

    @patch("qiboconnection.models.platform.Path.iterdir", autospec=True, return_value=platform_locations_sample)
    def test_list_platforms(self, mock_iterdir: MagicMock, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """List all platforms in the system"""
        platforms = Platform().list_platforms()
        assert isinstance(platforms, list)
        assert len(platforms) == 2
        mock_exists.assert_called_once()
        mock_mkdir.assert_not_called()
        assert mock_iterdir.return_value == platform_locations_sample
