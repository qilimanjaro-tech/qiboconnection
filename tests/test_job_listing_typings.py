from qiboconnection.typings.job_data import JobData
from qiboconnection.typings.responses import JobListingItemResponse


def test_JobData_typing():
    """Test JobData typing, this is what is returned to the user with get_job()."""

    job_full_data = JobData(
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
    assert isinstance(job_full_data, JobData)


def test_job_listing_item_response_typing():
    """Test JobListingItemResponse instantiation"""

    listing_job_response = JobListingItemResponse(
        status="89", user_id=None, device_id=3, job_type="jaiof", number_shots=84, id=3
    )

    assert isinstance(listing_job_response, JobListingItemResponse)
