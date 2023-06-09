from qiboconnection.job_listing import JobListing, JobListingItem
from qiboconnection.typings.job import JobFullData, ListingJobResponse


def test_job_listing_item_creation_from_response():
    """JobListingItem cration from response"""
    listing_job_response = ListingJobResponse(
        status="89", user_id=None, device_id=3, job_type="jaiof", number_shots=84, id=3
    )
    Job_listing_item = JobListingItem.from_response(listing_job_response)

    assert isinstance(Job_listing_item, JobListingItem)
    assert Job_listing_item.id == listing_job_response.id
