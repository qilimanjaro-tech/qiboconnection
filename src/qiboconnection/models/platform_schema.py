""" Platform Schema CRUD operations """

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from qiboconnection.models.model import Model


@dataclass
class PlatformSchema(Model):
    """Platform Schema CRUD operations"""

    NAME = "platform-schema"
    platform_schema_base_path: Path = field(init=False)

    def __post_init__(self):
        """Initialize the platform schema data folder"""
        self.platform_schema_base_path = Path(__file__).parent.parent / self.DATA_FOLDER
        if not self.platform_schema_base_path.exists():
            self.platform_schema_base_path.mkdir()

    def create(self) -> dict:
        """Creates new Platform Schema

        Returns:
            dict: returning the created dictionary data with its unique identifier
        """
        platform_schema_id = self._get_new_platform_schema_id()
        platform_schema_path = self.platform_schema_base_path / f"{self.NAME}_{platform_schema_id}"
        platform_schema_path.mkdir()
        return {"id": platform_schema_id, "location": str(platform_schema_path)}

    def list_platform_schemas(self) -> List[dict]:
        """List all platform schemas in the system

        Returns:
            List[dict]: List of platform schemas dictionaries
        """
        # !!! TODO: use the remote connection
        platforms_path = self.platform_schema_base_path.iterdir()
        return [
            {
                "id": self._get_platform_schema_id_from_platform_schema_path(platform_schema_path=platform_schema_path),
                "location": str(platform_schema_path),
            }
            for platform_schema_path in platforms_path
        ]

    def get_platform_name(self, platform_schema_id: int) -> str:
        """Returns the platform name from the given platform ID

        Args:
            platform_schema_id (int): Platform unique identifier

        Returns:
            str: platform name
        """
        # !!! TODO: use the remote connection
        return f"{self.NAME}_{platform_schema_id}"

    def check_platform_schema_exists(self, platform_schema_id: int) -> None:
        """Checks if the given platform schema exists

        Args:
            platform_schema_id (int): platform unique identifier
        """
        # !!! TODO: use the remote connection
        exists = (
            self.platform_schema_base_path / self.get_platform_name(platform_schema_id=platform_schema_id)
        ).exists()
        if not exists:
            raise ValueError(f"Platform with id={platform_schema_id} does not exist.")

    def _get_new_platform_schema_id(self) -> int:
        """Returns a new platform unique identifier

        Returns:
            int: platform unique identifier
        """
        # !!! TODO: use the remote connection
        number_items = len(list(self.platform_schema_base_path.iterdir()))
        return number_items + 1

    def _get_platform_schema_id_from_platform_schema_path(self, platform_schema_path: Path) -> int:
        """Get platform_schema_id from platform_schema_path

        Args:
            platform_schema_path (Path): Platform Path

        Returns:
            int: Platform ID
        """
        platform_schema_path_str = str(platform_schema_path)
        if f"{self.NAME}_" not in platform_schema_path_str:
            raise ValueError(f"path does not contain {self.NAME}_")
        return int(platform_schema_path_str.rsplit("_", maxsplit=1)[-1])
