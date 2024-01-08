"""Endurance tests."""
# pylint: disable=logging-fstring-interpolation
import logging

import pytest
from end2end.utils.operations import Operation, check_operation_possible_or_skip
from end2end.utils.utils import get_devices_listing_params, post_and_get_result
from qibo.models import Circuit

from qiboconnection.api import API
from qiboconnection.models.devices import Device
from qiboconnection.typings.enums import JobStatus
from qiboconnection.typings.responses.job_response import JobResponse


@pytest.mark.parametrize("device", get_devices_listing_params())
@pytest.mark.slow
def test_endurance(device: Device, api: API, numpy_circuit: Circuit, total: int = 100, timeout: int = 5):
    """Check there is no a degradation of service.

    The same circuit is executed multiple times and  wait always the same maximum amount of time for a COMPLETED status.

    Args:
        device (Device): The device instance
        api (API): The api instance
        numpy_circuit (Circuit): the circuit
    """

    check_operation_possible_or_skip(Operation.RESPONSE, device)

    logger = logging.getLogger(__name__)

    logger.info(f"Device: {device}")
    for ind in range(total):
        logger.info(f"Run {ind}/{total} (wait {timeout} seconds)")
        result: JobResponse = post_and_get_result(api, device, numpy_circuit, timeout)
        logger.info(f"Job #{result.job_id}: {result.status}")
        assert result.status == JobStatus.COMPLETED
        api.delete_job(job_id=result.job_id)
