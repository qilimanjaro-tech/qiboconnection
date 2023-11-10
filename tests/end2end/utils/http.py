import os
import textwrap
from typing import TextIO

from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration

from .typings import UserRole


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


def _build_formatted_generic_message(message: str) -> dict:
    """
    Builds a generic message to be sent to slack
    Args:
        message: String we want to wrap in a formatted message

    Returns:
        dict: Object to be sent to slack
    """
    response_dict: dict = {"blocks": []}
    for portion in textwrap.wrap(text=message, width=int(MAX_SLACK_LENGTH)):
        response_dict["blocks"].append({"type": "section", "text": {"type": "mrkdwn", "text": f"{portion}"}})
    return response_dict


def _determine_results_emoji(summary: str):
    """Computes which emoji should we use to indicate tests results depending on the presence of failed and/or skipped
    tests
    Args:
        summary: text containing summary of the results of the tests

    Returns:
        str: emoji code understandable by slack
    """
    first_report_line = summary.split(" ")[0]

    if False in [test_result in PYTEST_VALID_CHARACTERS for test_result in first_report_line]:
        return ":warning:"
    if True in [test_result in PYTEST_FAILURE_CHARACTERS for test_result in first_report_line]:
        return ":red_circle:"
    if True in [test_result in PYTEST_SKIP_CHARACTERS for test_result in first_report_line]:
        return ":large_yellow_circle:"
    return ":large_green_circle:"


def _build_formatted_summary_message(summary: str) -> dict:
    """
    Builds a specific message to be sent to slack containing the summary of the results of the tests and an indicative
    emoji
    Args:
        summary: text containing summary of the results of the tests

    Returns:
        dict: Object to be sent to slack
    """
    emoji = _determine_results_emoji(summary)
    response_dict = {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"SUMMARY {emoji}:\n TEST run with results:"}}
        ]
    }
    for portion in textwrap.wrap(summary, int(MAX_SLACK_LENGTH)):
        response_dict["blocks"].append({"type": "section", "text": {"type": "mrkdwn", "text": f"{portion}"}})
    return response_dict


def send_slack_message(message: str, test_summary_message: bool = False):
    """Sends a message to slack. Depending on this message being the summary of some tests results or any other thing,
    it will be formatted differently.

    Args:
        message: text we want to send to slack
        test_summary_message: flag to tell whether to activate the 'summary of test results' formatting.

    Returns:

    """
    conf = get_logging_conf()
    api = get_api(conf)
    if test_summary_message:
        formatted_message = _build_formatted_summary_message(message)
    else:
        formatted_message = _build_formatted_generic_message(message)

    return api._connection.send_message(channel_id=int(TEST_MESSAGE_SLACK_CHANNEL_ID), message=formatted_message)


def send_slack_file(file: TextIO, filename: str):
    """Sends a file to slack.

    Args:
        file: File to send to slack
        filename: Filename to send the file with

    Returns:
        Response: server response

    """
    conf = get_logging_conf()
    api = get_api(conf)

    return api._connection.send_file(channel_id=int(TEST_FILE_SLACK_CHANNEL_ID), filename=filename, file=file)
