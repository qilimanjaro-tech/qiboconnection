""" Platform Settings CRUD operations """

from dataclasses import dataclass

from qiboconnection.models.model import Model
from qiboconnection.models.platform import Platform


@dataclass
class PlatformSettings(Model):
    """Platform Settings CRUD operations"""

    NAME = "platform_settings"
    platform = Platform()

    def create(self, platform_id: int, platform_settings: dict) -> dict:
        """Creates new Platform Settings from the given settings dictionary
        Args:
            platform_id (int): platform unique identifier
            platform_settings (dict): dictionary containing the data.
        Returns:
            dict: returning the created dictionary data with its unique identifier
        """
        platform_settings_id = self._get_new_platform_settings_id(platform_id=platform_id)
        path = str(
            self.platform.platform_base_path
            / self.platform.get_platform_name(platform_id=platform_id)
            / f"{self.NAME}_{platform_settings_id}.yml"
        )

        result_data = super()._create(path=path, data=platform_settings)

        return {"id": platform_settings_id} | result_data

    def _get_new_platform_settings_id(self, platform_id: int) -> int:
        """Returns a new platform_settings unique identifier

        Args:
            platform_id (int): Platform unique identifier

        Returns:
            int: platform_settings unique identifier
        """
        # !!! TODO: use the remote connection
        platform_path = self.platform.platform_base_path / self.platform.get_platform_name(platform_id=platform_id)
        number_items = len(list(platform_path.iterdir()))
        return number_items + 1
