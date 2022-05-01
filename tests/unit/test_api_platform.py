""" Tests methods for API platform settings calls """

from typing import List, cast
from unittest.mock import MagicMock, patch

from qiboconnection.api import API
from qiboconnection.connection import Connection

from ..data import (
    sample_all_platform_settings,
    sample_bus_model_data,
    sample_bus_update_model_data,
    sample_component_model_data,
    sample_component_update_model_data,
    sample_multi_page_platform_settings_items,
    sample_multi_platform_settings_first_page_paginated_data,
    sample_multi_platform_settings_second_page_paginated_data,
    sample_one_page_platform_settings_paginated_data,
    sample_platform_settings_model_data,
    sample_platform_settings_one_page_items,
    sample_platform_settings_updated_model_data,
    sample_schema_model_data,
    sample_schema_update_model_data,
)

PLATFORM_SETTINGS_ID = 15
PLATFORM_SCHEMA_SETTINGS_ID = 12
PLATFORM_BUS_SETTINGS_ID = 11
PLATFORM_COMPONENT_SETTINGS_ID = 13
PLATFORM_PARENT_COMPONENT_SETTINGS_ID = 1

sample_result_create_platform_settings = {"id_": PLATFORM_SETTINGS_ID} | sample_platform_settings_model_data
sample_result_update_platform_settings = {"id_": PLATFORM_SETTINGS_ID} | sample_platform_settings_updated_model_data
sample_result_create_platform_schema_settings = {"id_": PLATFORM_SETTINGS_ID} | sample_schema_model_data
sample_result_update_platform_schema_settings = {"id_": PLATFORM_SETTINGS_ID} | sample_schema_update_model_data
sample_result_create_platform_bus_settings = {"id_": PLATFORM_BUS_SETTINGS_ID} | sample_bus_model_data
sample_result_update_platform_bus_settings = {"id_": PLATFORM_BUS_SETTINGS_ID} | sample_bus_update_model_data
sample_result_create_platform_component_settings = {"id_": PLATFORM_COMPONENT_SETTINGS_ID} | sample_component_model_data
sample_result_update_platform_component_settings = {
    "id_": PLATFORM_COMPONENT_SETTINGS_ID
} | sample_component_update_model_data


class TestAPIPlatformSettings:
    """Tests methods for API platform settings calls"""

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_all_platform_settings, 200),
    )
    def test_load_all_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """load all platform settings"""
        response = mocked_api.load_all_platform_settings(
            platform_settings_id=cast(int, sample_all_platform_settings["platform"]["id_"])
        )
        assert isinstance(response, dict)
        assert response == sample_all_platform_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_platform_settings, 201),
    )
    def test_create_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """create a new platform settings"""
        response = mocked_api.create_platform_settings(platform_settings=sample_platform_settings_model_data)
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_platform_settings, 200),
    )
    def test_load_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Gets a specific platform settings"""
        response = mocked_api.load_platform_settings(platform_settings_id=PLATFORM_SETTINGS_ID)
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_platform_settings, 201),
    )
    def test_update_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Update a platform settings"""
        response = mocked_api.update_platform_settings(
            platform_settings_id=PLATFORM_SETTINGS_ID, platform_settings=sample_platform_settings_updated_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_update_platform_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_delete_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Delete a specific platform settings"""
        mocked_api.delete_platform_settings(platform_settings_id=PLATFORM_SETTINGS_ID)
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
    )
    def test_list_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """test listing all platform settings"""
        patched_connection.side_effect = [(sample_one_page_platform_settings_paginated_data, 200)]
        response = mocked_api.list_platform_settings()
        assert isinstance(response, List)
        assert len(response) == 5
        assert response == sample_platform_settings_one_page_items
        assert patched_connection.call_count == 1

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
    )
    def test_list_platform_settings_multi_page(self, patched_connection: MagicMock, mocked_api: API):
        """test listing all platform settings"""
        patched_connection.side_effect = [
            (sample_multi_platform_settings_first_page_paginated_data, 200),
            (sample_multi_platform_settings_second_page_paginated_data, 200),
        ]
        response = mocked_api.list_platform_settings()
        assert isinstance(response, List)
        assert len(response) == 9
        assert response == sample_multi_page_platform_settings_items
        assert patched_connection.call_count == 2


class TestAPIPlatformSchemaSettings:
    """Tests methods for API platform schema settings calls"""

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_platform_settings, 201),
    )
    def test_create_platform_schema_settings(self, patched_connection: MagicMock, mocked_api: API):
        """create a new platform schema settings"""
        response = mocked_api.create_platform_schema_settings(
            platform_settings_id=PLATFORM_SETTINGS_ID, platform_schema_settings=sample_schema_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_platform_schema_settings, 200),
    )
    def test_load_platform_schema_settingss(self, patched_connection: MagicMock, mocked_api: API):
        """Gets a specific platform schema settings"""
        response = mocked_api.load_platform_schema_settings(platform_schema_settings_id=PLATFORM_SCHEMA_SETTINGS_ID)
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_schema_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_platform_schema_settings, 201),
    )
    def test_update_platform_schema_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Update a platform schema settings"""
        response = mocked_api.update_platform_schema_settings(
            platform_schema_settings_id=PLATFORM_SCHEMA_SETTINGS_ID,
            platform_schema_settings=sample_schema_update_model_data,
        )
        assert isinstance(response, dict)
        assert response == sample_result_update_platform_schema_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_delete_platform_schema_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Delete a specific platform schema settings"""
        mocked_api.delete_platform_schema_settings(platform_schema_settings_id=PLATFORM_SCHEMA_SETTINGS_ID)
        patched_connection.assert_called_once()


class TestAPIPlatformBusSettings:
    """Tests methods for API platform bus settings calls"""

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_platform_bus_settings, 201),
    )
    def test_create_platform_bus_settings(self, patched_connection: MagicMock, mocked_api: API):
        """create a new platform bus settings"""
        response = mocked_api.create_platform_bus_settings(
            platform_schema_settings_id=PLATFORM_SCHEMA_SETTINGS_ID, platform_bus_settings=sample_bus_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_bus_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_platform_bus_settings, 200),
    )
    def test_load_platform_bus_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Gets a specific platform bus settings"""
        response = mocked_api.load_platform_bus_settings(platform_bus_settings_id=PLATFORM_BUS_SETTINGS_ID)
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_bus_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_platform_bus_settings, 201),
    )
    def test_update_platform_bus_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Update a platform bus settings"""
        response = mocked_api.update_platform_bus_settings(
            platform_bus_settings_id=PLATFORM_BUS_SETTINGS_ID,
            platform_bus_settings=sample_bus_update_model_data,
        )
        assert isinstance(response, dict)
        assert response == sample_result_update_platform_bus_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_delete_platform_bus_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Delete a specific platform bus settings"""
        mocked_api.delete_platform_bus_settings(platform_bus_settings_id=PLATFORM_BUS_SETTINGS_ID)
        patched_connection.assert_called_once()


class TestAPIPlatformComponentSettings:
    """Tests methods for API platform component settings calls"""

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_platform_component_settings, 201),
    )
    def test_create_platform_component_settings_parent_bus(self, patched_connection: MagicMock, mocked_api: API):
        """create a new platform component settings with a bus as a parent"""
        response = mocked_api.create_platform_component_settings(
            platform_bus_settings_id=PLATFORM_BUS_SETTINGS_ID, platform_component_settings=sample_component_model_data
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_component_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_platform_component_settings, 201),
    )
    def test_create_platform_component_settings_parent_component(self, patched_connection: MagicMock, mocked_api: API):
        """create a new platform component settings with a component as a parent"""
        response = mocked_api.create_platform_component_settings(
            platform_component_parent_settings_id=PLATFORM_PARENT_COMPONENT_SETTINGS_ID,
            platform_component_settings=sample_component_model_data,
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_component_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_platform_component_settings, 200),
    )
    def test_load_platform_component_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Gets a specific platform component settings"""
        response = mocked_api.load_platform_component_settings(
            platform_component_settings_id=PLATFORM_COMPONENT_SETTINGS_ID
        )
        assert isinstance(response, dict)
        assert response == sample_result_create_platform_component_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_platform_component_settings, 201),
    )
    def test_update_platform_component_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Update a platform component settings"""
        response = mocked_api.update_platform_component_settings(
            platform_component_settings_id=PLATFORM_COMPONENT_SETTINGS_ID,
            platform_component_settings=sample_component_update_model_data,
        )
        assert isinstance(response, dict)
        assert response == sample_result_update_platform_component_settings
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_delete_platform_component_settings(self, patched_connection: MagicMock, mocked_api: API):
        """Delete a specific platform component settings"""
        mocked_api.delete_platform_component_settings(platform_component_settings_id=PLATFORM_COMPONENT_SETTINGS_ID)
        patched_connection.assert_called_once()
