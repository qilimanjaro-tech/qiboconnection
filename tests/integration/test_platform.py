""" Tests methods for platform calls """

from qiboconnection.models.platform import Platform


class TestPlatform:
    """Test methods for platform calls"""

    def test_create_platform(self):
        """Create a new platform"""
        platform_data = Platform().create()
        assert "id" in platform_data
        assert "location" in platform_data

    def test_list_platforms(self):
        """List all platforms in the system"""
        platforms = Platform().list_platforms()
        assert isinstance(platforms, list)
