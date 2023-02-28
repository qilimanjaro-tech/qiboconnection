""" Test methods for SavedExperiment classes"""

import datetime

from qiboconnection.saved_experiment import SavedExperiment
from qiboconnection.typings.saved_experiment import (
    SavedExperimentRequest,
    SavedExperimentResponse,
)


def test_saved_experiment_creation():
    """Tests SavedExperiment creation"""
    saved_experiment = SavedExperiment(
        name="name",
        user_id=1,
        device_id=1,
        description="description",
        experiment={"a": 0},
        results={"a": 0},
        qililab_version="0.0.0",
        id=0,
        created_at=datetime.datetime.now(),
    )

    assert isinstance(saved_experiment, SavedExperiment)


def test_saved_experiment_creation_from_response():
    """Tests SavedExperiment creation from response"""
    saved_experiment_response = SavedExperimentResponse(
        name="name",
        user_id=1,
        device_id=1,
        description="description",
        experiment="eyJhIjogMH0=",
        results="eyJhIjogMH0=",
        qililab_version="0.0.0",
        saved_experiment_id=0,
        created_at=datetime.datetime.now(),
    )

    saved_experiment = SavedExperiment.from_response(response=saved_experiment_response)

    assert isinstance(saved_experiment, SavedExperiment)
    assert saved_experiment.experiment == {"a": 0}, "Decoded experiment does not coincide with expected"
    assert saved_experiment.results == {"a": 0}, "Decoded results do not coincide with expected"


def test_saved_experiment_request():
    """Tests SavedExperiment request builder method"""
    saved_experiment = SavedExperiment(
        name="name",
        user_id=1,
        device_id=1,
        description="description",
        experiment={"a": 0},
        results={"a": 0},
        qililab_version="0.0.0",
        id=0,
        created_at=datetime.datetime.now(),
    )

    saved_experiment_request = saved_experiment.saved_experiment_request(favourite=False)

    assert isinstance(saved_experiment_request, SavedExperimentRequest)
    assert saved_experiment_request.experiment == "eyJhIjogMH0=", "Decoded experiment does not coincide with expected"
    assert saved_experiment_request.results == "eyJhIjogMH0=", "Decoded results do not coincide with expected"
