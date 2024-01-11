import warnings

import pytest

from qiboconnection.api import API


@pytest.mark.order(0)
def test_store_initial_job_and_runcard_count(api: API, request):
    """Count number jobs and runcards before running the test suite"""
    initial_job_count = len(api.list_jobs().dataframe)
    initial_runcards_count = len(api.list_runcards())
    request.config.cache.set("initial_job_count", initial_job_count)
    request.config.cache.set("initial_runcards_count", initial_runcards_count)

    assert isinstance(initial_job_count, int)


@pytest.mark.order(-1)
def test_check_all_test_jobs_and_runcards_deleted(api: API, request):
    """Count number jobs and runcards before running the test suite"""
    if request.config.cache.get("initial_job_count", None) != len(api.list_jobs().dataframe):
        warnings.warn(
            "Initial job count doesn't match the post test suite job count, make sure you are deleting all created jobs within its corresponding test!"
        )
    if request.config.cache.get("initial_runcards_count", None) != len(api.list_runcards()):
        warnings.warn(
            "Initial runcards count doesn't match the post test suite ruyncards count, make sure you are deleting all created runcards within its corresponding test!"
        )
