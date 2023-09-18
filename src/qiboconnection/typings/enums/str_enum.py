""" StrEnum base class """
from enum import Enum


class StrEnum(str, Enum):
    """Associates a number to each entry. Unlike a normal enum, this is not used for indexing, and adding the '.value'
    to everywhere is still not needed.
    This int can be used for where a string is not suitable."""

    @property
    def to_int(self):
        """Returns the int associated to the str entry in the enum class. Order is important."""
        return list(self.__class__).index(self)
