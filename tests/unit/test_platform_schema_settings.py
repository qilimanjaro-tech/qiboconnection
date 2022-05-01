""" Tests methods for platform schema calls """

from unittest.mock import MagicMock, patch

import pytest

from qiboconnection.connection import Connection
from qiboconnection.models.model import Model
from qiboconnection.models.platform_schema_settings import PlatformSchemaSettings

from ..data import sample_schema_model_data

PLATFORM_SETTINGS_ID = 15
PLATFORM_SCHEMA_SETTINGS_ID = 1

sample_result_create_data = {"id": PLATFORM_SCHEMA_SETTINGS_ID} | sample_schema_model_data


@pytest.fixture(name="mocked_platform_schema_settings")
def fixture_mocked_platform_schema_settings(mocked_connection: Connection) -> PlatformSchemaSettings:
    """Create a mocked Platform Schema Settings

    Args:
        mocked_connection (Connection): Mocked Connection

    Returns:
        PlatformSchemaSettings: Platform Schema Settings object
    """
    return PlatformSchemaSettings(connection=mocked_connection)


class TestPlatformSchemaSettings:
    """Test methods for platform schema settings calls"""

    def test_platform_schema_settings_constructor(self, mocked_connection: Connection):
        """Test a new Platform Schema Settings object"""
        platform_schema_settings = PlatformSchemaSettings(connection=mocked_connection)
        assert isinstance(platform_schema_settings, PlatformSchemaSettings)
        assert platform_schema_settings.collection_name == "platform_schema_settings"

    def test_platform_schema_settings_create(self, mocked_platform_schema_settings: PlatformSchemaSettings):
        """test the creation of a new data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_schema_settings.create(data=sample_schema_model_data)

    @patch.object(
        Model,
        "create",
        return_value=sample_result_create_data,
    )
    def test_platform_schema_settings_create_settings(
        self, patched_model: MagicMock, mocked_platform_schema_settings: PlatformSchemaSettings
    ):
        """test the creation of a new platform bus settings model"""
        response = mocked_platform_schema_settings.create_settings(
            platform_settings_id=PLATFORM_SETTINGS_ID, platform_schema_settings=sample_schema_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_model.assert_called_with(
            data=sample_schema_model_data,
            path=f"{mocked_platform_schema_settings.collection_name}?platform_settings_id={PLATFORM_SETTINGS_ID}",
        )
        patched_model.assert_called_once()

    def test_platform_settings_list_elements(self, mocked_platform_schema_settings: PlatformSchemaSettings):
        """test listing elements of a data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_schema_settings.list_elements()
