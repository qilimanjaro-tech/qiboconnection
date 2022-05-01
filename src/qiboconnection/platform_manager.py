""" Platform module to manage all settings from a platform """

from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import List

from qiboconnection.connection import Connection
from qiboconnection.models import (
    PlatformBusSettings,
    PlatformComponentSettings,
    PlatformSchemaSettings,
    PlatformSettings,
)


@dataclass
class PlatformManager(ABC):
    """Orchestrates all Platform necessary functions"""

    connection: InitVar[Connection]
    platform_settings: PlatformSettings = field(init=False)
    platform_schema_settings: PlatformSchemaSettings = field(init=False)
    platform_bus_settings: PlatformBusSettings = field(init=False)
    platform_component_settings: PlatformComponentSettings = field(init=False)

    def __post_init__(self, connection: Connection):
        self.platform_settings = PlatformSettings(connection=connection)
        self.platform_schema_settings = PlatformSchemaSettings(connection=connection)
        self.platform_bus_settings = PlatformBusSettings(connection=connection)
        self.platform_component_settings = PlatformComponentSettings(connection=connection)

    def load_all_platform_settings(self, platform_settings_id: int) -> dict:
        """Loads the complete platform settings including each component's settings

        Args:
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning the complete platform settings
        """

        return self.platform_settings.read_all_settings(platform_settings_id=platform_settings_id)

    def create_platform_settings(self, platform_settings: dict) -> dict:
        """Create a new Platform settings using a remote connection

        Args:
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection


        Returns:
            dict: returning platform with its unique identifier
        """

        return self.platform_settings.create(data=platform_settings)

    def read_platform_settings(self, platform_settings_id: int) -> dict:
        """Get Platform Settings using a remote connection

        Args:
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """

        return self.platform_settings.read(model_id=platform_settings_id)

    def update_platform_settings(self, platform_settings_id: int, platform_settings: dict) -> dict:
        """Updates a Platform Settings using a remote connection

        Args:
            platform_settings_id (int): Platform unique identifier
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform settings with its unique identifier
        """

        return self.platform_settings.update(model_id=platform_settings_id, data=platform_settings)

    def delete_platform_settings(self, platform_settings_id: int) -> None:
        """Delete Platform Settings using a remote connection

        Args:
            platform_settings_id (int): Platform Settings unique identifier

        """

        self.platform_settings.delete(model_id=platform_settings_id)

    def list_platform_settings(self) -> List[dict]:
        """List all platform settings in the system

        Returns:
            List[dict]: List of platform settings
        """

        return self.platform_settings.list_elements()

    def create_platform_schema_settings(self, platform_settings_id: int, platform_schema_settings: dict) -> dict:
        """Create a new Platform schema settings using a remote connection

        Args:
            platform_settings_id (int): Platform settings unique identifier
            platform_schema_settings (dict): Platform schema Settings as a dictionary to be sent to the remote connection


        Returns:
            dict: returning platform schema with its unique identifier
        """

        return self.platform_schema_settings.create_settings(
            platform_settings_id=platform_settings_id, platform_schema_settings=platform_schema_settings
        )

    def read_platform_schema_settings(self, platform_schema_settings_id: int) -> dict:
        """Get Platform Schema Settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform Schema Settings unique identifier

        Returns:
            dict: returning platform schema settings
        """

        return self.platform_schema_settings.read(model_id=platform_schema_settings_id)

    def update_platform_schema_settings(self, platform_schema_settings_id: int, platform_schema_settings: dict) -> dict:
        """Updates a Platform schema Settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform unique identifier
            platform_schema_settings (dict): Platform schema Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform schema _settings with its unique identifier
        """

        return self.platform_schema_settings.update(model_id=platform_schema_settings_id, data=platform_schema_settings)

    def delete_platform_schema_settings(self, platform_schema_settings_id: int) -> None:
        """Delete Platform Schema Settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform Schema Settings unique identifier

        """

        self.platform_schema_settings.delete(model_id=platform_schema_settings_id)

    def create_platform_bus_settings(self, platform_schema_settings_id: int, platform_bus_settings: dict) -> dict:
        """Create a new Platform buses settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform schema settings unique identifier
            platform_bus_settings (dict): Platform buses Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform buses settings with its unique identifier
        """

        return self.platform_bus_settings.create_settings(
            platform_schema_settings_id=platform_schema_settings_id, platform_bus_settings=platform_bus_settings
        )

    def read_platform_bus_settings(self, platform_bus_settings_id: int) -> dict:
        """Load a Platform buses Settings using a remote connection

        Args:
            platform_bus_settings_id (int): Platform buses settings unique identifier

        Returns:
            dict: returning platform buses settings with its unique identifier
        """

        return self.platform_bus_settings.read(model_id=platform_bus_settings_id)

    def update_platform_bus_settings(self, platform_bus_settings_id: int, platform_bus_settings: dict) -> dict:
        """Updates a Platform buses Settings using a remote connection

        Args:
            platform_bus_settings_id (int): Platform buses settings unique identifier
            platform_bus_settings (dict): Platform schema Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform schema _settings with its unique identifier
        """

        return self.platform_bus_settings.update(model_id=platform_bus_settings_id, data=platform_bus_settings)

    def delete_platform_bus_settings(self, platform_bus_settings_id: int) -> None:
        """Deletes a Platform buses Settings using a remote connection

        Args:
            platform_schema_settings_id (int): Platform schema settings unique identifier
            platform_bus_settings_id (int): Platform buses settings unique identifier

        """

        self.platform_bus_settings.delete(model_id=platform_bus_settings_id)

    def create_platform_component_settings(
        self,
        platform_component_settings: dict,
        platform_bus_settings_id: int | None = None,
        platform_component_parent_settings_id: int | None = None,
    ) -> dict:
        """Create a new Platform component Settings associated to a Platform using a remote connection

        Args:
            platform_component_settings (dict): Platform component Settings as a dictionary to be sent to
                                                the remote connection
            platform_bus_settings_id (int | None): Platform buses settings unique identifier only defined
                                                     when the component parent is a bus component
            platform_component_parent_settings_id (int | None): Platform Component Settings ID to to link the
                                                         new platform component settings
                                                         or None if it is not linked to any other platform
                                                        component settings.

        Returns:
            dict: returning platform component settings with its unique identifier
        """

        return self.platform_component_settings.create_settings(
            platform_component_settings=platform_component_settings,
            platform_bus_settings_id=platform_bus_settings_id,
            platform_component_parent_settings_id=platform_component_parent_settings_id,
        )

    def read_platform_component_settings(self, platform_component_settings_id: int) -> dict:
        """Load a new Platform component Settings using a remote connection

        Args:
            platform_component_settings_id (int): Platform component Settings unique identifier

        Returns:
            dict: returning platform component settings
        """

        return self.platform_component_settings.read(model_id=platform_component_settings_id)

    def update_platform_component_settings(
        self, platform_component_settings_id: int, platform_component_settings: dict
    ) -> dict:
        """Updates a new Platform component Settings using a remote connection

        Args:
            platform_component_settings_id (int): Platform Settings unique identifier
            platform_component_settings (dict): dictionary containing the data


        Returns:
            dict: returning platform settings
        """

        return self.platform_component_settings.update(
            model_id=platform_component_settings_id, data=platform_component_settings
        )

    def delete_platform_component_settings(self, platform_component_settings_id: int) -> None:
        """Deletes a Platform Component Settings using a remote connection

        Args:
            platform_component_settings_id (int): Platform component settings unique identifier
        """

        self.platform_component_settings.delete(model_id=platform_component_settings_id)
