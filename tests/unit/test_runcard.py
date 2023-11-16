""" Test methods for Runcards classes """

from datetime import datetime, timezone

from qiboconnection.models.runcard import Runcard
from qiboconnection.typings.responses.runcard_response import RuncardRequest, RuncardResponse

# pylint: disable=no-member


def test_runcard_creation():
    """Tests Runcard Creation"""

    runcard = Runcard(
        name="runcard",
        description="description",
        user_id=0,
        device_id=0,
        runcard={"a": 0},
        qililab_version="0.0.0",
    )

    assert isinstance(runcard, Runcard)


def test_runcard_creation_from_response():
    """Tests Runcard Creation"""

    runcard_response = RuncardResponse(
        name="runcard",
        description="description",
        user_id=0,
        device_id=0,
        runcard="eyJhIjogMH0=",
        qililab_version="0.0.0",
        runcard_id=0,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    runcard = Runcard.from_response(response=runcard_response)

    assert isinstance(runcard, Runcard)
    assert runcard.runcard == {"a": 0}, "Decoded runcard does not coincide with expected"


def test_runcard_request():
    """Tests Runcard request builder method"""

    runcard = Runcard(
        name="runcard",
        description="description",
        user_id=0,
        device_id=0,
        runcard={"a": 0},
        qililab_version="0.0.0",
    )

    runcard_request = runcard.runcard_request()

    assert isinstance(runcard_request, RuncardRequest)
    assert runcard_request.runcard == "eyJhIjogMH0="
