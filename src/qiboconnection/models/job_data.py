""" Job Data Typing """

from dataclasses import dataclass
from inspect import signature

from qibo.models.circuit import Circuit

from qiboconnection.typings.enums import JobStatus, JobType


@dataclass(slots=True)
class JobData:
    """Data shown to the user when get_job() method is used. It includes job human-readable results and
    metadata.
    """

    status: str | JobStatus
    queue_position: int
    user_id: int | None
    device_id: int
    job_id: int
    job_type: str | JobType
    number_shots: int
    description: Circuit | dict
    result: dict | None

    @classmethod
    def from_kwargs(cls, **kwargs):
        # fetch the constructor's signature
        cls_fields = set(signature(cls).parameters)
        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        ret = cls(**native_args)

        # add the new ones by hand
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
        return ret
