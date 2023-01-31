""" Web Responses class"""

from .devices import Devices
from .ping import Ping
from .responses_raw import ResponsesRaw
from .runcards import Runcards
from .saved_experiments import SavedExperiments
from .users import Users


class WebResponses:
    """Class holding all the response-kind of data, for mocking our web calls"""

    ping = Ping()
    devices = Devices()
    saved_experiments = SavedExperiments()
    runcards = Runcards()
    users = Users()
    raw = ResponsesRaw()
