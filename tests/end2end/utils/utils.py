# pylint: disable=logging-fstring-interpolation
# pylint: disable=protected-access
# pylint: disable=no-name-in-module
import logging
import os
from enum import Enum
from time import sleep

import pytest
from numpy import False_
from qibo.models.circuit import Circuit

from qiboconnection.api import API
from qiboconnection.errors import HTTPError
from qiboconnection.models.devices import Device
from qiboconnection.typings.connection import ConnectionConfiguration
from qiboconnection.typings.enums import DeviceAvailability, DeviceStatus, JobStatus
from qiboconnection.typings.job_data import JobData


class MissingCredentialsException(ValueError):
    pass


class UserRole(str, Enum):
    """User roles with different permissions. admin is allowed to change device status and availability. qilimanjaro_user can only change availability provided that device status=maintenance. bsc_user can change none."""

    ADMIN = "admin"
    QILI = "qilimanjaro_user"
    BSC = "bsc_user"
    MACHINE = "machine"


TIMEOUT = 100
CALL_EVERY_SECONDS = 10

USER_OPERATIONS = [
    {
        "role": UserRole.ADMIN,
        "can_change_status": True,
        "can_change_availability": True,
        "can_post_qprograms": True,
        "can_post_vqas": True,
        "can_get_runcard": True,
        "can_list_runcard": True,
        "can_save_runcard": True,
        "can_delete_runcard": True,
        "can_update_runcard": True,
    },
    {
        "role": UserRole.BSC,
        "can_change_status": False,
        "can_change_availability": False,
        "can_post_qprograms": True,
        "can_post_vqas": False,
        "can_get_runcard": True,
        "can_list_runcard": True,
        "can_save_runcard": False,
        "can_delete_runcard": False,
        "can_update_runcard": False,
    },
    {
        "role": UserRole.QILI,
        "can_change_status": False,
        "can_change_availability": True,
        "can_post_qprograms": True,
        "can_post_vqas": True,
        "can_get_runcard": True,
        "can_list_runcard": True,
        "can_save_runcard": True,
        "can_delete_runcard": True,
        "can_update_runcard": True,
    },
    {
        "role": UserRole.MACHINE,
        "can_change_status": False,
        "can_change_availability": False,
        "can_post_qprograms": False,
        "can_post_vqas": False,
        "can_get_runcard": True,
        "can_list_runcard": False,
        "can_save_runcard": True,
        "can_delete_runcard": False,
        "can_update_runcard": True,
    },
]

# TODO: review if these methods are really needed or instead that just raise an exception if there is an error
# These methods are used in the fixtures like get_api_fixture()


def is_development() -> bool:
    """Returns True if the environment is development.

    Returns:
        bool: if the environment is development
    """
    return os.environ["QIBOCONNECTION_ENVIRONMENT"] == "development"


def get_logging_conf_or_fail_test(user_role=UserRole.ADMIN) -> ConnectionConfiguration:
    """Informatively fail the test if the ConnectionConfiguration instance could not be build with the credentials:

    Returns:
        ConnectionConfiguration: credentials instance if it could be built."""
    try:
        return get_logging_conf(role=user_role)
    except MissingCredentialsException:
        return pytest.fail("Login failed. Credentials were not provided in the environment.", pytrace=True)


def get_api_or_fail_test(  # pylint: disable=inconsistent-return-statements
    logging_conf: ConnectionConfiguration,
) -> API:
    """Informatively fail the test if the API instance could not be build with the ConnectionConfiguration:

    Returns:
        API: api instance if it could be built."""
    try:
        return API(configuration=logging_conf)
    except MissingCredentialsException as ex:
        pytest.fail(f"Login failed. Check credentials. {ex}.", pytrace=True)


def get_devices_listing_params(user_role: UserRole = UserRole.ADMIN) -> list[Device]:
    """Not a fixture. Normal function that returns the list of devices. For using on parametrize (that cannot accept
    fixtures)."""
    logging_conf = get_logging_conf(role=user_role)
    qibo_api = get_api_or_fail_test(logging_conf)
    try:
        devices = qibo_api.list_devices()
        return devices._devices
    except HTTPError:
        return []


def get_device(api: API, device_id) -> Device:
    """Get a device by id.

    Args:
        api (API): api instance
        device_id (_type_): device id

    Raises:
        Exception: if no device is found

    Returns:
        Device: the device instance
    """
    if found := [device for device in api.list_devices()._devices if device.id == device_id]:
        return found[0]
    raise NameError(f"Not found device with id {device_id}")


def post_and_get_result(
    api: API,
    device: Device,
    circuit: Circuit | list[Circuit],
    timeout: int = TIMEOUT,
    call_every_seconds: int = CALL_EVERY_SECONDS,
    name: str = "-",
    summary: str = "-",
) -> JobData:
    """Post a circuit and tries to get the result. While he job is pending, retries during timeout

    Args:
        api (API): the api instance
        device (Device): the device instance
        circuit (Circuit): the circuit to be posted
        timeout (int, optional): number of seconds the job is in pending before returning. Defaults to 250.
        call_every_seconds (int, optional): how often, in seconds, the results are requested. Defaults to 5.

    Returns:
        JobResponse: The object with the result of the job.
    """

    api.select_device_id(device_id=device.id)
    job_id = api.execute(circuit=circuit, name=name, summary=summary)[0]

    return get_job_result(api, job_id, timeout, call_every_seconds)


def delete_job(api: API, job_id: int):
    """Delete a job.

    Args:
        api (API): the api instance
        job_id (int): the id of the job
    """

    api.delete_job(job_id)


def get_job_result(api: API, job_id: int, timeout: int = 250, call_every_seconds: int = 5) -> JobData:
    """Post a circuit and tries to get the result. While he job is pending, retries during timeout

    Args:
        api (API): the api instance
        job_id (int): The id with the job
        timeout (int, optional): number of seconds the job is in pending before returning. Defaults to 250.
        call_every_seconds (int, optional): how often, in seconds, the results are requested. Defaults to 5.

    Returns:
        JobResponse: The object with the result of the job.
    """
    logger = logging.getLogger(__name__)
    timer = 0
    job_data: JobData = None
    while timer < timeout:
        sleep(call_every_seconds)
        logger.debug(f"timer: {timer}, timeout: {timeout}")
        job_data = api.get_job(job_id)
        if job_data.status not in [JobStatus.PENDING, JobStatus.QUEUED]:
            break

        timer += call_every_seconds

    return job_data


def get_user_role_operations(user_role: UserRole) -> dict:
    """Get a dictionary that specifies with booleans which operations are allowed
    depending on the user role.

    Args:
        user_role (str): valur from UserRole enum

    Raises:
        Exception: None operation found
        Exception: More than one operation found

    Returns:
        dict: one of the dicts defined in USER_OPERATIONS object
    """
    ops = [item for item in USER_OPERATIONS if user_role == item["role"]]
    if len(ops) == 0:
        raise ValueError(f"Not found operation for user role:{user_role}")
    if len(ops) > 1:
        raise ValueError(f"Found {len(ops)} operations (when 1 was expected) in status:{user_role}")

    return ops[0]


def list_user_roles() -> list[UserRole]:
    """Get a list of user roles defined in UserRole enum

    Returns:
        List : List of defined user roles
    """
    return list(UserRole)


def get_user_roles_id(user_role: UserRole) -> int:
    """Get the id of a user with the corresponding user role

    Returns:
        int: user id
    """
    if user_role == UserRole.ADMIN:
        return 3  # qili-admin-test
    if user_role == UserRole.BSC:
        return 5  # bsc-user
    if user_role == UserRole.QILI:
        return 6  # qili-user
    if user_role == UserRole.MACHINE:
        return 13  # dev_quant
    raise ValueError(f"No user id defined for {user_role}")


def list_runcards():
    "List all runcards with admin"
    return get_api_or_fail_test(get_logging_conf_or_fail_test()).list_runcards()


def get_user_can_change_status_api(user_role: UserRole):
    """Get API instance for the user roles that can change status, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API: API instance only for the users that can change status
    """

    if not get_user_role_operations(user_role=user_role)["can_change_status"]:
        pytest.skip(f"{user_role} cannot change status")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_change_status_api(user_role: UserRole):
    """Get API instance for the user roles that can change status, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API: API instance only for the users that can change status
    """
    if get_user_role_operations(user_role=user_role)["can_change_status"]:
        pytest.skip(f"{user_role} can change status")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_change_availability_api(user_role: UserRole):
    """Get API instance for the user roles that can change availability, by definition.
    Args:
        user_role (UserRole):

    Returns:
        API: API instance only for the users that can change status
    """

    if not get_user_role_operations(user_role=user_role)["can_change_availability"]:
        pytest.skip(f"{user_role} cannot change availability")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_change_availability_api(user_role: UserRole):
    """Get API instance for the user roles that cannot change availability, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API: API instance only for the users that can change status
    """
    if get_user_role_operations(user_role=user_role)["can_change_availability"]:
        pytest.skip(f"{user_role} can change availability")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_post_and_list_qprogram_api(user_role: UserRole):
    """Get API instance for the user roles that cannot post qililab qprogram, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API: API instance only for the users that cannot post qprogram
    """
    if get_user_role_operations(user_role=user_role)["can_post_qprograms"]:
        pytest.skip(f"{user_role} can post qprograms")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_post_and_list_vqa_api(user_role: UserRole):
    """Get API instance for the user roles that cannot post applications-sdk vqa, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API: API instance
    """
    if get_user_role_operations(user_role=user_role)["can_post_vqas"]:
        pytest.skip(f"{user_role} can post vqas")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_save_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that can save runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if not get_user_role_operations(user_role=user_role)["can_save_runcard"]:
        pytest.skip(f"{user_role} cannot save runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_save_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that cannot save runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if get_user_role_operations(user_role=user_role)["can_save_runcard"]:
        pytest.skip(f"{user_role} can save runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_delete_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that can delete runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if not get_user_role_operations(user_role=user_role)["can_delete_runcard"]:
        pytest.skip(f"{user_role} cannot delete runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_delete_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that cannot delete runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if get_user_role_operations(user_role=user_role)["can_delete_runcard"]:
        pytest.skip(f"{user_role} can delete runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_update_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that can update runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if not get_user_role_operations(user_role=user_role)["can_update_runcard"]:
        pytest.skip(f"{user_role} cannot update runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_update_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that cannot update runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if get_user_role_operations(user_role=user_role)["can_update_runcard"]:
        pytest.skip(f"{user_role} can update runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_get_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that can get runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if not get_user_role_operations(user_role=user_role)["can_get_runcard"]:
        pytest.skip(f"{user_role} cannot get runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_get_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that cannot get runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if get_user_role_operations(user_role=user_role)["can_get_runcard"]:
        pytest.skip(f"{user_role} can get runcards")

    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_can_list_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that can list runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if not get_user_role_operations(user_role=user_role)["can_list_runcard"]:
        pytest.skip(f"{user_role} cannot list runcards")
    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def get_user_cannot_list_runcard_api(user_role: UserRole):
    """Get API instance for the user roles that cannot list runcards, by definition.

    Args:
        user_role (UserRole):

    Returns:
        API
    """
    if get_user_role_operations(user_role=user_role)["can_list_runcard"]:
        pytest.skip(f"{user_role} can list runcards")
    return get_api_or_fail_test(get_logging_conf_or_fail_test(user_role=user_role))


def admin_set_device_to_online(device: Device, api: API):
    """Set device to online by admin user

    Args:
        device (Device): device.
    """
    if device._availability == DeviceAvailability.BLOCKED:
        pytest.fail(f"{device.name} is {device._availability} and hence can't set it to online.")

    if device._status == DeviceStatus.OFFLINE and is_development():
        pytest.skip(f"{device.name} is {device._status}")

    api.set_device_to_online(device_id=device.id)


def admin_set_device_to_maintenance(device: Device, api: API):
    """Set device status to maintenance by admin user

    Args:
        device (Device): device
    """
    if get_device(api, device.id)._availability == DeviceAvailability.BLOCKED:
        pytest.fail(f"{device.name} is {device._availability} and hence can't set it to maintenance.")

    if get_device(api, device.id)._status == DeviceStatus.OFFLINE and is_development():
        pytest.skip(f"{device.name} is {device._status}")

    api.set_device_to_maintenance(device_id=device.id)


def admin_block_device(device: Device, api: API):
    """Block device with admin user

    Args:
        device (Device): device
    """

    if get_device(api, device.id)._status == DeviceStatus.ONLINE:
        pytest.fail(f"{device.name} is {device._status} and hence can't block it.")

    if get_device(api, device.id)._status == DeviceStatus.OFFLINE and is_development():
        pytest.skip(f"{device} is {device._status}")

    api.block_device_id(device_id=device.id)


def admin_release_device(device: Device, api: API):
    """Release device with admin user

    Args:
        device (Device): device
    """

    if get_device(api, device.id)._status == DeviceStatus.ONLINE:
        pytest.fail(f"{device.name} is {device._status} and hence can't release it.")

    if get_device(api, device.id)._status == DeviceStatus.OFFLINE and is_development():
        pytest.skip(f"{device.name} is {device._status}")

    api.release_device(device_id=device.id)


def get_logging_conf(role: UserRole = UserRole.ADMIN) -> ConnectionConfiguration:
    """Build a ConnectionConfiguration object from the keys defined in environment

    Args:
        role (UserRoles): admin, bsc_user or qilimanjaro_user

    Raises:
        MissingCredentialsException: missing or wrong credentials

    Returns:
        ConnectionConfiguration: instance with credentials for creating API instance
    """

    if role == UserRole.ADMIN:
        public_login_username = os.getenv("PUBLIC_LOGIN_ADMIN_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_ADMIN_KEY")

    elif role == UserRole.BSC:
        public_login_username = os.getenv("PUBLIC_LOGIN_BSC_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_BSC_KEY")

    elif role == UserRole.QILI:
        public_login_username = os.getenv("PUBLIC_LOGIN_QILI_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_QILI_KEY")

    elif role == UserRole.MACHINE:
        public_login_username = os.getenv("PUBLIC_LOGIN_MACHINE_USERNAME")
        public_login_key = os.getenv("PUBLIC_LOGIN_MACHINE_KEY")

    # previous try/except was not catching the error
    if public_login_username is None or public_login_key is None:
        raise MissingCredentialsException(
            "Login failed. Credentials were not provided in the environment or are not valid. Recall you need to define a environment variables for every user role."
        )

    return ConnectionConfiguration(username=public_login_username, api_key=public_login_key)
