import os

from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration

from .utils import UserRole


class MissingCredentialsException(ValueError):
    pass


# GLOBALS
MAX_SLACK_LENGTH = os.getenv("MAX_SLACK_LENGTH", "2800")
TEST_MESSAGE_SLACK_CHANNEL_ID = os.getenv("TEST_MESSAGE_SLACK_CHANNEL_ID", "3")
TEST_FILE_SLACK_CHANNEL_ID = os.getenv("TEST_FILE_SLACK_CHANNEL_ID", "4")
PYTEST_VALID_CHARACTERS = [".", "F", "s", "x"]
PYTEST_SKIP_CHARACTERS = ["s"]
PYTEST_FAILURE_CHARACTERS = ["F"]


def get_logging_conf(role: UserRole = UserRole.ADMIN) -> ConnectionConfiguration:
    """Build a ConnectionConfiguration object from the keys defined in environment

    Args:
        role (UserRoles): admin, bsc_user or qilimanjaro_user

    Raises:
        MissingCredentialsException: missing or wrong credentials

    Returns:
        ConnectionConfiguration: instance with credentials for creating API instance
    """

    if role == UserRole.ADMIN:
        public_login_username = os.getenv("PUBLIC_LOGIN_ADMIN_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_ADMIN_KEY")

    elif role == UserRole.BSC:
        public_login_username = os.getenv("PUBLIC_LOGIN_BSC_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_BSC_KEY")

    elif role == UserRole.QILI:
        public_login_username = os.getenv("PUBLIC_LOGIN_QILI_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_QILI_KEY")

    elif role == UserRole.MACHINE:
        public_login_username = os.getenv("PUBLIC_LOGIN_MACHINE_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_MACHINE_KEY")

    # previous try/except was not catching the error
    if public_login_username is None or public_login_key is None:
        raise MissingCredentialsException(
            "Login failed. Credentials were not provided in the environment or are not valid. Recall you need to define a environment variables for every user role."
        )

    return ConnectionConfiguration(username=public_login_username, api_key=public_login_key)


def get_api(logging_conf: ConnectionConfiguration) -> API:
    """Returns API instance given a ConnectionConfiguration instance

    Args:
        logging_conf: login credentials

    Returns:
        API: api usable api instance
    """
    return API(configuration=logging_conf)
