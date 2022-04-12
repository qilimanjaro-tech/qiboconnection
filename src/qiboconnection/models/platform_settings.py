""" Platform Settings CRUD operations """

from dataclasses import dataclass
from pathlib import Path

from qiboconnection.models.model import Model
from qiboconnection.models.platform_schema import PlatformSchema


@dataclass
class PlatformSettings(Model):
    """Platform Settings CRUD operations"""

    NAME = "platform_settings"
    platform_schema = PlatformSchema()

    def create(self, platform_schema_id: int, platform_settings: dict) -> dict:
        """Creates new Platform Settings from the given settings dictionary
        Args:
            platform_schema_id (int): platform unique identifier
            platform_settings (dict): dictionary containing the data.
        Returns:
            dict: returning the created dictionary data with its unique identifier
        """
        platform_settings_id = self._get_new_platform_settings_id(platform_schema_id=platform_schema_id)
        path = str(
            self._get_platform_settings_file_path(
                platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
            )
        )

        data = {"id": platform_settings_id} | platform_settings

        return super()._create(path=path, data=data)

    def read(self, platform_schema_id: int, platform_settings_id: int) -> dict:
        """Load a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """
        return super()._read(
            path=str(
                self._get_platform_settings_file_path(
                    platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
                )
            )
        )

    def update(self, platform_schema_id: int, platform_settings_id: int, platform_settings: dict) -> dict:
        """Updates a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier
            platform_settings (dict): dictionary containing the data. It should be all platform settings data without the id

        Returns:
            dict: returning platform settings
        """
        path = str(
            self._get_platform_settings_file_path(
                platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
            )
        )

        data = {"id": platform_settings_id} | platform_settings

        return super()._update(path=path, data=data)

    def delete(self, platform_schema_id: int, platform_settings_id: int) -> None:
        """Deletes a Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        """
        super()._delete(
            path=str(
                self._get_platform_settings_file_path(
                    platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
                )
            )
        )

    def check_platform_settings_exists(self, platform_schema_id: int, platform_settings_id: int) -> None:
        """Checks if the given platform exists

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        """
        # !!! TODO: use the remote connection
        exists = self._get_platform_settings_file_path(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        ).exists()
        if not exists:
            raise ValueError(f"Platform settings with id={platform_settings_id} does not exist.")

    def _get_new_platform_settings_id(self, platform_schema_id: int) -> int:
        """Returns a new platform_settings unique identifier

        Args:
            platform_schema_id (int): Platform unique identifier

        Returns:
            int: platform_settings unique identifier
        """
        # !!! TODO: use the remote connection
        platform_path = self.platform_schema.platform_schema_base_path / self.platform_schema.get_platform_name(
            platform_schema_id=platform_schema_id
        )
        number_items = len(list(platform_path.iterdir()))
        return number_items + 1

    def _get_platform_settings_file_path(self, platform_schema_id: int, platform_settings_id: int) -> Path:
        """returns the platform settings file path

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            Path: platform settings file path
        """
        return (
            self.platform_schema.platform_schema_base_path
            / self.platform_schema.get_platform_name(platform_schema_id=platform_schema_id)
            / f"{self.NAME}_{platform_settings_id}.yml"
        )
