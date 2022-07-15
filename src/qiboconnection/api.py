""" Qilimanjaro Client API to communicate with the Qilimanajaro Global Quantum Services """
import json
from abc import ABC
from dataclasses import asdict
from typing import List, Optional, cast

import numpy as np
import numpy.typing as npt
from qibo.abstractions.states import AbstractState
from qibo.core.circuit import Circuit
from requests import HTTPError
from typeguard import typechecked

from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.devices.device import Device
from qiboconnection.devices.devices import Devices
from qiboconnection.devices.offline_device import OfflineDevice
from qiboconnection.devices.quantum_device import QuantumDevice
from qiboconnection.devices.simulator_device import SimulatorDevice
from qiboconnection.devices.util import create_device
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.job import Job
from qiboconnection.job_result import JobResult
from qiboconnection.live_plots import LivePlots
from qiboconnection.typings.connection import ConnectionConfiguration
from qiboconnection.typings.experiment import Experiment
from qiboconnection.typings.job import JobResponse, JobStatus
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotType,
    PlottingResponse,
)


class API(ABC):
    """Qilimanjaro Client API class to communicate with the Quantum Service"""

    API_VERSION = "v1"
    API_PATH = f"/api/{API_VERSION}"
    JOBS_CALL_PATH = "/jobs"
    CIRCUITS_CALL_PATH = "/circuits"
    DEVICES_CALL_PATH = "/devices"
    PING_CALL_PATH = "/status"
    LIVE_PLOTTING_PATH = "/live-plotting"

    @typechecked
    def __init__(
        self,
        configuration: Optional[ConnectionConfiguration] = None,
    ):
        self._connection = Connection(configuration=configuration, api_path=self.API_PATH)
        self._devices: Devices | None = None
        self._jobs: List[Job] = []
        self._selected_devices: List[Device] | None = None
        self._live_plots: LivePlots = LivePlots()

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
        self._devices = Devices([create_device(device_input=device_input) for device_input in response["items"]])
        return self._devices

    @typechecked
    def _add_or_update_single_device(self, device_id: int):
        """Requests the info of a specific device to the public api and updates its entry in _devices or creates a new
        device if it does not already exist.

        Args:
            device_id: id of the device which info is to be retrieved from api

        Raises:
            RemoteExecutionException: Devices could not be retrieved
            ValueError: Unexpected object in API._devices.
        """
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self.DEVICES_CALL_PATH}/{device_id}"
        )

        if status_code != 200:
            raise RemoteExecutionException(message="Devices could not be retrieved.", status_code=status_code)

        new_device = create_device(device_input=response)

        if self._devices is None:
            self._devices = Devices([new_device])
        elif isinstance(self._devices, Devices):
            self._devices.add_or_update(new_device)

        if self._devices is None:
            raise ValueError("Unexpected object in API._devices.")

    @typechecked
    def select_device_id(self, device_id: int) -> None:
        """Select a device from a given identifier

        Args:
            device_id (int): Device identifier

        """
        self._add_or_update_single_device(device_id=device_id)
        self._devices = cast(Devices, self._devices)
        try:
            selected_device = self._devices.select_device(device_id=device_id)
            self._selected_devices = [selected_device]
            logger.info("Device %s selected.", selected_device.name)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))["detail"])
            raise ex

    @typechecked
    def select_device_ids(self, device_ids: List[int]) -> None:
        """Select a device from a given identifier

        Args:
            device_ids (int): List of device identifiers
        """
        self._selected_devices = []
        for device_id in device_ids:
            self._add_or_update_single_device(device_id=device_id)
            self._devices = cast(Devices, self._devices)
            try:
                self._selected_devices.append(self._devices.select_device(device_id=device_id))
            except HTTPError as ex:
                logger.error(json.loads(str(ex))["detail"])
                raise ex
        linebreak = "\n"
        text = (
            f"Selected devices:{linebreak} -{linebreak.join([f' -{device.name}' for device in self._selected_devices])}"
        )
        logger.info(text)

    @typechecked
    def block_device_id(self, device_id: int) -> None:
        """Blocks a device to avoid others to use it

        Args:
            device_id (int): Device identifier
        """
        self._add_or_update_single_device(device_id=device_id)
        self._devices = cast(Devices, self._devices)
        try:
            self._devices.block_device(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))["detail"])
            raise ex

    @typechecked
    def release_device(self, device_id: int) -> None:
        """Releases a device to let others use it

        Args:
            device_id (int): Device identifier
        """
        self._add_or_update_single_device(device_id=device_id)
        self._devices = cast(Devices, self._devices)
        try:
            self._devices.release_device(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))["detail"])
            raise ex

    # @typechecked
    # def execute_program(self, program: ProgramDefinition) -> Any:
    #     """Send a remote experiment from the provided algorithm to be executed on the remote service API
    #
    #     Args:
    #         program (ProgramDefinition): program details conforming the experiment
    #
    #     Returns:
    #         Any: Result of the algorithm executed remotely
    #     """
    #     job = Job(
    #         program=program,
    #         user=self._connection.user,
    #         device=cast(Device, self._selected_device),
    #     )
    #
    #     logger.debug("Sending experiment for a remote execution...")
    #     response, status_code = self._connection.send_post_auth_remote_api_call(
    #         path=self.JOBS_CALL_PATH, data=job.job_request
    #     )
    #     if status_code != 201:
    #         raise RemoteExecutionException(message="Experiment could not be executed.", status_code=status_code)
    #     logger.debug("Experiment completed successfully.")
    #     job.update_with_job_response(job_response=JobResponse(**cast(dict, response)))
    #     self._jobs.append(job)
    #
    #     return job.result

    @typechecked
    def execute(
        self,
        circuit: Circuit | None = None,
        experiment: Experiment | None = None,
        nshots: int = 10,
        device_ids: List[int] | None = None,
    ) -> List[int]:
        """Send a Qibo circuit to be executed on the remote service API. User should define either a *circuit* or an
        *experiment*. If both are provided, the function will fail.

        Args:
            circuit (Circuit): a Qibo circuit to execute
            experiment (Experiment): an Experiment description
            nshots (int): number of times the execution is to be done.
            device_ids (List[int]): list of devices where the execution should be performed. If set, any device set
             using API.select_device_id() will not be used. This will not update the selecte

        Returns:
            List[int]: list of job ids
        Raises:
            ValueError: Both circuit and experiment were provided, but execute() only takes at most of them.
            ValueError: Neither of experiment or circuit were provided, but execute() only takes at least one of them.
        """

        # Ensure provided selected_devices are valid. If not provided, use the ones selected by API.select_device_id.
        selected_devices: List[Device | QuantumDevice | SimulatorDevice | OfflineDevice] = []
        if device_ids is not None:
            for device_id in device_ids:
                try:
                    self._add_or_update_single_device(device_id=device_id)
                    self._devices = cast(Devices, self._devices)
                    selected_devices.append(self._devices.select_device(device_id=device_id))
                except HTTPError as ex:
                    logger.error(json.loads(str(ex))["detail"])
                    raise ex
        else:
            selected_devices = cast(
                List[Device | QuantumDevice | SimulatorDevice | OfflineDevice], self._selected_devices
            )

        jobs = [
            Job(
                circuit=circuit,
                experiment=experiment,
                nshots=nshots,
                user=self._connection.user,
                device=cast(Device, device),
            )
            for device in selected_devices
        ]

        job_ids = []
        logger.debug("Sending qibo circuits for a remote execution...")
        for job in jobs:
            response, status_code = self._connection.send_post_auth_remote_api_call(
                path=self.CIRCUITS_CALL_PATH, data=asdict(job.job_request)
            )
            if status_code != 201:
                raise RemoteExecutionException(
                    message=f"Circuit {job.job_id} could not be executed.", status_code=status_code
                )
            logger.debug("Job circuit queued successfully.")
            job.id = response["job_id"]
            self._jobs.append(job)
            job_ids.append(job.id)
        return job_ids

    @typechecked
    def get_results(self, job_ids: List[int]) -> List[AbstractState | npt.NDArray | None]:
        """Get a Job result from a remote execution

        Args:
            job_ids (List[int]): List of Job identifiers

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported

        Returns:
            Union[AbstractState, None]: The Job result as an Abstract State or None when it is not executed yet.
        """
        return [self.get_result(job_id) for job_id in job_ids]

    @typechecked
    def get_result(self, job_id: int) -> AbstractState | npt.NDArray | None:
        """Get a Job result from a remote execution

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved.
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
            logger.warning("Your job is still pending. Job queue position: %s", job_response.queue_position)
            return None
        if status == JobStatus.RUNNING:
            logger.warning("Your job is still running.")
            return None
        if status == JobStatus.NOT_SENT:
            logger.warning("Your job has not been sent.")
            return None
        if status == JobStatus.ERROR:
            logger.error("Your job failed.")
            return None
        if status == JobStatus.COMPLETED:
            logger.warning("Your job is completed.")
            raw_result = JobResult(job_id=job_id, http_response=job_response.result).data
            return raw_result[0] if isinstance(raw_result, List) else raw_result
        raise ValueError(f"Job status not supported: {status}")

    @typechecked
    def create_liveplot(
        self,
        plot_type: str = LivePlotType.LINES.value,
        title: str | None = None,
        x_label: str | None = None,
        y_label: str | None = None,
        z_label: str | None = None,
        x_axis: npt.NDArray[np.int_] | List[int] | None = None,
        y_axis: npt.NDArray[np.int_] | List[int] | None = None,
    ):
        """Creates a LivePlot of *plot_type* type at which we will be able to send points to plot.

        Attributes:
            plot_type: LivePlotType
            title: title for the plot
            x_label: title for the x label
            y_label: title for the y label
            z_label: title for the z label
            x_axis: range of values for the x_axis
            y_axis: range of values for the y_axis


        Raises:
            RemoteExecutionException: Live-plotting connection data could not be retrieved

        Returns:
            int: id of the just created plot
        """
        # Get info from PublicAPI
        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=f"{self.LIVE_PLOTTING_PATH}", data={}
        )
        if status_code != 200:
            raise RemoteExecutionException(
                message="Live-plotting connection data could not be retrieved.", status_code=status_code
            )
        plotting_response = PlottingResponse.from_response(**response)
        self._live_plots.create_live_plot(
            plot_id=plotting_response.plot_id,
            websocket_url=plotting_response.websocket_url,
            plot_type=LivePlotType(plot_type),
            labels=LivePlotLabels(title=title, x_label=x_label, y_label=y_label, z_label=z_label),
            axis=LivePlotAxis(x_axis=x_axis, y_axis=y_axis),
        )
        return plotting_response.plot_id

    @typechecked
    def send_plot_points(
        self,
        plot_id: int,
        x: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        y: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int,
        z: npt.NDArray[np.float_ | np.int_] | list[float] | list[int] | float | int | None = None,
    ):
        """Sends point(s) to a specific plot.
        Args:
            plot_id: Id of the plot to send points to
            x: x coord of the point to send info to
            y: y coord of the point to send info to
            z: z coord of the point to send info to

        Returns:
            None
        """
        return self._live_plots.send_data(plot_id=plot_id, x=x, y=y, z=z)
