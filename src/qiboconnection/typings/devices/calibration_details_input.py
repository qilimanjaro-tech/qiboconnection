""" Calibration Details Input Typing """
from dataclasses import dataclass


@dataclass(kw_only=True)
class CalibrationDetailsInput:
    """Calibration Details Input

    Attributes:
        elapsed_time (int | None): elapsed time
        t1 (int | None): last calibrated t1 time
        frequency (int | None): last calibrated frequency
    """

    elapsed_time: int | None = None
    t1: int | None = None  # pylint: disable=invalid-name
    frequency: int | None = None
