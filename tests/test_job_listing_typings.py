from qiboconnection.typings.job import JobFullData, ListingJobResponse


def test_JobFullData_typing():
    """Test JobFullData typing, this is what is returned to the user with get_job()."""

    job_full_data = JobFullData(
        queue_position=32,
        status="89",
        user_id=None,
        device_id=3,
        job_id=4,
        job_type="jaiof",
        number_shots=84,
        description="<qibo.models.circuit.Circuit at 0x7fb8c2127650>",
        result={},
    )
    assert isinstance(job_full_data, JobFullData)


def test_ListingJobResponse_typing():
    """Test ListingJobResponse instantation"""

    listing_job_response = ListingJobResponse(
        status="89", user_id=None, device_id=3, job_type="jaiof", number_shots=84, id=3
    )

    assert isinstance(listing_job_response, ListingJobResponse)
