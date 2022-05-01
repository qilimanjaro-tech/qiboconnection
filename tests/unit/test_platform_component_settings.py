""" Tests methods for platform component settings calls """

from unittest.mock import MagicMock, patch

import pytest

from qiboconnection.connection import Connection
from qiboconnection.models.model import Model
from qiboconnection.models.platform_component_settings import PlatformComponentSettings

from ..data import sample_component_model_data

PLATFORM_BUS_SETTINGS_ID = 4
PLATFORM_PARENT_COMPONENT_SETTINGS_ID = 10
PLATFORM_COMPONENT_SETTINGS_ID = 1

sample_result_create_data = {"id": PLATFORM_COMPONENT_SETTINGS_ID} | sample_component_model_data


@pytest.fixture(name="mocked_platform_component_settings")
def fixture_mocked_platform_component_settings(mocked_connection: Connection) -> PlatformComponentSettings:
    """Create a mocked Platform Component Settings

    Args:
        mocked_connection (Connection): Mocked Connection

    Returns:
        PlatformComponentSettings: Platform Component Settings object
    """
    return PlatformComponentSettings(connection=mocked_connection)


class TestPlatformComponentSettingss:
    """Test methods for platform component settings calls"""

    def test_platform_component_settings_constructor(self, mocked_connection: Connection):
        """Test a new Platform Component Settings object"""
        platform_component_settings = PlatformComponentSettings(connection=mocked_connection)
        assert isinstance(platform_component_settings, PlatformComponentSettings)
        assert platform_component_settings.collection_name == "platform_component_settings"

    def test_platform_component_settings_create(self, mocked_platform_component_settings: PlatformComponentSettings):
        """test the creation of a new data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_component_settings.create(data=sample_component_model_data)

    @patch.object(
        Model,
        "create",
        return_value=sample_result_create_data,
    )
    def test_platform_component_settings_create_settings_into_a_bus(
        self, patched_model: MagicMock, mocked_platform_component_settings: PlatformComponentSettings
    ):
        """test the creation of a new platform buses settings model into a bus"""
        response = mocked_platform_component_settings.create_settings(
            platform_component_settings=sample_component_model_data,
            platform_bus_settings_id=PLATFORM_BUS_SETTINGS_ID,
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_model.assert_called_with(
            data=sample_component_model_data,
            path=f"{mocked_platform_component_settings.collection_name}?platform_bus_settings_id={PLATFORM_BUS_SETTINGS_ID}",
        )
        patched_model.assert_called_once()

    @patch.object(
        Model,
        "create",
        return_value=sample_result_create_data,
    )
    def test_platform_component_settings_create_settings_into_another_component(
        self, patched_model: MagicMock, mocked_platform_component_settings: PlatformComponentSettings
    ):
        """test the creation of a new platform buses settings model into another component."""
        response = mocked_platform_component_settings.create_settings(
            platform_component_settings=sample_component_model_data,
            platform_component_parent_settings_id=PLATFORM_PARENT_COMPONENT_SETTINGS_ID,
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_model.assert_called_with(
            data=sample_component_model_data,
            path=f"{mocked_platform_component_settings.collection_name}?platform_component_parent_settings_id={PLATFORM_PARENT_COMPONENT_SETTINGS_ID}",
        )
        patched_model.assert_called_once()

    def test_platform_settings_list_elements(self, mocked_platform_component_settings: PlatformComponentSettings):
        """test listing elements of a data model"""
        with pytest.raises(NotImplementedError):
            mocked_platform_component_settings.list_elements()
