# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" global configuration settings """
import enum
import logging
import os
from typing import Literal, Union

from qiboconnection import __version__  # pylint: disable=cyclic-import

logger = logging.getLogger(__name__)


if "QUANTUM_SERVICE_URL" not in os.environ:
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
    LAMBDA = "lambda"


class Environment:
    """Execution Environment"""

    def __init__(self, environment_type: Union[EnvironmentType | None] = None):
        if "QUANTUM_SERVICE_URL" in os.environ:
            self._environment_type = EnvironmentType.LAMBDA
            self.quantum_service_url = os.environ["QUANTUM_SERVICE_URL"]
            self._audience_url = os.environ.get("AUDIENCE_URL", self.quantum_service_url)
        else:
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
    ) -> Union[
        Literal[EnvironmentType.LOCAL],
        Literal[EnvironmentType.STAGING],
        Literal[EnvironmentType.DEVELOPMENT],
        Literal[EnvironmentType.LAMBDA],
    ]:
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
