"""Web Responses class"""

from .auth import Auth
from .devices import Devices
from .job import JobResponse
from .ping import Ping
from .responses_raw import ResponsesRaw
from .runcards import Runcards
from .users import Users


class WebResponses:
    """Class holding all the response-kind of data, for mocking our web calls. Note that each one corresponds to one endpoint of the API"""

    ping = Ping()
    devices = Devices()
    runcards = Runcards()
    users = Users()
    auth = Auth()
    raw = ResponsesRaw()
    job_response = JobResponse()
