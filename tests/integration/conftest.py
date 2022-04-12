""" Pytest configuration fixtures for each session """

from dataclasses import asdict
from typing import Tuple
from unittest.mock import patch

import pytest

from qiboconnection.api import API
from qiboconnection.models.platform import Platform
from qiboconnection.models.platform_settings import PlatformSettings
from qiboconnection.typings.connection import (
    ConnectionConfiguration,
    ConnectionEstablished,
)

from .data import platform_settings_sample


@pytest.fixture(scope="session", name="mocked_connection_configuration")
def fixture_create_mocked_connection_configuration() -> ConnectionConfiguration:
    """Create a mock connection configuration"""
    return ConnectionConfiguration(user_id=666, username="mocked_user", api_key="betterNOTaskMockedAPIKey")


@pytest.fixture(scope="session", name="mocked_connection_established")
def fixture_create_mocked_connection_established(
    mocked_connection_configuration: ConnectionConfiguration,
) -> ConnectionEstablished:
    """Create a mock connection configuration"""
    return ConnectionEstablished(
        **asdict(mocked_connection_configuration),
        authorisation_access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3O"
        + "DkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        api_path="/api/v1",
    )


@pytest.fixture(scope="session", name="mocked_api")
def fixture_create_mocked_api_connection(mocked_connection_established: ConnectionEstablished) -> API:
    """Create a mocked api connection

    Returns:
        API: API mocked connection
    """
    with patch(
        "qiboconnection.connection.load_config_file_to_disk",
        autospec=True,
        return_value=mocked_connection_established,
    ) as mock_config:
        api = API()
        mock_config.assert_called()
        return api


@pytest.fixture(scope="session", name="platform")
def fixture_platform() -> dict:
    """Create a platform as a fixture"""
    return Platform().create()


@pytest.fixture(scope="session", name="platform_id_settings_id")
def fixture_platform_settings(platform: dict) -> Tuple[int, int]:
    """Create a new platform settings as a fixture"""
    platform_settings = PlatformSettings().create(
        platform_id=platform["id"], platform_settings=platform_settings_sample
    )
    return platform["id"], platform_settings["id"]
