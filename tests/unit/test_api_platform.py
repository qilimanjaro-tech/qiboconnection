""" Tests methods for API platform settings calls """

import unittest
from typing import Tuple
from unittest.mock import MagicMock, patch

from qiboconnection.api import API

from .data import (
    platform_locations_sample,
    platform_mocked_settings_sample,
    platform_settings_sample,
    platform_settings_updated_sample,
)


@patch("builtins.open", unittest.mock.mock_open())
class TestAPIPlatform:
    """Tests methods for API platform calls"""

    @patch("qiboconnection.models.platform.Path.iterdir", autospec=True, return_value=[])
    @patch("qiboconnection.models.platform.Path.mkdir", autospec=True, return_value=None)
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_create_platform(
        self,
        mock_exists: MagicMock,
        mock_mkdir: MagicMock,
        mock_iterdir: MagicMock,
        mocked_api: API,
    ):
        """Create a new platform"""
        platform_data = mocked_api.create_platform()
        assert "id" in platform_data
        assert "location" in platform_data
        mock_exists.assert_called()
        mock_mkdir.assert_called()
        mock_iterdir.assert_called()

    @patch("qiboconnection.models.platform.Path.iterdir", autospec=True, return_value=platform_locations_sample)
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_list_platforms(self, mock_exists: MagicMock, mock_iterdir: MagicMock, mocked_api: API):
        """List all platforms in the system"""
        platforms = mocked_api.list_platforms()
        assert isinstance(platforms, list)
        assert len(platforms) == 2
        mock_exists.assert_called()
        assert mock_iterdir.return_value == platform_locations_sample


@patch("builtins.open", unittest.mock.mock_open())
class TestAPIPlatformSettings:
    """Tests methods for API platform settings calls"""

    @patch("qiboconnection.models.platform.Path.iterdir", autospec=True, return_value=[])
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_create_platform_settings(
        self, mock_exists: MagicMock, mock_iterdir: MagicMock, mocked_api: API, mocked_platform: dict
    ):
        """test the creation of a new platform settings"""
        platform_settings = mocked_api.create_platform_settings(
            platform_id=mocked_platform["id"], platform_settings=platform_settings_sample
        )
        assert isinstance(platform_settings, dict)
        assert "id" in platform_settings
        mock_exists.assert_called()
        mock_iterdir.assert_called()

    @patch("qiboconnection.models.model.yaml.safe_load", autospec=True, return_value=platform_mocked_settings_sample)
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_read_platform_settings(
        self,
        mock_exists: MagicMock,
        mock_load: MagicMock,
        mocked_api: API,
        mocked_platform_id_settings_id: Tuple[int, int],
    ):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        platform_settings = mocked_api.read_platform_settings(
            platform_id=platform_id, platform_settings_id=platform_settings_id
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        mock_exists.assert_called()
        mock_load.assert_called()

    @patch("qiboconnection.models.model.yaml.dump", autospec=True, return_value=None)
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_update_platform_settings(
        self,
        mock_exists: MagicMock,
        mock_dump: MagicMock,
        mocked_api: API,
        mocked_platform_id_settings_id: Tuple[int, int],
    ):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        platform_settings = mocked_api.update_platform_settings(
            platform_id=platform_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings_updated_sample,
        )
        assert isinstance(platform_settings, dict)
        assert platform_settings["id"] == platform_settings_id
        assert platform_settings_updated_sample["hardware_average"] == platform_settings["hardware_average"]
        mock_exists.assert_called()
        mock_dump.assert_called()

    @patch("qiboconnection.models.model.Path.unlink", autospec=True, return_value=None)
    @patch("qiboconnection.models.platform.Path.exists", autospec=True, return_value=True)
    def test_delete_platform_settings(
        self,
        mock_exists: MagicMock,
        mock_unlink: MagicMock,
        mocked_api: API,
        mocked_platform_id_settings_id: Tuple[int, int],
    ):
        """test the read of a created platform settings"""
        platform_id = mocked_platform_id_settings_id[0]
        platform_settings_id = mocked_platform_id_settings_id[1]

        try:
            mocked_api.delete_platform_settings(platform_id=platform_id, platform_settings_id=platform_settings_id)
        except Exception as ex:  # pylint: disable=broad-except
            assert False, f"'delete' raised an exception {ex}"
        mock_exists.assert_called()
        mock_unlink.assert_called()
