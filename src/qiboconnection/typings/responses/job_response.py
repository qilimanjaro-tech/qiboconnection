""" JobResponse """
from dataclasses import dataclass, field
from inspect import signature

from ..requests import JobRequest


@dataclass
class JobResponse(JobRequest):
    """Full Job Response. Includes job results which may
    be weight a few GB.

    Attributes:
        user_id (int): User identifier
        device_id (int): Device identifier
        description (str): Description of the job
        job_id (int): Job identifier
        queue_position (int): Job queue position
        status (str): Status of the job
        result (str): Job result
    """

    job_id: int
    queue_position: int
    result: str
    status: str

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
