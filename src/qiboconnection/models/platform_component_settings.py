""" Platform Component Settings CRUD operations """

from dataclasses import dataclass, field
from functools import partial
from typing import Callable, List

from qiboconnection.models.model import Model


@dataclass
class PlatformComponentSettings(Model):
    """Platform Component Settings CRUD operations"""

    collection_name = "platform_component_settings"
    _path: str = field(init=False)

    class SetPath:
        """Property used to check if both platform_buses_settings_id and platform_component_parent_settings_id
        are correctly defined and sets the path to call the remote API"""

        def __init__(self, method: Callable):
            self._method = method

        def __get__(self, obj, objtype):
            """Support instance methods."""
            return partial(self.__call__, obj)

        def __call__(self, ref: "PlatformComponentSettings", *args, **kwargs):
            """
            Args:
                method (Callable): Class method.

            Raises:
                AttributeError: If the instrument is not connected.
            """
            if "platform_buses_settings_id" not in kwargs or "platform_component_parent_settings_id" not in kwargs:
                raise AttributeError(
                    "Either 'platform_buses_settings_id' or 'platform_component_parent_settings_id' MUST be defined."
                )

            platform_buses_settings_id, platform_component_parent_settings_id = (
                kwargs["platform_buses_settings_id"],
                kwargs["platform_component_parent_settings_id"],
            )

            if platform_buses_settings_id is None and platform_component_parent_settings_id is None:
                raise AttributeError(
                    "Either 'platform_buses_settings_id' or 'platform_component_parent_settings_id' MUST be defined."
                )
            if platform_buses_settings_id is not None and platform_component_parent_settings_id is not None:
                raise AttributeError(
                    "Both 'platform_buses_settings_id' and 'platform_component_parent_settings_id' are defined. "
                    + "Just ONE of them MUST be defined."
                )
            ref._path = f"{ref.collection_name}"
            if "platform_component_settings_id" in kwargs:
                ref._path += f"/{kwargs['platform_component_settings_id']}"
            if platform_buses_settings_id is not None:
                ref._path += f"?platform_buses_settings_id={platform_buses_settings_id}"
            if platform_component_parent_settings_id is not None:
                ref._path += f"?platform_component_parent_settings_id={platform_component_parent_settings_id}"
            return self._method(ref, *args, **kwargs)

    @SetPath
    def create_settings(
        self,
        platform_component_settings: dict,
        platform_buses_settings_id: int | None = None,  # pylint: disable=unused-argument
        platform_component_parent_settings_id: int | None = None,  # pylint: disable=unused-argument
    ) -> dict:
        """Create a new Platform component Settings associated to a Platform using a remote connection

        Args:
            platform_component_settings (dict): Platform component Settings as a dictionary to be sent to
                                                the remote connection
            platform_buses_settings_id (int | None): Platform buses settings unique identifier only defined
                                                     when the component parent is a bus component
            platform_component_parent_settings_id (int | None): Platform Component Settings ID to to link the
                                                         new platform component settings
                                                         or None if it is not linked to any other platform
                                                        component settings.

        Returns:
            dict: returning platform component settings with its unique identifier
        """

        return super().create(data=platform_component_settings, path=self._path)

    @SetPath
    def delete_settings(
        self,
        platform_component_settings_id: int,  # pylint: disable=unused-argument
        platform_buses_settings_id: int | None = None,  # pylint: disable=unused-argument
        platform_component_parent_settings_id: int | None = None,  # pylint: disable=unused-argument
    ) -> None:
        """Deletes a Platform buses Settings using a remote connection

        Args:
            platform_component_settings_id (int): Platform component settings unique identifier
            platform_buses_settings_id (int | None): Platform buses settings unique identifier only defined
                                                     when the component parent is a bus component
            platform_component_parent_settings_id (int | None): Platform Component Settings ID to to link the
                                                         new platform component settings
                                                         or None if it is not linked to any other platform
                                                        component settings.

        """
        super().delete(path=self._path)

    def list_elements(self) -> List[dict]:
        raise NotImplementedError
