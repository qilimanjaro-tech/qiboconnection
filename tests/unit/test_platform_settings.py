""" Tests methods for platform settings calls """

from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from qiboconnection.connection import Connection
from qiboconnection.models.model import Model
from qiboconnection.models.platform_settings import ALL_SETTINGS_PATH, PlatformSettings

from ..data import sample_all_platform_settings


@pytest.fixture(name="mocked_platform_settings")
def fixture_mocked_platform_settings(mocked_connection: Connection) -> PlatformSettings:
    """Create a mocked Platform Settings

    Args:
        mocked_connection (Connection): Mocked Connection

    Returns:
        PlatformSettings: Platform Settings object
    """
    return PlatformSettings(connection=mocked_connection)


class TestPlatformSettings:
    """Test platform settings platform"""

    def test_platform_settings_constructor(self, mocked_connection: Connection):
        """Test a new PlatformSettings object"""
        platform_settings = PlatformSettings(connection=mocked_connection)
        assert isinstance(platform_settings, PlatformSettings)
        assert platform_settings.collection_name == "platform_settings"

    @patch.object(
        Model,
        "read",
        return_value=sample_all_platform_settings,
    )
    def test_platform_settings_read_all_settings(
        self, patched_model: MagicMock, mocked_platform_settings: PlatformSettings
    ):
        """test the creation of a new platform bus settings model"""
        response = mocked_platform_settings.read_all_settings(
            platform_settings_id=cast(int, sample_all_platform_settings["platform"]["id_"])
        )
        assert isinstance(response, dict)
        assert response == sample_all_platform_settings
        patched_model.assert_called_with(
            path=f"{mocked_platform_settings.collection_name}/{sample_all_platform_settings['platform']['id_']}/{ALL_SETTINGS_PATH}"
        )
        patched_model.assert_called_once()
