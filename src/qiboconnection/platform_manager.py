""" Platform module to manage all settings from a platform """

from abc import ABC
from typing import List

from qiboconnection.middleware.platform_schema import check_platform_schema_exists
from qiboconnection.middleware.platform_settings import check_platform_settings_exists
from qiboconnection.models import PlatformSchema, PlatformSettings


class PlatformManager(ABC):
    """Orchestrates all Platform necessary functions"""

    def create_platform_schema(self) -> dict:
        """Create a new Platform schema using a remote connection

        Returns:
            dict: returning platform schema with its unique identifier
        """

        return PlatformSchema().create()

    def list_platform_schemas(self) -> List[dict]:
        """List all platform schemas in the system

        Returns:
            List[dict]: List of platform dictionaries
        """

        return PlatformSchema().list_platform_schemas()

    @check_platform_schema_exists
    def create_platform_settings(self, platform_schema_id: int, platform_settings: dict) -> dict:
        """Create a new Platform Settings associated to a Platform using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform settings with its unique identifier
        """

        return PlatformSettings().create(platform_schema_id=platform_schema_id, platform_settings=platform_settings)

    @check_platform_schema_exists
    @check_platform_settings_exists
    def read_platform_settings(self, platform_schema_id: int, platform_settings_id: int) -> dict:
        """Load a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """

        return PlatformSettings().read(platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id)

    @check_platform_schema_exists
    @check_platform_settings_exists
    def update_platform_settings(
        self, platform_schema_id: int, platform_settings_id: int, platform_settings: dict
    ) -> dict:
        """Updates a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier
            platform_settings (dict): dictionary containing the data. It should be all platform settings data without the id

        Returns:
            dict: returning platform settings
        """

        return PlatformSettings().update(
            platform_schema_id=platform_schema_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings,
        )

    @check_platform_schema_exists
    @check_platform_settings_exists
    def delete_platform_settings(self, platform_schema_id: int, platform_settings_id: int) -> None:
        """Deletes a Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """

        PlatformSettings().delete(platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id)
