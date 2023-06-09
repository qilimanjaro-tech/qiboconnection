from qiboconnection.typings.job import JobFullData


def test_JobFullData_typing():
    job_full_data = JobFullData(
        queue_position=32,
        status="89",
        user_id=None,
        device_id=3,
        job_id=4,
        job_type="jaiof",
        number_shots=84,
        result={},
    )
    assert isinstance(job_full_data, JobFullData)
