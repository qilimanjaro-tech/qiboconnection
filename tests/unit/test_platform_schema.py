""" Tests methods for platform schema calls """

from unittest.mock import MagicMock, patch

from qiboconnection.models.platform_schema import PlatformSchema

from .data import platform_locations_sample


@patch("qiboconnection.models.platform_schema.Path.mkdir", autospec=True, return_value=None)
@patch("qiboconnection.models.platform_schema.Path.exists", autospec=True, return_value=True)
class TestPlatformSchema:
    """Test methods for platform schema calls"""

    def test_constructor_platform(self, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """Create a new platform"""
        platform_schema = PlatformSchema()
        assert isinstance(platform_schema, PlatformSchema)
        mock_mkdir.assert_not_called()
        mock_exists.assert_called_once()

    def test_create_platform(self, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """Create a new platform"""
        platform_schema_data = PlatformSchema().create()
        assert "id" in platform_schema_data
        assert "location" in platform_schema_data
        mock_exists.assert_called_once()
        mock_mkdir.assert_called_once()

    @patch("qiboconnection.models.platform_schema.Path.iterdir", autospec=True, return_value=platform_locations_sample)
    def test_list_platforms(self, mock_iterdir: MagicMock, mock_exists: MagicMock, mock_mkdir: MagicMock):
        """List all platforms in the system"""
        platform_schemas = PlatformSchema().list_platform_schemas()
        assert isinstance(platform_schemas, list)
        assert len(platform_schemas) == 2
        mock_exists.assert_called_once()
        mock_mkdir.assert_not_called()
        assert mock_iterdir.return_value == platform_locations_sample
