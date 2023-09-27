""" JobType enum """
from .str_enum import StrEnum


class JobType(StrEnum):
    """Job Type

    Args:
        enum (str): Accepted values are:
            * "circuit"
            * "experiment"
    """

    CIRCUIT = "circuit"
    EXPERIMENT = "experiment"
