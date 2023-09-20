import pandas as pd

from qiboconnection.models.job_listing import JobListing, JobListingItem
from qiboconnection.typings.responses import JobListingItemResponse


def test_job_listing_item_creation_from_response():
    """JobListingItem cration from response"""
    listing_job_response = JobListingItemResponse(
        status="89", user_id=None, device_id=3, job_type="jaiof", number_shots=84, id=3
    )
    Job_listing_item = JobListingItem.from_response(listing_job_response)

    assert isinstance(Job_listing_item, JobListingItem)
    assert Job_listing_item.id == listing_job_response.id


def test_job_listing_creation_dataframe():
    """Ensure job are listed as dataframes"""
    listing_job_response_1 = JobListingItemResponse(
        status="89", user_id=5, device_id=3, job_type="jaiof", number_shots=84, id=3
    )
    listing_job_response_2 = JobListingItemResponse(
        status="89", user_id=5, device_id=38, job_type="jahfwsiof", number_shots=884, id=3
    )
    job_listing = JobListing.from_response([listing_job_response_1, listing_job_response_2])

    assert isinstance(job_listing, JobListing)
    assert isinstance(job_listing.dataframe, pd.DataFrame)
