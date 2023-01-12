""" Test methods for SavedExperimentListing classes"""
import datetime

import pandas as pd

from qiboconnection.saved_experiment_listing import (
    SavedExperimentListing,
    SavedExperimentListingItem,
)
from qiboconnection.typings.saved_experiment import SavedExperimentListingItemResponse


def test_saved_experiment_listing_item_creation():
    """Tests SavedExperimentListingItem creation"""

    saved_experiment_listing_item = SavedExperimentListingItem(
        name="name",
        experiment={"a": 0},
        device_id=1,
        user_id=1,
        description="description",
        qililab_version="0.0.0",
        id=0,
        created_at=datetime.datetime.now(),
    )

    assert isinstance(saved_experiment_listing_item, SavedExperimentListingItem)


def test_saved_experiment_listing_item_creation_from_response():
    """Tests SavedExperimentListingItem's from_response() constructor"""

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

    saved_experiment_listing_item = SavedExperimentListingItem.from_response(
        response=saved_experiment_listing_item_response
    )

    assert isinstance(saved_experiment_listing_item, SavedExperimentListingItem)
    assert saved_experiment_listing_item.experiment == {"a": 0}, "Decoded experiment does not coincide with expected"


def test_saved_experiment_listing_creation():
    """Tests SavedExperimentListing creation"""

    saved_experiment_listing_item = SavedExperimentListingItem(
        name="name",
        experiment={"a": 0},
        device_id=1,
        user_id=1,
        description="description",
        qililab_version="0.0.0",
        id=0,
        created_at=datetime.datetime.now(),
    )

    saved_experiment_listing = SavedExperimentListing(items=[saved_experiment_listing_item])

    assert isinstance(saved_experiment_listing, SavedExperimentListing)
    assert isinstance(saved_experiment_listing.dataframe, pd.DataFrame)


def test_saved_experiment_listing_creation_from_response():
    """Tests SavedExperimentListing creation"""

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

    saved_experiment_listing = SavedExperimentListing.from_response(
        response_list=[saved_experiment_listing_item_response]
    )

    assert isinstance(saved_experiment_listing, SavedExperimentListing)
    assert isinstance(saved_experiment_listing.dataframe, pd.DataFrame)
