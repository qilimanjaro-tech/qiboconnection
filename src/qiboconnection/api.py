""" Qilimanjaro Client API to communicate with the Qilimanjaro Global Quantum Services """
import json
from abc import ABC
from dataclasses import asdict
from datetime import datetime, timedelta
from time import sleep
from typing import Any, List, Optional, cast

import numpy as np
from numpy import typing as npt
from qibo.abstractions.states import AbstractState
from qibo.core.circuit import Circuit
from requests import HTTPError
from typeguard import typechecked

from qiboconnection.api_utils import log_job_status_info, parse_job_responses_to_results
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
from qiboconnection.live_plots import LivePlots
from qiboconnection.saved_experiment import SavedExperiment
from qiboconnection.saved_experiment_listing import SavedExperimentListing
from qiboconnection.typings.connection import ConnectionConfiguration
from qiboconnection.typings.job import JobResponse, JobStatus
from qiboconnection.typings.live_plot import (
    LivePlotAxis,
    LivePlotLabels,
    LivePlotType,
    PlottingResponse,
)
from qiboconnection.typings.saved_experiment import (
    SavedExperimentListingItemResponse,
    SavedExperimentRequest,
    SavedExperimentResponse,
)


class API(ABC):
    """Qilimanjaro Client API class to communicate with the Quantum Service"""

    API_VERSION = "v1"
    API_PATH = f"/api/{API_VERSION}"
    JOBS_CALL_PATH = "/jobs"
    CIRCUITS_CALL_PATH = "/circuits"
    DEVICES_CALL_PATH = "/devices"
    SAVED_EXPERIMENTS_CALL_PATH = "/save-experiments"
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
        self._saved_experiments: List[SavedExperiment] = []
        self._saved_experiments_listing: SavedExperimentListing | None = None

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
    def _add_or_update_single_device(self, device_id: int) -> Devices:
        """Requests the info of a specific device to the public api and updates its entry in _devices or creates a new
        device if it does not already exist. It *modifies* the internal `_devices` list *and returns* the modified list.

        Args:
            device_id: id of the device which info is to be retrieved from api

        Returns:
            Devices: modified (or created) devices object

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
            return self._devices
        if isinstance(self._devices, Devices):
            self._devices.add_or_update(new_device)
            return self._devices
        raise ValueError("Unexpected object in API._devices.")

    @typechecked
    def select_device_id(self, device_id: int) -> None:
        """Select a device from a given identifier

        Args:
            device_id (int): Device identifier

        """
        self._selected_devices = []
        self._devices = self._add_or_update_single_device(device_id=device_id)
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
            self._devices = self._add_or_update_single_device(device_id=device_id)
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
        self._devices = self._add_or_update_single_device(device_id=device_id)
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
        self._devices = self._add_or_update_single_device(device_id=device_id)
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
        experiment: dict | None = None,
        nshots: int = 10,
        device_ids: List[int] | None = None,
    ) -> List[int]:
        """Send a Qibo circuit to be executed on the remote service API. User should define either a *circuit* or an
        *experiment*. If both are provided, the function will fail.

        Args:
            circuit (Circuit): a Qibo circuit to execute
            experiment (dict): an Experiment description, result of Qililab's Experiment().to_dict() function.
            nshots (int): number of times the execution is to be done.
            device_ids (List[int]): list of devices where the execution should be performed. If set, any device set
             using API.select_device_id() will not be used. This will not update the selected devices.

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
                    self._devices = self._add_or_update_single_device(device_id=device_id)
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

    def _get_result(self, job_id: int) -> JobResponse:
        """Calls the API to get a job from a remote execution.

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved.

        Returns:
            JobResponse: typecasted backend response with the job info.
        """
        response, status_code = self._connection.send_get_auth_remote_api_call(path=f"{self.JOBS_CALL_PATH}/{job_id}")
        if status_code != 200:
            raise RemoteExecutionException(message="Job could not be retrieved.", status_code=status_code)

        return JobResponse(**cast(dict, response))

    @typechecked
    def get_result(self, job_id: int) -> AbstractState | npt.NDArray | dict | None:
        """Get a Job result from a remote execution

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported.
            ValueError: Your job failed.

        Returns:
            AbstractState | npt.NDArray | dict | None: The Job result as an Abstract State or None when it is not
            executed yet.
        """

        job_response = self._get_result(job_id=job_id)
        log_job_status_info(job_response=job_response)
        return parse_job_responses_to_results(job_responses=[job_response])[0]

    @typechecked
    def get_results(self, job_ids: List[int]) -> List[AbstractState | npt.NDArray | dict | None]:
        """Get a Job result from a remote execution

        Args:
            job_ids (List[int]): List of Job identifiers

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported

        Returns:
            Union[AbstractState, None]: The Job result as an Abstract State or None when it is not executed yet.
        """
        job_responses = [self._get_result(job_id) for job_id in job_ids]
        for job_reponse in job_responses:
            log_job_status_info(job_response=job_reponse)
        return parse_job_responses_to_results(job_responses=job_responses)

    def _wait_and_return_results(
        self, deadline: datetime, interval: int, job_ids: List[int]
    ) -> List[dict | Any | None]:
        """Try and recover results from the backend until all of them are finished (this is, with status being either
        ERROR or COMPLETED).

        Args:
            deadline (datetime): date at which this process should be interrupted
            interval (int): seconds to sleep between trials
            job_ids (List[int]): List of jobs to get the status of.

        Raises:
            TimeoutError: timeout seconds reached

        Returns:
            List[dict | None]: list of the results for each of the
        """
        while datetime.now() < deadline:
            job_responses = [self._get_result(job_id) for job_id in job_ids]
            job_responses_status = [job_response.status for job_response in job_responses]
            if set(job_responses_status).issubset({JobStatus.COMPLETED, JobStatus.ERROR}):
                return parse_job_responses_to_results(job_responses=job_responses)
            sleep(interval)
        raise TimeoutError("Server did not execute the jobs in time.")

    def execute_and_return_results(
        self,
        circuit: Circuit | None = None,
        experiment: dict | None = None,
        nshots: int = 10,
        device_ids: List[int] | None = None,
        timeout: int = 3600,
        interval: int = 60,
    ) -> List[dict | Any | None]:
        """Executes a `circuit` or `experiment` the same way as :func:`qiboconnection.API.execute`.

        Args:
            circuit (Circuit): a Qibo circuit to execute
            experiment (dict): an Experiment description, result of Qililab's Experiment().to_dict() function.
            nshots (int): number of times the execution is to be done.
            device_ids (List[int]): list of devices where the execution should be performed. If set, any device set
             using API.select_device_id() will not be used. This will not update the selected
            timeout (int): seconds passed which the function should be interrupted with an error.
            interval (int): seconds to wait between checking with the backend if the results are ready. If the task is
              expected to last for tens of minutes, this should be set to, at least, 60 seconds.

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported
            TimeoutError: timeout seconds reached

        Returns:
            Union[AbstractState, None]: The Job result as an Abstract State or None when it is not executed yet.

        """

        deadline = datetime.now() + timedelta(seconds=timeout)
        job_ids = self.execute(
            circuit=circuit,
            experiment=experiment,
            nshots=nshots,
            device_ids=device_ids,
        )
        return self._wait_and_return_results(deadline=deadline, interval=interval, job_ids=job_ids)

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
            plot_id: id of the plot to send points to
            x: x coord of the point to send info to
            y: y coord of the point to send info to
            z: z coord of the point to send info to

        Returns:
            None
        """
        return self._live_plots.send_data(plot_id=plot_id, x=x, y=y, z=z)

    @typechecked
    def save_experiment(
        self,
        name: str | None,
        description: str | None,
        experiment_dict: dict,
        results_dict: dict,
        device_id: int,
        user_id: int,
        favourite: bool = False,
    ):
        """Save an experiment and its results into the database af our servers, for them to be easily recovered when
        needed.

        Args:
            name: Name the experiment is going to be saved with.
            description: Short descriptive text to more easily identify this specific experiment instance.
            experiment_dict: Serialized qililab experiment (using its `.to_dict()` method)
            results_dict: Serialized qililab results (using their `.to_dict()` method )
            device_id: Id of the device the experiment was executed in
            user_id: Id of the user that is executing the experiment
            favourite: Whether to save the experiment as favourite

        Returns:
            newly created experiment id

        """

        saved_experiment = SavedExperiment(
            id=None,
            name=name,
            description=description,
            experiment=experiment_dict,
            results=results_dict,
            device_id=device_id,
            user_id=user_id,
        )

        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self.SAVED_EXPERIMENTS_CALL_PATH,
            data=asdict(saved_experiment.saved_experiment_request(favourite=favourite)),
        )
        if status_code != 201:
            raise RemoteExecutionException(message="Experiment could not be saved.", status_code=status_code)
        logger.debug("Experiment saved successfully.")

        saved_experiment.id = response["saved_experiment_id"]

        self._saved_experiments = [saved_experiment]
        return saved_experiment.id

    def _get_list_saved_experiments_response(self) -> List[SavedExperimentListingItemResponse]:
        response, status_code = self._connection.send_get_auth_remote_api_call(path=self.SAVED_EXPERIMENTS_CALL_PATH)
        if status_code != 200:
            raise RemoteExecutionException(message="Experiment could not be saved.", status_code=status_code)

        # TODO: get all paginated results!
        return [SavedExperimentListingItemResponse(**item) for item in response["items"]]

    @typechecked
    def list_saved_experiments(self) -> SavedExperimentListing:
        """List all available devices

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All available Devices
        """
        saved_experiments_list_response = self._get_list_saved_experiments_response()
        # !!! TODO: handle all items, not only the returned on first call
        self._saved_experiments_listing = SavedExperimentListing.from_response(saved_experiments_list_response)
        return self._saved_experiments_listing

    @typechecked
    def _get_saved_experiment_response(self, saved_experiment_id: int):
        """Gets complete information of a single saved experiment

        Raises:
            RemoteExecutionException: SavedExperiment could not be retrieved

        Returns:
            SavedExperimentResponse: All available Devices"""
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self.SAVED_EXPERIMENTS_CALL_PATH}/{saved_experiment_id}"
        )
        if status_code != 200:
            raise RemoteExecutionException(message="Job could not be retrieved.", status_code=status_code)
        return SavedExperimentResponse(**response)

    @typechecked
    def get_saved_experiment(self, saved_experiment_id: int):
        """Get full information of a single experiment

        Raises:
            RemoteExecutionException: SavedExperiments could not be retrieved

        Returns:
            Devices: All available Devices
        """
        saved_experiment = SavedExperiment.from_response(
            self._get_saved_experiment_response(saved_experiment_id=saved_experiment_id)
        )
        self._saved_experiments = [saved_experiment]
        return saved_experiment

    @typechecked
    def get_saved_experiments(self, saved_experiment_ids: List[int] | npt.NDArray[int]) -> List[SavedExperiment]:
        """Get full information of the chosen experiments

        Raises:
            RemoteExecutionException: SavedExperiments could not be retrieved

        Returns:
            Devices: All available Devices
        """
        self._saved_experiments = [
            SavedExperiment.from_response(self._get_saved_experiment_response(saved_experiment_id=saved_experiment_id))
            for saved_experiment_id in saved_experiment_ids
        ]
        return self._saved_experiments
