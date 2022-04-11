""" Platform module to manage all settings from a platform """

from abc import ABC

from qiboconnection.middleware.platform import check_platform_exists
from qiboconnection.models import Platform, PlatformSettings


class PlatformManager(ABC):
    """Orchestrates all Platform necessary functions"""

    def create_platform(self) -> dict:
        """Create a new Platform using a remote connection

        Returns:
            dict: returning platform with its unique identifier
        """

        return Platform().create()

    @check_platform_exists
    def create_platform_settings(self, platform_id: int, platform_settings: dict) -> dict:
        """Create a new Platform Settings associated to a Platform using a remote connection

        Args:
            platform_id (int): Platform unique identifier
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform settings with its unique identifier
        """

        return PlatformSettings().create(platform_id=platform_id, platform_settings=platform_settings)
