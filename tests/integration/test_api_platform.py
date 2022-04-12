""" Tests methods for API platform settings calls """


from typing import Tuple

import pytest

from qiboconnection.api import API

from .data import platform_settings_sample, platform_settings_updated_sample


@pytest.fixture(name="temp_platform_id_settings_id")
def fixture_temp_platform_settings(mocked_api: API, platform: dict) -> Tuple[int, int]:
    """Create a new platform settings as a fixture"""
    platform_settings = mocked_api.create_platform_settings(
        platform_id=platform["id"], platform_settings=platform_settings_sample
    )
    return platform["id"], platform_settings["id"]


class TestAPIPlatform:
    """Tests methods for API platform calls"""

    def test_create_platform(self, mocked_api: API):
        """Create a new platform"""
        platform_data = mocked_api.create_platform()
        assert "id" in platform_data
        assert "location" in platform_data

    def test_list_platforms(self, mocked_api: API):
        """List all platforms in the system"""
        platforms = mocked_api.list_platforms()
        assert isinstance(platforms, list)


class TestAPIPlatformSettings:
    """Tests methods for API platform settings calls"""

    def test_create_platform_settings(self, mocked_api: API, platform: dict):
        """test the creation of a new platform settings"""
        platform_settings = mocked_api.create_platform_settings(
            platform_id=platform["id"], platform_settings=platform_settings_sample
        )
        assert isinstance(platform_settings, dict)
        assert "id" in platform_settings

    def test_read_platform_settings(self, mocked_api: API, platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = platform_id_settings_id[0]
        platform_settings_id = platform_id_settings_id[1]

        platform_settings = mocked_api.read_platform_settings(
            platform_id=platform_id, platform_settings_id=platform_settings_id
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id

    def test_update_platform_settings(self, mocked_api: API, platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = platform_id_settings_id[0]
        platform_settings_id = platform_id_settings_id[1]

        platform_settings = mocked_api.update_platform_settings(
            platform_id=platform_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings_updated_sample,
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        assert platform_settings_updated_sample["hardware_average"] == platform_settings["hardware_average"]

    def test_delete_platform_settings(self, mocked_api: API, temp_platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = temp_platform_id_settings_id[0]
        platform_settings_id = temp_platform_id_settings_id[1]

        platform_settings = mocked_api.read_platform_settings(
            platform_id=platform_id, platform_settings_id=platform_settings_id
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id

        try:
            mocked_api.delete_platform_settings(platform_id=platform_id, platform_settings_id=platform_settings_id)
        except Exception as ex:  # pylint: disable=broad-except
            assert False, f"'delete' raised an exception {ex}"

        with pytest.raises((FileNotFoundError, ValueError)):
            mocked_api.read_platform_settings(platform_id=platform_id, platform_settings_id=platform_settings_id)
