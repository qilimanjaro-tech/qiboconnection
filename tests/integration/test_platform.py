""" Tests methods for platform schema calls """

from qiboconnection.models.platform_schema import PlatformSchema


class TestPlatformSchema:
    """Test methods for platform calls"""

    def test_create_platform_schema(self):
        """Create a new platform schema"""
        platform_schema_data = PlatformSchema().create()
        assert "id" in platform_schema_data
        assert "location" in platform_schema_data

    def test_list_platform_schemas(self):
        """List all platform schemas in the system"""
        platform_schemas = PlatformSchema().list_platform_schemas()
        assert isinstance(platform_schemas, list)
