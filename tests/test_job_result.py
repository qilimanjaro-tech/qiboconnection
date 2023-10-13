""" Tests methods for job result """
import numpy as np

from qiboconnection.models.job_result import JobResult
from qiboconnection.typings.enums import JobType


def test_job_result_creation():
    """Test job result creation"""
    job_result = JobResult(
        job_id=1,
        http_response="gASVsAAAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwWFlGgDjAVkdHlwZZSTlIwCZjiUiYiHlFKUKEsDjAE8lE5OTkr_____Sv____9LAHSUYolDKAAAAAAAAPA_AAAAAAAA8D8AAAAAAADwPwAAAAAAAPA_AAAAAAAA8D-UdJRiLg==",
        job_type=JobType.CIRCUIT,
    )

    assert isinstance(job_result, JobResult)
    assert job_result.job_id == 1
    assert (
        job_result.http_response
        == "gASVsAAAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwWFlGgDjAVkdHlwZZSTlIwCZjiUiYiHlFKUKEsDjAE8lE5OTkr_____Sv____9LAHSUYolDKAAAAAAAAPA_AAAAAAAA8D8AAAAAAADwPwAAAAAAAPA_AAAAAAAA8D-UdJRiLg=="
    )
    assert (job_result.data == np.array([1.0, 1.0, 1.0, 1.0, 1.0])).all()


def test_job_result_program_raises_error():
    """Test we are rising exceptions to inform correctly that PROGRAMS are not currently supported."""

    job_result = JobResult(job_id=0, http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==", job_type="program")
    assert isinstance(job_result.data, str)
