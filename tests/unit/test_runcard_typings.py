""" Test methods for Runcard typing classes"""

from datetime import datetime, timezone

from qiboconnection.typings.responses.runcard_response import RuncardRequest, RuncardResponse


def test_runcard_request_creation():
    """Tests RuncardRequest creation"""

    runcard_request = RuncardRequest(
        name="runcard",
        description="description",
        user_id=0,
        device_id=0,
        runcard="eyJhIjogMH0=",
        qililab_version="0.0.0",
    )

    assert isinstance(runcard_request, RuncardRequest)


def test_runcard_response_creation():
    """Tests RuncardRequest creation"""

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

    assert isinstance(runcard_response, RuncardResponse)
