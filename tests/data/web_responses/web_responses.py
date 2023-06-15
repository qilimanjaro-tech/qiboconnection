""" Web Responses class"""

from .auth import Auth
from .devices import Devices
from .job_listing import JobResponse
from .ping import Ping
from .responses_raw import ResponsesRaw
from .runcards import Runcards
from .saved_experiments import SavedExperiments
from .users import Users


class WebResponses:
    """Class holding all the response-kind of data, for mocking our web calls. Note that each one corresponds to one endpoint of the API"""

    ping = Ping()
    devices = Devices()
    saved_experiments = SavedExperiments()
    runcards = Runcards()
    users = Users()
    auth = Auth()
    raw = ResponsesRaw()
    job_listing = JobResponse()
