# Utils module for testing

import asyncio
import os
from typing import Dict, Union


def get_current_event_loop_or_create():
    """Gets current asyncio event loop or creates and sets a new one.
    Using `get_event_loop` should be enough as it has the logic for creating new loops,
    but tests complain about it when launching the suite from terminal."""

    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


def set_and_keep_values(
    values: Dict[str, str], my_dict: Union[Dict[str, str], os._Environ[str]] = os.environ
) -> Dict[str, str]:
    """Utility to set or remove values in a dictionary.

    The original values are return, so they can be set afterwards.
    Args:
        value: the values to be set. If the value is None, remove the key
        my_dict: the dictionary to set or remove the values
    Returns:
        dict: the original values in my_dict or None if that key did not exist
    """

    old_values = {}
    for key, value in values.items():
        old_values[key] = my_dict.get(key, None)
        if value is None:
            del my_dict[key]
        else:
            my_dict[key] = value

    return old_values
