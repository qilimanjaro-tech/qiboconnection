""" Tests methods for job result """
from qiboconnection.job_result import JobResult


def test_job_result_creation():
    """Test job result creation"""
    job_result = JobResult(
        job_id=1,
        http_response="WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ==",
    )
    assert isinstance(job_result, JobResult)
    assert job_result.job_id == 1
    assert job_result.http_response == "WzAuMSwgMC4xLCAwLjEsIDAuMSwgMC4xXQ=="
    assert job_result.data == [0.1, 0.1, 0.1, 0.1, 0.1]
