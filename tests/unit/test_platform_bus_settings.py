""" Tests methods for platform bus settings calls """

from unittest.mock import MagicMock, patch

import pytest

from qiboconnection.connection import Connection
from qiboconnection.models.model import Model
from qiboconnection.models.platform_bus_settings import PlatformBusSettings

from ..data import sample_bus_model_data

PLATFORM_SCHEMA_SETTINGS_ID = 1
PLATFORM_BUS_SETTINGS_ID = 1

sample_result_create_data = {"id": PLATFORM_BUS_SETTINGS_ID} | sample_bus_model_data


@pytest.fixture(name="mocked_platform_bus_settings")
def fixture_mocked_platform_bus_settings(mocked_connection: Connection) -> PlatformBusSettings:
    """Create a mocked Platform Bus Settings

    Args:
        mocked_connection (Connection): Mocked Connection

    Returns:
        PlatformBusSettings: Platform Bus Settings object
    """
    return PlatformBusSettings(connection=mocked_connection)


class TestPlatformBusSettingss:
    """Test methods for platform bus settings calls"""

    def test_platform_bus_settings_constructor(self, mocked_connection: Connection):
        """Test a new Platform Bus Settings object"""
        platform_bus_settings = PlatformBusSettings(connection=mocked_connection)
        assert isinstance(platform_bus_settings, PlatformBusSettings)
        assert platform_bus_settings.collection_name == "platform_bus_settings"

    def test_platform_bus_settings_create(self, mocked_platform_bus_settings: PlatformBusSettings):
        """test the creation of a new data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_bus_settings.create(data=sample_bus_model_data)

    @patch.object(
        Model,
        "create",
        return_value=sample_result_create_data,
    )
    def test_platform_bus_settings_create_settings(
        self, patched_model: MagicMock, mocked_platform_bus_settings: PlatformBusSettings
    ):
        """test the creation of a new platform bus settings model"""
        response = mocked_platform_bus_settings.create_settings(
            platform_schema_settings_id=PLATFORM_SCHEMA_SETTINGS_ID, platform_bus_settings=sample_bus_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_model.assert_called_with(
            data=sample_bus_model_data,
            path=f"{mocked_platform_bus_settings.collection_name}?platform_schema_settings_id={PLATFORM_SCHEMA_SETTINGS_ID}",
        )
        patched_model.assert_called_once()

    def test_platform_settings_list_elements(self, mocked_platform_bus_settings: PlatformBusSettings):
        """test listing elements of a data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_bus_settings.list_elements()
