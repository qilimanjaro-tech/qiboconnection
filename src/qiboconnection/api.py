""" Qilimanjaro Client API to communicate with the Qilimanajaro Global Quantum Services """
import json
from abc import ABC
from typing import Any, List, Optional, Union, cast

from qibo.abstractions.states import AbstractState
from qibo.core.circuit import Circuit
from requests import HTTPError
from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.device import Device
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.util import create_device
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.job import Job
from qiboconnection.job_result import JobResult
from qiboconnection.platform_manager import PlatformManager
from qiboconnection.typings.algorithm import ProgramDefinition
from qiboconnection.typings.connection import ConnectionConfiguration
from qiboconnection.typings.device import (
    OfflineDeviceInput,
    QuantumDeviceInput,
    SimulatorDeviceInput,
)
from qiboconnection.typings.job import JobResponse, JobStatus


class API(ABC):
    """Qilimanjaro Client API class to communicate with the Quantum Service"""

    API_VERSION = "v1"
    API_PATH = f"/api/{API_VERSION}"
    JOBS_CALL_PATH = "/jobs"
    CIRCUITS_CALL_PATH = "/circuits"
    DEVICES_CALL_PATH = "/devices"
    PING_CALL_PATH = "/status"

    @typechecked
    def __init__(self, configuration: Optional[ConnectionConfiguration | None] = None):
        self._connection = Connection(configuration=configuration, api_path=self.API_PATH)
        self._devices: Devices | None = None
        self._jobs: List[Job] = []
        self._selected_device: Device | None = None
        self._platform_manager = PlatformManager()

    @property
    def jobs(self) -> List[Job]:
        """List all jobs launched to the API

        Returns:
            List[Job]: List of Jobs launched
        """
        return self._jobs

    @property
    def last_job(self) -> Job:
        """Returns the last job launched

        Returns:
            Job: last Job launched
        """
        return self._jobs[-1]

    def ping(self) -> str:
        """Checks if the connection is alive and response OK when it is.

        Returns:
            str: OK when connection is alive or raise Connection Error.
        """
        response, status_code = self._connection.send_get_remote_call(path=self.PING_CALL_PATH)
        if status_code != 200:
            raise ConnectionException("Error connecting to Qilimanjaro API")
        return response

    @typechecked
    def list_devices(self) -> Devices:
        """List all available devices

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All available Devices
        """
        response, status_code = self._connection.send_get_auth_remote_api_call(path=self.DEVICES_CALL_PATH)
        if status_code != 200:
            raise RemoteExecutionException(message="Devices could not be retrieved.", status_code=status_code)

        # !!! TODO: handle all items, not only the returned on first call
        self._devices = Devices(
            [
                create_device(
                    device_input=cast(Union[QuantumDeviceInput, SimulatorDeviceInput, OfflineDeviceInput], device_input)
                )
                for device_input in response["items"]
            ]
        )
        return self._devices

    @typechecked
    def _add_or_update_single_device(self, device_id: int):
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self.DEVICES_CALL_PATH}/{device_id}"
        )

        if status_code != 200:
            raise RemoteExecutionException(message="Devices could not be retrieved.", status_code=status_code)

        new_device = create_device(
            device_input=cast(Union[QuantumDeviceInput, SimulatorDeviceInput, OfflineDeviceInput], response)
        )

        if self._devices is None:
            self._devices = Devices([new_device])
        else:
            self._devices.add_or_update(new_device)

    @typechecked
    def select_device_id(self, device_id: int) -> None:
        """Select a device from a given identifier

        Args:
            device_id (int): Device identifier

        Raises:
            ValueError: No devices collected. Please call 'list_devices' first.
        """
        self._add_or_update_single_device(device_id=device_id)
        try:
            if self._devices is None:
                raise ValueError("No devices collected. Please call 'list_devices' first.")
            self._selected_device = self._devices.select_device(device_id=device_id)
            logger.info("Device %s selected.", self._selected_device.name)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))["detail"])

    @typechecked
    def block_device_id(self, device_id: int) -> None:
        """Blocks a device to avoid others to use it

        Args:
            device_id (int): Device identifier

        Raises:
            ValueError: No devices collected. Please call 'list_devices' first.
        """
        self._add_or_update_single_device(device_id=device_id)
        try:
            if self._devices is None:
                raise ValueError("No devices collected. Please call 'list_devices' first.")
            self._devices.block_device(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))["detail"])

    @typechecked
    def release_device(self, device_id: int) -> None:
        """Releases a device to let others use it

        Args:
            device_id (int): Device identifier

        Raises:
            ValueError: No devices collected. Please call 'list_devices' first.
        """
        if self._devices is None:
            raise ValueError("No devices collected. Please call 'list_devices' first.")
        self._devices.release_device(connection=self._connection, device_id=device_id)

    @typechecked
    def execute_program(self, program: ProgramDefinition) -> Any:
        """Send a remote experiment from the provided algorithm to be executed on the remote service API

        Args:
            program (ProgramDefinition): program details conforming the experiment

        Returns:
            Any: Result of the algorithm executed remotely
        """
        job = Job(
            program=program,
            user=self._connection.user,
            device=cast(Device, self._selected_device),
        )

        logger.debug("Sending experiment for a remote execution...")
        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self.JOBS_CALL_PATH, data=job.job_request
        )
        if status_code != 201:
            raise RemoteExecutionException(message="Experiment could not be executed.", status_code=status_code)
        logger.debug("Experiment completed successfully.")
        job.update_with_job_response(job_response=JobResponse(**cast(dict, response)))
        self._jobs.append(job)

        return job.result

    @typechecked
    def execute(self, circuit: Circuit) -> int:
        """Send a Qibo circuit to be executed on the remote service API

        Args:
            circuit (Circuit): a Qibo circuit

        Returns:
            int: Job id
        """
        job = Job(
            circuit=circuit,
            user=self._connection.user,
            device=cast(Device, self._selected_device),
        )

        logger.debug("Sending qibo circuit for a remote execution...")
        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self.CIRCUITS_CALL_PATH, data=job.job_request
        )
        if status_code != 201:
            raise RemoteExecutionException(message="Circuit could not be executed.", status_code=status_code)
        logger.debug("Job circuit queued successfully.")
        job.id = response["job_id"]
        self._jobs.append(job)
        return job.id

    @typechecked
    def get_result(self, job_id: int) -> Union[AbstractState, None]:
        """Get a Job result from a remote execution

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved."
            ValueError: Job status not supported

        Returns:
            Union[AbstractState, None]: The Job result as an Abstract State or None when it is not executed yet.
        """
        response, status_code = self._connection.send_get_auth_remote_api_call(path=f"{self.JOBS_CALL_PATH}/{job_id}")
        if status_code != 200:
            raise RemoteExecutionException(message="Job could not be retrieved.", status_code=status_code)

        job_response = JobResponse(**cast(dict, response))
        status = job_response.status if isinstance(job_response.status, JobStatus) else JobStatus(job_response.status)
        if status == JobStatus.PENDING:
            logger.info("Your job is still pending. Job queue position: %s", job_response.queue_position)
            return None
        if status == JobStatus.RUNNING:
            logger.info("Your job is still running.")
            return None
        if status == JobStatus.NOT_SENT:
            logger.info("Your job has not been sent.")
            return None
        if status == JobStatus.ERROR:
            logger.info("Your job failed.")
            return None
        if status == JobStatus.COMPLETED:
            logger.info("Your job is completed.")
            result = JobResult(job_id=job_id, http_response=job_response.result).data
            return result[0] if isinstance(result, List) else result
        raise ValueError(f"Job status not supported: {status}")

    ##############################
    ##    PLATFORM FUNCTIONS    ##
    ##############################

    def create_platform_schema(self) -> dict:
        """Create a new Platform schema using a remote connection

        Returns:
            dict: returning platform schema with its unique identifier
        """

        return self._platform_manager.create_platform_schema()

    def list_platform_schemas(self) -> List[dict]:
        """List all platform schemas in the system

        Returns:
            List[dict]: List of platform schemas dictionaries
        """

        return self._platform_manager.list_platform_schemas()

    def create_platform_settings(self, platform_schema_id: int, platform_settings: dict) -> dict:
        """Create a new Platform Settings associated to a Platform using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings (dict): Platform Settings as a dictionary to be sent to the remote connection

        Returns:
            dict: returning platform settings with its unique identifier
        """
        return self._platform_manager.create_platform_settings(
            platform_schema_id=platform_schema_id, platform_settings=platform_settings
        )

    def read_platform_settings(self, platform_schema_id: int, platform_settings_id: int) -> dict:
        """Load a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """

        return self._platform_manager.read_platform_settings(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        )

    def update_platform_settings(
        self, platform_schema_id: int, platform_settings_id: int, platform_settings: dict
    ) -> dict:
        """Updates a new Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier
            platform_settings (dict): dictionary containing the data. It should be all platform settings data without the id

        Returns:
            dict: returning platform settings
        """

        return self._platform_manager.update_platform_settings(
            platform_schema_id=platform_schema_id,
            platform_settings_id=platform_settings_id,
            platform_settings=platform_settings,
        )

    def delete_platform_settings(self, platform_schema_id: int, platform_settings_id: int) -> None:
        """Deletes a Platform Settings using a remote connection

        Args:
            platform_schema_id (int): Platform unique identifier
            platform_settings_id (int): Platform Settings unique identifier

        Returns:
            dict: returning platform settings
        """

        self._platform_manager.delete_platform_settings(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        )
