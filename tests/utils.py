# Utils module for testing

import asyncio


def get_current_event_loop_or_create():
    """Gets current asyncio event loop or creates and sets a new one.
    Using `get_event_loop` should be enough as it has the logic for creating new loops,
    but tests complain about it when launching the suite from terminal."""

    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.new_event_loop()
