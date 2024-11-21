"""Test methods for Calibration typing classes"""

from datetime import datetime, timezone

from qiboconnection.typings.responses.calibration_response import CalibrationRequest, CalibrationResponse


def test_calibration_request_creation():
    """Tests CalibrationRequest creation"""

    calibration_request = CalibrationRequest(
        name="calibration",
        description="description",
        user_id=0,
        device_id=0,
        calibration="eyJhIjogMH0=",
        qililab_version="0.0.0",
    )

    assert isinstance(calibration_request, CalibrationRequest)


def test_calibration_response_creation():
    """Tests CalibrationRequest creation"""

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

    assert isinstance(calibration_response, CalibrationResponse)
