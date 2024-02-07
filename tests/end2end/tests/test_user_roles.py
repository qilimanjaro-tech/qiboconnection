"""Testing user roles can only do what they are intended to."""
# pylint: disable=logging-fstring-interpolation
import logging
import os
import sys

import pytest
import requests
from qibo.models import Circuit

from qiboconnection.api import API
from qiboconnection.models.devices import Device
from qiboconnection.models.runcard import Runcard
from qiboconnection.typings.enums import DeviceAvailability, DeviceStatus
from qiboconnection.typings.enums.job_status import JobStatus
from qiboconnection.typings.job_data import JobData
from tests.end2end.utils.operations import Operation, check_operation_possible_or_skip
from tests.end2end.utils.utils import (
    UserRole,
    admin_block_device,
    admin_release_device,
    admin_set_device_to_maintenance,
    admin_set_device_to_online,
    get_api_or_fail_test,
    get_device,
    get_devices_listing_params,
    get_logging_conf_or_fail_test,
    get_user_can_change_availability_api,
    get_user_can_change_status_api,
    get_user_can_delete_runcard_api,
    get_user_can_get_runcard_api,
    get_user_can_list_runcard_api,
    get_user_can_save_runcard_api,
    get_user_can_update_runcard_api,
    get_user_cannot_change_availability_api,
    get_user_cannot_change_status_api,
    get_user_cannot_delete_runcard_api,
    get_user_cannot_get_runcard_api,
    get_user_cannot_list_runcard_api,
    get_user_cannot_post_and_list_qprogram_api,
    get_user_cannot_save_runcard_api,
    get_user_cannot_update_runcard_api,
    get_user_roles_id,
    list_runcards,
    list_user_roles,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# ------------------------------------------------------------------------ OPERATION: CAN CHANGE STATUS

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
def test_can_change_device_status(device: Device, user_role: UserRole):
    """Ensure that user roles which, by definition, can change status are allowed to do it.

    Args:
        device (Device): _description_
        user_role (str): _description_
        api (API): _description_
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    api = get_user_can_change_status_api(user_role=user_role)
    check_operation_possible_or_skip(operation=Operation.CHANGE_STATUS, device=device)

    api.set_device_to_online(device_id=device.id)
    assert get_device(api, device.id)._status == DeviceStatus.ONLINE

    api.set_device_to_maintenance(device_id=device.id)
    assert get_device(api, device.id)._status == DeviceStatus.MAINTENANCE

    api.set_device_to_online(device_id=device.id)
    assert get_device(api, device.id)._status == DeviceStatus.ONLINE


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
def test_cannot_change_device_status(device: Device, user_role: UserRole):
    """Ensure that user roles which, by definition, cannot change status are not allowed to do it.

    Args:
        device (Device): all devices
        user_role (str): all users
        api (API): Qiboconnection API instance
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    api = get_user_cannot_change_status_api(user_role=user_role)
    check_operation_possible_or_skip(operation=Operation.CHANGE_STATUS, device=device)

    with pytest.raises(requests.exceptions.HTTPError):
        api.set_device_to_online(device_id=device.id)
        api.set_device_to_maintenance(device_id=device.id)
        api.set_device_to_online(device_id=device.id)


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_cannot_change_device_status_when_blocked(device: Device, user_role: UserRole, api: API):
    """Ensure any user role can change device status when device availabiliyty is not available

    Args:
        device (Device): all devices
        user_role (str): all users
        api (API): Qiboconnection API instance
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    admin_set_device_to_maintenance(device=device, api=api)
    admin_block_device(device=device, api=api)

    user_api = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))

    with pytest.raises(requests.exceptions.HTTPError):
        user_api.set_device_to_online(device_id=device.id)
        user_api.set_device_to_maintenance(device_id=device.id)

    admin_release_device(device=device, api=api)
    admin_set_device_to_online(device=device, api=api)


# ------------------------------------------------------------------------ OPERATION: CAN CHANGE AVAILABILITY


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_can_change_device_availability(device: Device, user_role: UserRole, api: API):
    """Ensure that user roles which, by definition, can change availability are allowed to do it.

    Args:
        device (Device): _description_
        user_role (str): _description_
        api (API): _description_
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    admin_set_device_to_maintenance(device=device, api=api)

    user_role_api = get_user_can_change_availability_api(user_role=user_role)

    user_role_api.release_device(device_id=device.id)
    assert get_device(user_role_api, device.id)._availability == DeviceAvailability.AVAILABLE

    user_role_api.block_device_id(device_id=device.id)
    assert get_device(user_role_api, device.id)._availability == DeviceAvailability.BLOCKED

    user_role_api.release_device(device_id=device.id)
    assert get_device(user_role_api, device.id)._availability == DeviceAvailability.AVAILABLE

    admin_set_device_to_online(device=device, api=api)


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_cannot_change_device_availability(device: Device, user_role: UserRole, api: API):
    """Ensure that user roles which, by definition, cannot change availability are not allowed to do it

    Args:
        device (Device): all devices
        user_role (str): all users
        api (API): Qiboconnection API instance
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    admin_set_device_to_maintenance(device=device, api=api)

    user_api = get_user_cannot_change_availability_api(user_role=user_role)

    with pytest.raises(requests.exceptions.HTTPError):
        user_api.release_device(device_id=device.id)
        user_api.block_device_id(device_id=device.id)
        user_api.release_device(device_id=device.id)

    admin_set_device_to_online(device=device, api=api)


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_cannot_change_device_availability_when_online(device: Device, user_role: UserRole, api: API):
    """Ensure tany user can block any device when status is not maintenance

    Args:
        device (Device): all devices
        user_role (str): all users
        api (API): Qiboconnection API instance
    """
    logger.info(f"Device: {device}, User Role: {user_role}")

    admin_set_device_to_online(device=device, api=api)

    user_api = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))

    with pytest.raises(requests.exceptions.HTTPError):
        user_api.release_device(device_id=device.id)
        user_api.block_device_id(device_id=device.id)
        user_api.release_device(device_id=device.id)

    admin_set_device_to_online(device=device, api=api)


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_cannot_post_qprogram(device: Device, qprogram_dict: dict, user_role: UserRole):
    """Test user roles that aren't allowed to post qprogram can do it -- e.g bsc
    Args:
        api: api instance to call the server with.
    """

    check_operation_possible_or_skip(operation=Operation.POST, device=device)

    user_api = get_user_cannot_post_and_list_qprogram_api(user_role=user_role)

    user_api.select_device_id(device_id=device.id)

    with pytest.raises(requests.exceptions.HTTPError):
        user_api.execute(qprogram=qprogram_dict)


# ------------------------------------------------------------------------ OPERATION: LIST AND SELECT DEVICES


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_can_select_device(device: Device, user_role: UserRole):
    """Test every user can select the devices to which it has access
    Args:
        api: api instance to call the server with
    """
    check_operation_possible_or_skip(operation=Operation.SELECT, device=device)

    user_api = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))
    user_api.select_device_id(device_id=device.id)


# ------------------------------------------------------------------------ OPERATION: LIST JOBS


@pytest.mark.slow
def test_list_jobs(api: API):
    """Test that users can see only their saved experiments"""
    num_saved_exp_admin = len(api.list_jobs().dataframe)

    num_saved_exp_users = [
        len(get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role)).list_jobs().dataframe)
        for user_role in list(UserRole)
        if user_role not in [UserRole.ADMIN, UserRole.MACHINE]
    ]

    assert num_saved_exp_admin >= sum(num_saved_exp_users)


# ------------------------------------------------------------------------ OPERATION: POST, GET AND DELETE JOB


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_post_get_and_delete_job(user_role: UserRole, numpy_circuit: Circuit, device: Device, api: API):
    """Post a circuit and get all its data

    Args:
        user_role (UserRole): _description_
        numpy_circuit (Circuit): _description_
        device (Device): _description_
    """
    check_operation_possible_or_skip(Operation.POST, device=device)
    api_user = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))

    api_user.select_device_id(device_id=device.id)
    job_id = api_user.execute(circuit=numpy_circuit)[0]
    assert isinstance(api_user.get_job(job_id=job_id), JobData)

    if user_role != UserRole.ADMIN:  # check only admin can delete jobs
        with pytest.raises(BaseException):
            api_user.delete_job(job_id=job_id)

    api.delete_job(job_id=job_id)


# ------------------------------------------------------------------------ OPERATION: POST AND CANCEL JOB


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_post_cancel_and_get_job(user_role: UserRole, numpy_circuit: Circuit, device: Device):
    """Post a circuit and cancel it.

    Args:
        user_role (UserRole): _description_
        numpy_circuit (Circuit): _description_
        device (Device): _description_
    """
    check_operation_possible_or_skip(Operation.CANCEL, device=device)
    api_user = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))

    api_user.select_device_id(device_id=device.id)
    job_id = api_user.execute(circuit=numpy_circuit)[0]
    api_user.cancel_job(job_id)
    match device._status:
        case DeviceStatus.OFFLINE:
            assert api_user.get_job(job_id).status == JobStatus.PENDING
        case _:
            assert api_user.get_job(job_id).status == JobStatus.CANCELLED


@pytest.mark.parametrize(
    "device, user_role",
    [(device, user_role) for user_role in list_user_roles() for device in get_devices_listing_params(user_role)],
)
@pytest.mark.slow
def test_only_owned_jobs_can_be_cancelled(user_role: UserRole, numpy_circuit: Circuit, device: Device, api: API):
    """Post a circuit and cancel it.

    Args:
        user_role (UserRole): _description_
        numpy_circuit (Circuit): _description_
        device (Device): _description_
    """
    check_operation_possible_or_skip(Operation.CANCEL, device=device)
    api_user = get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))

    api.select_device_id(device_id=device.id)
    job_id = api.execute(circuit=numpy_circuit)[0]
    match user_role:
        case UserRole.ADMIN:
            api_user.cancel_job(job_id=job_id)
            match device._status:
                case DeviceStatus.OFFLINE:
                    assert api_user.get_job(job_id).status == JobStatus.PENDING
                case _:
                    assert api_user.get_job(job_id).status == JobStatus.CANCELLED
        case _:  # check only admin can delete jobs
            with pytest.raises(BaseException):
                api_user.cancel_job(job_id=job_id)


# ------------------------------------------------------------------------ OPERATION: GET RUNCARDS


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
@pytest.mark.parametrize("runcard", list_runcards())
def test_can_get_runcard(user_role: UserRole, runcard: Runcard):
    "Check certain users can get all runcards"
    api_get = get_user_can_get_runcard_api(user_role=user_role)
    assert isinstance(api_get.get_runcard(runcard_id=runcard.id), Runcard)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
@pytest.mark.parametrize("runcard", list_runcards())
def test_cannot_get_runcard(user_role: UserRole, runcard: Runcard):
    "Check certain users cannot get runcards"
    api_get = get_user_cannot_get_runcard_api(user_role=user_role)
    with pytest.raises(requests.exceptions.HTTPError):
        api_get.get_runcard(runcard_id=runcard.id)


# ------------------------------------------------------------------------ OPERATION: SAVE RUNCARDS


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_can_save_runcard(user_role: UserRole, runcard: Runcard, api: API):
    "Check certain users cannot save runcards"
    api_save = get_user_can_save_runcard_api(user_role=user_role)
    runcard_id = api_save.save_runcard(
        name=runcard.name,
        description=runcard.description,
        runcard_dict=runcard.runcard,
        device_id=runcard.device_id,
        user_id=get_user_roles_id(user_role),
        qililab_version=runcard.qililab_version,
    )
    assert isinstance(runcard_id, int)
    api.delete_runcard(runcard_id)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_save_runcard(user_role: UserRole, runcard: Runcard):
    "Check certain users cannot save runcards"
    api_save = get_user_cannot_save_runcard_api(user_role=user_role)
    with pytest.raises(requests.exceptions.HTTPError):
        api_save.save_runcard(
            name=runcard.name,
            description=runcard.description,
            runcard_dict=runcard.runcard,
            device_id=runcard.device_id,
            user_id=get_user_roles_id(user_role),
            qililab_version=runcard.qililab_version,
        )


# ------------------------------------------------------------------------ OPERATION: DELETE RUNCARDS


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_can_save_and_delete_owned_runcards(user_role: UserRole, runcard: Runcard):
    "Check all users can save runcard delete their runcards except for admin who can delete of all them."
    api_save = get_user_can_save_runcard_api(user_role=user_role)
    api_delete = get_user_can_delete_runcard_api(user_role=user_role)

    runcard_id = api_save.save_runcard(
        name=runcard.name,
        description=runcard.description,
        runcard_dict=runcard.runcard,
        device_id=runcard.device_id,
        user_id=get_user_roles_id(user_role),
        qililab_version=runcard.qililab_version,
    )
    assert isinstance(runcard_id, int)
    api_delete.delete_runcard(runcard_id)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_delete_not_owned_runcard(user_role: UserRole, runcard: Runcard, api: API):
    """Check users cannot delete runcards from other users, in particular, admin."""

    api_delete = get_user_can_delete_runcard_api(user_role=user_role)

    runcard_id = api.save_runcard(
        name=runcard.name,
        description=runcard.description,
        runcard_dict=runcard.runcard,
        device_id=runcard.device_id,
        user_id=get_user_roles_id(user_role=UserRole.ADMIN),
        qililab_version=runcard.qililab_version,
    )
    assert isinstance(runcard_id, int)

    if user_role != UserRole.ADMIN:  # api_delete includes admin
        with pytest.raises(requests.exceptions.HTTPError):
            api_delete.delete_runcard(runcard_id)
    else:
        api_delete.delete_runcard(runcard_id)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_delete_any_runcard(user_role: UserRole, api: API):
    "Check certain users  cannot delete any runcard"
    api_delete = get_user_cannot_delete_runcard_api(user_role=user_role)
    runcards = api.list_runcards()
    assert isinstance(runcards, list)

    for runcard in runcards:
        with pytest.raises(requests.exceptions.HTTPError):
            api_delete.delete_runcard(runcard.id)


# ------------------------------------------------------------------------ OPERATION: LIST RUNCARDS


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_can_list_runcards(user_role: UserRole):
    "Check certain users can list all runcards"
    api_list = get_user_can_list_runcard_api(user_role=user_role)
    runcards = api_list.list_runcards()
    assert isinstance(runcards, list)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_list_runcards(user_role: UserRole):
    "Check certain users cannot list runcards"
    api_list = get_user_cannot_list_runcard_api(user_role=user_role)
    with pytest.raises(requests.exceptions.HTTPError):
        api_list.list_runcards()


# ------------------------------------------------------------------------ OPERATION: UPDATE RUNCARDS


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_can_save_get_and_update_owned_runcards(user_role: UserRole, runcard: Runcard, api: API):
    "Check certain users can update their own runcards"
    api_save = get_user_can_save_runcard_api(user_role=user_role)
    api_update = get_user_can_update_runcard_api(user_role=user_role)
    api_get = get_user_can_get_runcard_api(user_role=user_role)

    runcard_id = api_save.save_runcard(
        name=runcard.name,
        description=runcard.description,
        runcard_dict=runcard.runcard,
        device_id=runcard.device_id,
        user_id=get_user_roles_id(user_role),
        qililab_version=runcard.qililab_version,
    )
    runcard_to_update = api_get.get_runcard(runcard_id=runcard_id)
    runcard_to_update.description = "updated_from_tests"
    updated_runcard = api_update.update_runcard(runcard_to_update)
    assert isinstance(updated_runcard, Runcard)
    api.delete_runcard(runcard_id)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_update_not_owned_runcards(user_role: UserRole, runcard: Runcard, api: API):
    "Check users who are allowed to update runcards can only update theirs"
    api_update = get_user_can_update_runcard_api(user_role=user_role)

    runcard_id = api.save_runcard(
        name=runcard.name,
        description=runcard.description,
        runcard_dict=runcard.runcard,
        device_id=runcard.device_id,
        user_id=get_user_roles_id(user_role=UserRole.ADMIN),
        qililab_version=runcard.qililab_version,
    )
    runcard_to_update = api.get_runcard(runcard_id)
    if user_role != UserRole.ADMIN:
        with pytest.raises(requests.exceptions.HTTPError):
            runcard_to_update.description = "updated from tests"
            api_update.update_runcard(runcard_to_update)
    api.delete_runcard(runcard_id)


@pytest.mark.slow
@pytest.mark.parametrize("user_role", list_user_roles())
def test_cannot_update_any_runcards(user_role: UserRole, api: API):
    "Check certain users can update their own runcards"
    api_update = get_user_cannot_update_runcard_api(user_role=user_role)
    runcards = api.list_runcards()
    assert isinstance(runcards, list)

    if user_role != UserRole.ADMIN:  # api includes admin
        for runcard in runcards:
            with pytest.raises(requests.exceptions.HTTPError):
                runcard.description = "updated"
                api_update.update_runcard(runcard)
