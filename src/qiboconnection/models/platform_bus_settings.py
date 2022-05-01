""" Platform Bus Settings CRUD operations """

from dataclasses import dataclass
from typing import List

from qiboconnection.models.model import Model


@dataclass
class PlatformBusSettings(Model):
    """Platform Bus Settings CRUD operations"""

    collection_name = "platform_bus_settings"

    def create(self, data: dict, path: str | None = None) -> dict:
        raise NotImplementedError("Use 'create_settings' instead.")

    def create_settings(self, platform_schema_settings_id: int, platform_bus_settings: dict) -> dict:
        """Create a new Platform bus settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform schema settings unique identifier
            platform_bus_settings (dict): Platform bus Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform bus settings with its unique identifier'
        """
        return super().create(
            data=platform_bus_settings,
            path=f"{self.collection_name}?platform_schema_settings_id={platform_schema_settings_id}",
        )

    def list_elements(self) -> List[dict]:
        raise NotImplementedError
