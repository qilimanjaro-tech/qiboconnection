""" Platform Settings operations """

from dataclasses import dataclass
from typing import List

from qiboconnection.models.model import Model


@dataclass
class PlatformSettings(Model):
    """Platform Settings that contains all platform component settings"""

    collection_name = "platform_settings"

    def create(self, data: dict, path: str | None = None) -> dict:
        raise NotImplementedError

    def update(self, data: dict, model_id: int | None = None, path: str | None = None) -> dict:
        raise NotImplementedError

    def delete(self, model_id: int | None = None, path: str | None = None) -> None:
        raise NotImplementedError

    def list_elements(self) -> List[dict]:
        raise NotImplementedError
