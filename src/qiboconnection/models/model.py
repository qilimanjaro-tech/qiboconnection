""" Generic Model module with CRUD operations """

from abc import ABC
from pathlib import Path
from typing import cast

import yaml


class Model(ABC):
    """Class to manage CRUD operations with general structures
    that require data model Create, Read, Update, Delete operations
    """

    DATA_FOLDER = "data"

    def _create(self, path: str, data: dict) -> dict:
        """Dump data into its corresponding location.
        Args:
            path (str): path to the settings file
            data (dict): dictionary containing the data.
        Returns:
            dict: returning the created dictionary data
        """
        # !!! TODO: use the remote connection instead of local files
        with open(path, "w", encoding="utf-8") as file:
            yaml.dump(data=data, stream=file, sort_keys=False)
        return data

    def _read(self, path: str) -> dict:
        """Load data from a location into a dictionary data
        Args:
            path (str): file location path
        Returns:
            dict: data in a dictionary format
        """
        # !!! TODO: use the remote connection instead of local files
        with open(path, "r", encoding="utf-8") as file:
            return cast(dict, yaml.safe_load(stream=file))

    def _update(self, path: str, data: dict) -> dict:
        """Update data into its corresponding location.
        Args:
            path (str): path to the settings file
            data (dict): dictionary containing the data.
        Returns:
            dict: returning the updated dictionary data
        """
        # !!! TODO: use the remote connection instead of local files
        with open(path, "w", encoding="utf-8") as file:
            yaml.dump(data=data, stream=file, sort_keys=False)
        return data

    def _delete(self, path: str) -> None:
        """Deletes the data from its corresponding location.
        Args:
            path (str): path to the settings file
        """
        # !!! TODO: use the remote connection instead of local files
        Path(path).unlink()
