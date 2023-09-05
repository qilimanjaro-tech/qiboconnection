""" LivePlotType enum """
from .str_enum import StrEnum


class LivePlotType(StrEnum):
    """
    Class for type
    """

    LINES = "LINES"
    SCATTER = "SCATTER"
    SCATTER3D = "SCATTER3D"
    HEATMAP = "HEATMAP"
