""" global configuration settings """
import enum
import logging
import os
from typing import Literal, Union

from qiboconnection import __version__

# Logging level from 0 (NOT SET) to 50 (critical) (see https://docs.python.org/3/library/logging.html#logging-levels)
QIBO_CLIENT_LOG_LEVEL = int(os.environ.get("QIBO_CLIENT_LOG_LEVEL", 20))

# Configuration for logging mechanism


class CustomHandler(logging.StreamHandler):
    """Custom handler for logging algorithm."""

    def format(self, record):
        """Format the record with specific format."""
        fmt = f"[qibo-connection] {__version__}|%(levelname)s|%(asctime)s]: %(message)s"
        return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S").format(record)


# allocate logger object
logger = logging.getLogger(__name__)
logger.setLevel(QIBO_CLIENT_LOG_LEVEL)
logger.addHandler(CustomHandler())


QUANTUM_SERVICE_URL = {
    "local": "http://localhost:8080",
    "docker_local": "http://nginx:8080",
    "staging": "https://qilimanjaroqaas.ddns.net:8080",
    "development": "https://qilimanjarodev.ddns.net:8080",
}


class EnvironmentType(str, enum.Enum):
    """Environment Type

    Args:
        enum (str): Available environment types:
            * local
            * staging
    """

    LOCAL = "local"
    STAGING = "staging"
    DEVELOPMENT = "development"


class Environment:
    """Execution Environment"""

    def __init__(self, environment_type: EnvironmentType):
        if environment_type not in [
            EnvironmentType.LOCAL,
            EnvironmentType.STAGING,
            EnvironmentType.DEVELOPMENT,
        ]:
            raise ValueError("Environment Type MUST be 'local', 'staging' or 'development'")
        if environment_type == EnvironmentType.LOCAL:
            self._environment_type = EnvironmentType.LOCAL
            self.quantum_service_url = QUANTUM_SERVICE_URL["local"]
            self._audience_url = QUANTUM_SERVICE_URL["docker_local"]
        if environment_type == EnvironmentType.STAGING:
            self._environment_type = EnvironmentType.STAGING
            self.quantum_service_url = QUANTUM_SERVICE_URL["staging"]
            self._audience_url = QUANTUM_SERVICE_URL["staging"]
        if environment_type == EnvironmentType.DEVELOPMENT:
            self._environment_type = EnvironmentType.DEVELOPMENT
            self.quantum_service_url = QUANTUM_SERVICE_URL["development"]
            self._audience_url = QUANTUM_SERVICE_URL["development"]

    @property
    def qibo_quantum_service_url(self) -> str:
        """returns quantum service url

        Returns:
            str: quantum service url
        """
        return self.quantum_service_url

    @property
    def audience_url(self) -> str:
        """returns the audience url

        Returns:
            str: audience url
        """
        return self._audience_url

    @property
    def environment_type(
        self,
    ) -> Union[Literal[EnvironmentType.LOCAL], Literal[EnvironmentType.STAGING], Literal[EnvironmentType.DEVELOPMENT]]:
        """Returns the environment_type

        Returns:
            Union[Literal[EnvironmentType.LOCAL], Literal[EnvironmentType.STAGING]]: environment type
        """
        return self._environment_type


def get_environment() -> Environment:
    """Return environment corresponding to QIBOCONNECTION_ENVIRONMENT env variable

    Returns:
        Environment: environment"""
    return Environment(environment_type=EnvironmentType(os.environ.get("QIBOCONNECTION_ENVIRONMENT", "staging")))
