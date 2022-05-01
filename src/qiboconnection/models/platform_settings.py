""" Platform Settings operations """

from dataclasses import dataclass

from qiboconnection.models.model import Model

ALL_SETTINGS_PATH = "complete-settings"


@dataclass
class PlatformSettings(Model):
    """Platform Settings that contains all platform component settings"""

    collection_name = "platform_settings"

    def read_all_settings(self, platform_settings_id: int) -> dict:
        """Loads the complete platform settings including each component's settings

        Args:
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning the complete platform settings
        """
        return super().read(
            path=f"{self.collection_name}/{platform_settings_id}/{ALL_SETTINGS_PATH}",
        )
