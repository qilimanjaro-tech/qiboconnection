""" Tests methods for platform settings calls """

import unittest
from typing import Tuple
from unittest.mock import MagicMock, patch

from qiboconnection.models.platform_settings import PlatformSettings

from .data import (
    platform_mocked_settings_sample,
    platform_settings_sample,
    platform_settings_updated_sample,
)


@patch("builtins.open", unittest.mock.mock_open())
class TestPlatformSettings:
    """Test platform settings platform"""

    @patch("qiboconnection.models.model.yaml.dump", autospec=True, return_value=None)
    @patch("qiboconnection.models.platform.Path.iterdir", autospec=True, return_value=[])
    def test_create_platform_settings(
        self,
        mock_iterdir: MagicMock,
        mock_dump: MagicMock,
        mocked_platform: dict,
    ):
        """test the creation of a new platform settings"""
        assert "id" in mocked_platform
        platform_settings = PlatformSettings().create(
            platform_id=mocked_platform["id"], platform_settings=platform_settings_sample
        )
        assert isinstance(platform_settings, dict)
        assert "id" in platform_settings
        mock_iterdir.assert_called()
        mock_dump.assert_called()

    @patch("qiboconnection.models.model.yaml.safe_load", autospec=True, return_value=platform_mocked_settings_sample)
    def test_read_platform_settings(self, mock_load: MagicMock, mocked_platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        platform_settings = PlatformSettings().read(platform_id=platform_id, platform_settings_id=platform_settings_id)
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        mock_load.assert_called()

    @patch("qiboconnection.models.model.yaml.dump", autospec=True, return_value=None)
    def test_update_platform_settings(self, mock_dump: MagicMock, mocked_platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        platform_settings = PlatformSettings().update(
            platform_id=platform_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings_updated_sample,
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        assert platform_settings_updated_sample["hardware_average"] == platform_settings["hardware_average"]
        mock_dump.assert_called()

    @patch("qiboconnection.models.model.Path.unlink", autospec=True, return_value=None)
    def test_delete_platform_settings(self, mock_unlink: MagicMock, mocked_platform_id_settings_id: Tuple[int, int]):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        try:
            PlatformSettings().delete(platform_id=platform_id, platform_settings_id=platform_settings_id)
        except Exception as ex:  # pylint: disable=broad-except
            assert False, f"'delete' raised an exception {ex}"
        mock_unlink.assert_called()
