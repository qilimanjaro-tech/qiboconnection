""" Platform CRUD operations """

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from qiboconnection.models.model import Model


@dataclass
class Platform(Model):
    """Platform CRUD operations"""

    NAME = "platform"
    platform_base_path: Path = field(init=False)

    def __post_init__(self):
        """Initialize the platform data folder"""
        self.platform_base_path = Path(__file__).parent.parent / self.DATA_FOLDER
        if not self.platform_base_path.exists():
            self.platform_base_path.mkdir()

    def create(self) -> dict:
        """Creates new Platform

        Returns:
            dict: returning the created dictionary data with its unique identifier
        """
        platform_id = self._get_new_platform_id()
        platform_path = self.platform_base_path / f"{self.NAME}_{platform_id}"
        platform_path.mkdir()
        return {"id": platform_id, "location": str(platform_path)}

    def list_platforms(self) -> List[dict]:
        """List all platforms in the system

        Returns:
            List[dict]: List of platform dictionaries
        """
        # !!! TODO: use the remote connection
        platforms_path = self.platform_base_path.iterdir()
        return [
            {
                "id": self._get_platform_id_from_platform_path(platform_path=platform_path),
                "location": str(platform_path),
            }
            for platform_path in platforms_path
        ]

    def get_platform_name(self, platform_id: int) -> str:
        """Returns the platform name from the given platform ID

        Args:
            platform_id (int): Platform unique identifier

        Returns:
            str: platform name
        """
        # !!! TODO: use the remote connection
        return f"{self.NAME}_{platform_id}"

    def check_platform_exists(self, platform_id: int) -> None:
        """Checks if the given platform exists

        Args:
            platform_id (int): platform unique identifier
        """
        # !!! TODO: use the remote connection
        exists = (self.platform_base_path / self.get_platform_name(platform_id=platform_id)).exists()
        if not exists:
            raise ValueError(f"Platform with id={platform_id} does not exist.")

    def _get_new_platform_id(self) -> int:
        """Returns a new platform unique identifier

        Returns:
            int: platform unique identifier
        """
        # !!! TODO: use the remote connection
        number_items = len(list(self.platform_base_path.iterdir()))
        return number_items + 1

    def _get_platform_id_from_platform_path(self, platform_path: Path) -> int:
        """Get platform_id from platform_path

        Args:
            platform_path (Path): Platform Path

        Returns:
            int: Platform ID
        """
        platform_path_str = str(platform_path)
        if f"{self.NAME}_" not in platform_path_str:
            raise ValueError(f"path does not contain {self.NAME}_")
        return int(platform_path_str.rsplit("_", maxsplit=1)[-1])
