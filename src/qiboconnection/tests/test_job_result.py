""" Tests methods for job result """
from qiboconnection.job_result import JobResult


def test_job_result_creation():
    job_result = JobResult(
        job_id=1,
        http_response={"code": "201", "response": "some response"},
        data=[0.1, 0.1, 0.1, 0.1, 0.1],
    )
    assert isinstance(job_result, JobResult)
    assert job_result.job_id == 1
    assert job_result.http_response == {"code": "201", "response": "some response"}
    assert job_result.data == [0.1, 0.1, 0.1, 0.1, 0.1]
