""" Job Data Typing """
# pylint: disable=too-many-instance-attributes
# pylint: disable=E1101
from qibo.models import Circuit

from qiboconnection.api_utils import deserialize_job_description, parse_job_responses_to_results
from qiboconnection.models.job_response import JobResponse


class JobData(JobResponse):
    """Data shown to the user when get_job() method is used. It includes job human-readable results and metadata."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.result = parse_job_responses_to_results(job_responses=[JobResponse.from_kwargs(**kwargs)])[0]
        self.description = deserialize_job_description(base64_description=self.description, job_type=self.job_type)

        if not isinstance(self.result, (dict, type(None))):
            raise ValueError("Job result needs to be a dict!")

        if not isinstance(self.description, (dict, type(None), Circuit)):
            raise ValueError("Job description needs to be a dict of a Qibo Circuit!")

    def __repr__(self):
        # Use dataclass-like formatting, excluding attributes starting with an underscore
        attributes = [
            f"{attr}={getattr(self, attr)!r}"
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__") and attr != "_abc_impl"
        ]
        return f"JobData({', '.join(attributes)})"
