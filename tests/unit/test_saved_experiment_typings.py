""" Test methods for SavedExperiment typing classes"""

import datetime

from qiboconnection.typings.requests import SavedExperimentRequest
from qiboconnection.typings.responses import SavedExperimentListingItemResponse, SavedExperimentResponse


def test_saved_experiment_request_creation():
    """Tests SavedExperimentRequest creation"""
    saved_experiment_request = SavedExperimentRequest(
        name="name",
        experiment="eyJhIjogMH0=",
        results="eyJhIjogMH0=",
        device_id=1,
        user_id=1,
        description="description",
        qililab_version="0.0.0",
        favourite=False,
    )

    assert isinstance(saved_experiment_request, SavedExperimentRequest)


def test_saved_experiment_response_creation():
    """Tests SavedExperimentResponse creation"""
    saved_experiment_response = SavedExperimentResponse(
        name="name",
        experiment="eyJhIjogMH0=",
        results="eyJhIjogMH0=",
        device_id=1,
        user_id=1,
        description="description",
        qililab_version="0.0.0",
        saved_experiment_id=0,
        created_at=datetime.datetime.now(),
    )

    assert isinstance(saved_experiment_response, SavedExperimentResponse)


def test_saved_experiment_listing_item_response_creation():
    """Tests SavedExperimentListingItemResponse creation"""
    saved_experiment_listing_item_response = SavedExperimentListingItemResponse(
        name="name",
        experiment="eyJhIjogMH0=",
        device_id=1,
        user_id=1,
        description="description",
        qililab_version="0.0.0",
        id=0,
        created_at=datetime.datetime.now(),
    )

    assert isinstance(saved_experiment_listing_item_response, SavedExperimentListingItemResponse)
