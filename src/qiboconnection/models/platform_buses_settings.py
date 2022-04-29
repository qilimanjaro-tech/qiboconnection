""" Platform Buses Settings CRUD operations """

from dataclasses import dataclass
from typing import List

from qiboconnection.models.model import Model


@dataclass
class PlatformBusesSettings(Model):
    """Platform Buses Settings CRUD operations"""

    collection_name = "platform_buses_settings"

    def create_settings(self, platform_schema_settings_id: int, platform_buses_settings: dict) -> dict:
        """Create a new Platform buses settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform schema settings unique identifier
            platform_buses_settings (dict): Platform buses Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform buses settings with its unique identifier'
        """
        return super().create(
            data=platform_buses_settings,
            path=f"{self.collection_name}?platform_schema_settings_id={platform_schema_settings_id}",
        )

    def delete_settings(self, platform_schema_settings_id: int, platform_buses_settings_id: int) -> None:
        """Deletes a Platform buses Settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform schema settings unique identifier
            platform_buses_settings_id (int): Platform buses settings unique identifier

        """
        super().delete(
            path=f"{self.collection_name}/{platform_buses_settings_id}"
            + f"?platform_schema_settings_id={platform_schema_settings_id}",
        )

    def list_elements(self) -> List[dict]:
        raise NotImplementedError
