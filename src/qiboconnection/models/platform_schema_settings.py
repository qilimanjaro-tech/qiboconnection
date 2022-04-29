""" Platform Schema Settings CRUD operations """

from dataclasses import dataclass

from qiboconnection.models.model import Model


@dataclass
class PlatformSchemaSettings(Model):
    """Platform Schema Settings CRUD operations"""

    collection_name = "platform_schema_settings"
