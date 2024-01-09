import json
import os
import sys
from pathlib import Path
from typing import Union

from utils.slack_report_utils import send_slack_file, send_slack_message

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


os.environ["QIBOCONNECTION_ENVIRONMENT"] = "development"

# GLOBALS
WORKDIR = Path(".")  # cwd in daily_e2e_tests.yml in qgqs is qiboconnection/tests
LOGS_PATH = WORKDIR / "logs"
PATH_SUMMARY = LOGS_PATH / "summary.txt"
PATH_TEST_RUN = LOGS_PATH / "test_run.json"
PATH_FULL_REPORT = LOGS_PATH / "test_run.md"


def main():
    """Entry point"""
    send_tests_summary_as_message()
    send_tests_full_report_as_file()


def send_tests_summary_as_message():
    """Send a summary text to Slack."""
    summary: Union[str, None] = None

    try:
        summary = ""
        with open(PATH_TEST_RUN, "r") as file:
            data: dict = json.load(file)["summary"]
            summary += f"Test Cases: {data['tot_test_plan']} - "
            summary += f"Test Cases Executed: {data['tot_test_plan_executed']} : "
            summary += ", ".join([f"{outcome} : {tot}" for outcome, tot in data["tot_outcomes"].items()])
        send_slack_message(f"{summary}", test_summary_message=True)
    except Exception as e:
        send_slack_message(
            f":skull: SUMMARY ERROR\n-Found {e}\n."
            f" {'' if not summary else 'The message had size '+str(len(summary))}."
        )


def send_tests_full_report_as_file():
    """ "Send a file to Slack"""
    try:
        filename = PATH_FULL_REPORT.name
        file = open(PATH_FULL_REPORT, "r")
        send_slack_file(filename=filename, file=file)
    except Exception as e:
        send_slack_message(f":skull: FULL REPORT ERROR\n-Found {e}")


if __name__ == "__main__":
    """Main entry point"""
    main()
