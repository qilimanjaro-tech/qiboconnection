""" Tests methods for platform settings calls """

from typing import Tuple

import pytest

from qiboconnection.models.platform_settings import PlatformSettings

from .data import platform_settings_sample, platform_settings_updated_sample


@pytest.fixture(name="temp_platform_schema_id_settings_id")
def fixture_temp_platform_settings(platform_schema: dict) -> Tuple[int, int]:
    """Create a new platform settings as a fixture"""
    platform_settings = PlatformSettings().create(
        platform_schema_id=platform_schema["id"], platform_settings=platform_settings_sample
    )
    return platform_schema["id"], platform_settings["id"]


class TestPlatformSettings:
    """Test platform settings platform"""

    def test_create_platform_settings(self, platform_schema: dict):
        """test the creation of a new platform settings"""
        assert "id" in platform_schema
        platform_settings = PlatformSettings().create(
            platform_schema_id=platform_schema["id"], platform_settings=platform_settings_sample
        )
        assert isinstance(platform_settings, dict)
        assert "id" in platform_settings

    def test_read_platform_settings(self, platform_schema_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_schema_id = platform_schema_id_settings_id[0]
        platform_settings_id = platform_schema_id_settings_id[1]

        platform_settings = PlatformSettings().read(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id

    def test_update_platform_settings(self, platform_schema_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_schema_id = platform_schema_id_settings_id[0]
        platform_settings_id = platform_schema_id_settings_id[1]

        platform_settings = PlatformSettings().update(
            platform_schema_id=platform_schema_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings_updated_sample,
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        assert platform_settings_updated_sample["hardware_average"] == platform_settings["hardware_average"]

    def test_delete_platform_settings(self, temp_platform_schema_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_schema_id = temp_platform_schema_id_settings_id[0]
        platform_settings_id = temp_platform_schema_id_settings_id[1]

        platform_settings = PlatformSettings().read(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id

        try:
            PlatformSettings().delete(platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id)
        except Exception as ex:  # pylint: disable=broad-except
            assert False, f"'delete' raised an exception {ex}"

        with pytest.raises(FileNotFoundError):
            PlatformSettings().read(platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id)
