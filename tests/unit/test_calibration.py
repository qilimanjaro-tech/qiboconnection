"""Test methods for Calibrations classes"""

from datetime import datetime, timezone

import yaml

from qiboconnection.models.calibration import Calibration
from qiboconnection.typings.responses.calibration_response import CalibrationRequest, CalibrationResponse


def test_calibration_creation():
    """Tests Calibration Creation"""

    calibration = Calibration(
        name="calibration",
        description="description",
        user_id=0,
        device_id=0,
        calibration={"a": 0},
        qililab_version="0.0.0",
    )

    assert isinstance(calibration, Calibration)


def test_calibration_creation_from_response():
    """Tests Calibration Creation"""

    calibration_response = CalibrationResponse(
        name="calibration",
        description="description",
        user_id=0,
        device_id=0,
        calibration="eyJhIjogMH0=",
        qililab_version="0.0.0",
        calibration_id=0,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    calibration = Calibration.from_response(response=calibration_response)

    assert isinstance(calibration, Calibration)
    assert yaml.safe_load(calibration.calibration) == {"a": 0}, "Decoded calibration does not coincide with expected"


def test_calibration_request():
    """Tests Calibration request builder method"""

    calibration = Calibration(
        name="calibration",
        description="description",
        user_id=0,
        device_id=0,
        calibration={"a": 0},
        qililab_version="0.0.0",
    )

    calibration_request = calibration.calibration_request()

    assert isinstance(calibration_request, CalibrationRequest)
    assert calibration_request.calibration == "eyJhIjogMH0="
