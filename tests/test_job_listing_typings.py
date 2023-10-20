from unittest.mock import MagicMock, patch

import pytest

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


def test_JobData_typing_result_raises_value_error():
    """Test JobData typing raises error if results are not the correct type"""

    with pytest.raises(ValueError) as ex:
        _ = JobData(
            queue_position=32,
            status="completed",
            user_id=None,
            device_id=3,
            job_id=4,
            job_type="jaiof",
            number_shots=84,
            description="<qibo.models.circuit.Circuit at 0x7fb8c2127650>",
            result="Not a dict or list",
        )

    assert ex.match("Job result needs to be a dict, a list or a None!")


@patch("qiboconnection.typings.job_data.deserialize_job_description", autospec=True)
def test_JobData_typing_descripton_raises_value_error(mocked_deserialize_job_description: MagicMock):
    """Test JobData typing, this is what is returned to the user with get_job()."""

    mocked_deserialize_job_description.return_value = "A bad description"

    with pytest.raises(ValueError) as ex:
        _ = JobData(
            queue_position=32,
            status="invent",
            user_id=None,
            device_id=3,
            job_id=4,
            job_type="experiment",
            number_shots=84,
            description="",
            result="",
        )

    assert ex.match("Job description needs to be a Qibo Circuit, a dict, a list or a None!")


def test_job_listing_item_response_typing():
    """Test JobListingItemResponse instantiation"""

    listing_job_response = JobListingItemResponse(
        status="89", user_id=None, device_id=3, job_type="jaiof", number_shots=84, id=3
    )

    assert isinstance(listing_job_response, JobListingItemResponse)
