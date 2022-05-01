""" Tests methods for model calls """

from typing import List
from unittest.mock import MagicMock, patch

import pytest

from qiboconnection.connection import Connection
from qiboconnection.models.model import Model

from ..data import (
    sample_model_data,
    sample_model_updated_data,
    sample_multi_first_page_paginated_data,
    sample_multi_page_items,
    sample_multi_second_page_paginated_data,
    sample_result_create_data,
    sample_result_update_data,
)


@pytest.fixture(name="mocked_model")
def fixture_mocked_model(mocked_connection: Connection) -> Model:
    """Create a mocked Model

    Args:
        mocked_connection (Connection): Mocked Connection

    Returns:
        Model: Model class
    """
    model = Model(connection=mocked_connection)
    model.collection_name = "testing"
    return model


class TestModel:
    """Test methods for generic model calls"""

    path = "some-tests"

    def test_model_constructor(self, mocked_connection: Connection):
        """Test a new Model object"""
        model = Model(connection=mocked_connection)
        assert isinstance(model, Model)

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_data, 201),
    )
    def test_model_create_without_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the creation of a new data model without using path"""
        response = mocked_model.create(data=sample_model_data)
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_connection.assert_called_with(data=sample_model_data, path=mocked_model.collection_name)
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_post_auth_remote_api_call",
        return_value=(sample_result_create_data, 201),
    )
    def test_model_create_with_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the creation of a new data model with path"""
        response = mocked_model.create(data=sample_model_data, path=self.path)
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_connection.assert_called_with(data=sample_model_data, path=self.path)
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_data, 200),
    )
    def test_model_read_without_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the read of a data model without using path"""
        response = mocked_model.read(model_id=sample_result_create_data["id"])
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_connection.assert_called_with(path=f'{mocked_model.collection_name}/{sample_result_create_data["id"]}')
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_result_create_data, 200),
    )
    def test_model_read_with_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the read of a data model with path"""
        response = mocked_model.read(model_id=sample_result_create_data["id"], path=self.path)
        assert isinstance(response, dict)
        assert response == sample_result_create_data
        patched_connection.assert_called_with(path=f'{self.path}/{sample_result_create_data["id"]}')
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_data, 201),
    )
    def test_model_update_without_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the update of a data model without using path"""
        response = mocked_model.update(model_id=sample_result_update_data["id"], data=sample_model_updated_data)
        assert isinstance(response, dict)
        assert response == sample_result_update_data
        patched_connection.assert_called_with(
            path=f'{mocked_model.collection_name}/{sample_result_create_data["id"]}', data=sample_model_updated_data
        )
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_put_auth_remote_api_call",
        return_value=(sample_result_update_data, 201),
    )
    def test_model_update_with_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the update of a data model with path"""
        response = mocked_model.update(
            model_id=sample_result_update_data["id"], data=sample_model_updated_data, path=self.path
        )
        assert isinstance(response, dict)
        assert response == sample_result_update_data
        patched_connection.assert_called_with(
            path=f'{self.path}/{sample_result_create_data["id"]}', data=sample_model_updated_data
        )
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_model_delete_without_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the delete of a data model without using path"""
        response = mocked_model.delete(model_id=sample_result_create_data["id"])
        assert response is None
        patched_connection.assert_called_with(path=f'{mocked_model.collection_name}/{sample_result_create_data["id"]}')
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_delete_auth_remote_api_call",
        return_value=(None, 204),
    )
    def test_model_delete_with_path(self, patched_connection: MagicMock, mocked_model: Model):
        """test the delete of a data model with path"""
        response = mocked_model.delete(model_id=sample_result_create_data["id"], path=self.path)
        assert response is None
        patched_connection.assert_called_with(path=f'{self.path}/{sample_result_create_data["id"]}')
        patched_connection.assert_called_once()

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
    )
    def test_model_list_elements_one_page(self, patched_connection: MagicMock, mocked_model: Model):
        """test the creation of a new data model without using path"""
        patched_connection.side_effect = [
            (sample_multi_first_page_paginated_data, 200),
            (sample_multi_second_page_paginated_data, 200),
        ]
        response = mocked_model.list_elements()
        assert isinstance(response, List)
        assert len(response) == 4
        assert response == sample_multi_page_items
        assert patched_connection.call_count == 2
