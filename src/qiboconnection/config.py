# config.py
# global configuration settings
import os
import logging
import enum
from typing import Literal, Union

# Logging level from 0 (all) to 4 (errors) (see https://docs.python.org/3/library/logging.html#logging-levels)
QIBO_CLIENT_LOG_LEVEL = int(os.environ.get("QIBO_CLIENT_LOG_LEVEL", 1))

# Configuration for logging mechanism


class CustomHandler(logging.StreamHandler):
    """Custom handler for logging algorithm."""

    def format(self, record):
        """Format the record with specific format."""
        from qiboconnection import __version__

        fmt = f"[qibo-connection] {__version__}|%(levelname)s|%(asctime)s]: %(message)s"
        return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S").format(record)


# allocate logger object
logger = logging.getLogger(__name__)
logger.setLevel(QIBO_CLIENT_LOG_LEVEL)
logger.addHandler(CustomHandler())


QUANTUM_SERVICE_URL = {
    "local": "http://localhost:8080",
    "docker_local": "http://nginx:8080",
    "staging": "https://qilimanjaro.ddns.net:8080",
}


class EnvironmentType(enum.Enum):
    local = "local"
    staging = "staging"


class Environment:
    def __init__(self, environment_type: EnvironmentType):
        if (
            environment_type != EnvironmentType.local and
            environment_type != EnvironmentType.staging
        ):
            raise ValueError(
                "Environment Type MUST be 'local', 'staging' or 'production'"
            )
        if environment_type == EnvironmentType.local:
            self._environment_type = EnvironmentType.local
            self.quantum_service_url = QUANTUM_SERVICE_URL["local"]
            self._audience_url = QUANTUM_SERVICE_URL["docker_local"]
        if environment_type == EnvironmentType.staging:
            self._environment_type = EnvironmentType.staging
            self.quantum_service_url = QUANTUM_SERVICE_URL["staging"]
            self._audience_url = QUANTUM_SERVICE_URL["staging"]

    @property
    def qibo_quantum_service_url(self) -> str:
        return self.quantum_service_url

    @property
    def audience_url(self) -> str:
        return self._audience_url

    @property
    def environment_type(
        self,
    ) -> Union[Literal[EnvironmentType.local], Literal[EnvironmentType.staging]]:
        return self._environment_type


environment = Environment(
    environment_type=EnvironmentType(os.environ.get("QIBO_ENVIRONMENT", "staging"))
)
QQS_URL = environment.qibo_quantum_service_url
AUDIENCE_URL = environment.audience_url
logger.debug(f"Qibo Quantum Service API SERVER URL: {QQS_URL}")
