""" Platform Schema Settings CRUD operations """

from dataclasses import dataclass
from typing import List

from qiboconnection.models.model import Model


@dataclass
class PlatformSchemaSettings(Model):
    """Platform Schema Settings CRUD operations"""

    collection_name = "platform_schema_settings"

    def create(self, data: dict, path: str | None = None) -> dict:
        raise NotImplementedError("Use 'create_settings' instead.")

    def create_settings(self, platform_settings_id: int, platform_schema_settings: dict) -> dict:
        """Create a new Platform Schema settings using a remote connection

        Args:
            platform_settings_id (int): Platform settings unique identifier
            platform_schema_settings (dict): Platform Schema Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform Schema settings with its unique identifier'
        """
        return super().create(
            data=platform_schema_settings,
            path=f"{self.collection_name}?platform_settings_id={platform_settings_id}",
        )

    def list_elements(self) -> List[dict]:
        raise NotImplementedError
