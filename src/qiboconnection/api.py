# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Qiboconnection API class."""

# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=no-member

import json
from abc import ABC
from dataclasses import asdict
from datetime import datetime, timedelta
from time import sleep
from typing import Any, List, cast

import numpy as np
from numpy import typing as npt
from qibo.models.circuit import Circuit
from qibo.states import CircuitResult
from requests import HTTPError
from typeguard import typechecked

from qiboconnection.api_utils import log_job_status_info, parse_job_responses_to_results
from qiboconnection.config import logger
from qiboconnection.connection import Connection
from qiboconnection.constants import API_CONSTANTS, REST, REST_ERROR
from qiboconnection.errors import ConnectionException, RemoteExecutionException
from qiboconnection.models import Job, JobListing, LivePlots, Runcard, SavedExperiment, SavedExperimentListing
from qiboconnection.models.devices import Device, Devices, OfflineDevice, QuantumDevice, SimulatorDevice, create_device
from qiboconnection.typings.connection import ConnectionConfiguration
from qiboconnection.typings.enums import JobStatus
from qiboconnection.typings.job_data import JobData
from qiboconnection.typings.live_plot import LivePlotAxis, LivePlotLabels, LivePlotType
from qiboconnection.typings.responses import (
    JobListingItemResponse,
    RuncardResponse,
    SavedExperimentListingItemResponse,
    SavedExperimentResponse,
)
from qiboconnection.typings.responses.job_response import JobResponse
from qiboconnection.typings.responses.plotting_response import PlottingResponse
from qiboconnection.util import unzip


class API(ABC):
    """Qilimanjaro Client API class to communicate with the Quantum Service."""

    _API_VERSION = "v1"
    _API_PATH = f"/api/{_API_VERSION}"
    _JOBS_CALL_PATH = "/jobs"
    _CIRCUITS_CALL_PATH = "/circuits"
    _DEVICES_CALL_PATH = "/devices"
    _SAVED_EXPERIMENTS_CALL_PATH = "/saved_experiments"
    _RUNCARDS_CALL_PATH = "/runcards"
    _PING_CALL_PATH = "/status"
    _LIVE_PLOTTING_PATH = "/live-plotting"

    @typechecked
    def __init__(
        self,
        configuration: ConnectionConfiguration,
    ):
        self._connection = Connection(configuration=configuration, api_path=self._API_PATH)
        self._devices: Devices | None = None
        self._jobs: List[Job] = []
        self._jobs_listing: JobListing | None = None
        self._selected_devices: List[Device] | None = None
        self._live_plots: LivePlots = LivePlots()
        self._saved_experiment: SavedExperiment | None = None
        self._saved_experiments_listing: SavedExperimentListing | None = None
        self._runcard: Runcard | None = None

    @classmethod
    def login(cls, username: str, api_key: str):
        """Log into QaaS using your username and api_key

        Args:
            username: username of your account
            api_key: you access key

        Returns:
            Authenticated API instance
        """
        _configuration = ConnectionConfiguration(username=username, api_key=api_key)
        return cls(configuration=_configuration)

    # LOCAL INFORMATION

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

    @property
    def _last_saved_experiment(self) -> SavedExperiment | None:
        """Returns the last saved experiment of the current session, in case there has been one.

        Returns:
            SavedExperiment | None: last saved experiment
        """
        return self._saved_experiment

    @property
    def _last_saved_experiment_listing(self) -> SavedExperimentListing | None:
        """Returns the last experiment listing downloaded in the current session, in case there has been one.

        Returns:
            SavedExperimentListing | None: last downloaded experiment listing
        """
        return self._saved_experiments_listing

    @property
    def last_runcard(self) -> Runcard | None:
        """Returns the last runcard uploaded in the current session, in case there has been one.

        Returns:
            Runcard | None: last uploaded runcard
        """
        return self._runcard

    @property
    def user_id(self) -> int:
        """Exposes the id of the authenticated user

        Returns:
            int: user ir

        Raises:
            ValueError: User does not have user_id
        """
        if self._connection.user.user_id is None:
            raise ValueError("User does not have user_id")

        return self._connection.user.user_id

    # PING

    def ping(self) -> str:
        """Checks if the connection is alive and response OK when it is.

        Returns:
            str: OK when connection is alive or raise Connection Error.
        """
        response, status_code = self._connection.send_get_remote_call(path=self._PING_CALL_PATH)
        if status_code != 200:
            raise ConnectionException("Error connecting to Qilimanjaro API")
        return response

    # DEVICES

    @typechecked
    def list_devices(self) -> Devices:
        """List all available devices

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All available Devices
        """
        responses, status_codes = unzip(
            self._connection.send_get_auth_remote_api_call_all_pages(path=self._DEVICES_CALL_PATH)
        )
        for status_code in status_codes:
            if status_code != 200:
                raise RemoteExecutionException(message="Devices could not be retrieved.", status_code=status_code)

        items = [item for response in responses for item in response[REST.ITEMS]]
        self._devices = Devices([create_device(device_input=device_input) for device_input in items])
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
            path=f"{self._DEVICES_CALL_PATH}/{device_id}"
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
            logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
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
                logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
                raise ex
        linebreak = "\n"
        text = (
            f"Selected devices:{linebreak} -{linebreak.join([f' -{device.name}' for device in self._selected_devices])}"
        )
        logger.info(text)

    @typechecked
    def set_device_to_online(self, device_id: int) -> None:
        """Sets a device into online mode, allowing external traffic and blocking manual manipulation.
        .. warning::

            This method is only available for admin members.

        Args:
            device_id (int): Device identifier
        """
        self._devices = self._add_or_update_single_device(device_id=device_id)
        try:
            self._devices.set_device_to_online(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
            raise ex

    @typechecked
    def set_device_to_maintenance(self, device_id: int) -> None:
        """Sets a device in maintenance mode, blocking external traffic and allowing for manual manipulation.

        .. warning::

            This method is only available for admin members.

        Args:
            device_id (int): Device identifier

        """
        self._devices = self._add_or_update_single_device(device_id=device_id)
        try:
            self._devices.set_device_to_maintenance(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
            raise ex

    @typechecked
    def block_device_id(self, device_id: int) -> None:
        """Blocks a device to avoid others to manually use it.
         .. warning::

            This method is only available for Qilimanjaro members.

        Args:
            device_id (int): Device identifier
        """
        self._devices = self._add_or_update_single_device(device_id=device_id)
        try:
            self._devices.block_device(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
            raise ex

    @typechecked
    def release_device(self, device_id: int) -> None:
        """Releases a device to let others manually using it.

        .. warning::

            This method is only available for Qilimanjaro members.

        Args:
            device_id (int): Device identifier
        """
        self._devices = self._add_or_update_single_device(device_id=device_id)
        try:
            self._devices.release_device(connection=self._connection, device_id=device_id)
        except HTTPError as ex:
            logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
            raise ex

    # REMOTE EXECUTIONS

    @typechecked
    def execute(
        self,
        circuit: Circuit | List[Circuit] | None = None,
        experiment: dict | None = None,
        nshots: int = 10,
        device_ids: List[int] | None = None,
    ) -> List[int]:
        """Send a Qibo circuit(s) to be executed on the remote service API. User should define either a *circuit* or an
        *experiment*. If both are provided, the function will fail.

        Args:
            circuit (Circuit or List[Circuit]): a Qibo circuit to execute
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
                    logger.error(json.loads(str(ex))[REST_ERROR.DETAIL])
                    raise ex
        else:
            selected_devices = cast(
                List[Device | QuantumDevice | SimulatorDevice | OfflineDevice], self._selected_devices
            )
        if not selected_devices:
            raise ValueError("No devices were selected for execution.")
        if not isinstance(circuit, list):
            circuit = [circuit]
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
                path=self._CIRCUITS_CALL_PATH, data=asdict(job.job_request)
            )
            if status_code != 201:
                raise RemoteExecutionException(
                    message=f"Circuit {job.job_id} could not be executed.", status_code=status_code
                )
            logger.debug("Job circuit queued successfully.")
            job.id = response[API_CONSTANTS.JOB_ID]
            self._jobs.append(job)
            job_ids.append(job.id)
        return job_ids

    def _get_job(self, job_id: int) -> JobResponse:
        """Calls the API to get a job from a remote execution.

        Args:
            job_id (int): Job identifier.

        Raises:
            RemoteExecutionException: Job could not be retrieved.

        Returns:
            JobResponse: type-casted backend response with the job info.
        """
        response, status_code = self._connection.send_get_auth_remote_api_call(path=f"{self._JOBS_CALL_PATH}/{job_id}")
        if status_code != 200:
            raise RemoteExecutionException(message="Job could not be retrieved.", status_code=status_code)

        return JobResponse.from_kwargs(**cast(dict, response))

    @typechecked
    def get_result(self, job_id: int) -> CircuitResult | npt.NDArray | dict | None:
        """Get a Job result from a remote execution

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported.s
            ValueError: Your job failed.

        Returns:
            CircuitResult | npt.NDArray | dict | None: The Job result as an Abstract State or None when it is not
            executed yet.
        """

        job_response = self._get_job(job_id=job_id)
        log_job_status_info(job_response=job_response)
        return parse_job_responses_to_results(job_responses=[job_response])[0]

    @typechecked
    def get_results(self, job_ids: List[int]) -> List[CircuitResult | npt.NDArray | dict | None]:
        """Get a Job result from a remote execution

        Args:
            job_ids (List[int]): List of Job identifiers

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported

        Returns:
            Union[CircuitResult, None]: The Job result as an Abstract State or None when it is not executed yet.
        """
        job_responses = [self._get_job(job_id) for job_id in job_ids]
        for job_response in job_responses:
            log_job_status_info(job_response=job_response)
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
            job_responses = [self._get_job(job_id) for job_id in job_ids]
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
            experiment (dict): an Experiment description, results of Qililab's Experiment().to_dict() function.
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
            Union[CircuitResult, None]: The Job result as an Abstract State or None when it is not executed yet.

        """

        deadline = datetime.now() + timedelta(seconds=timeout)
        job_ids = self.execute(
            circuit=circuit,
            experiment=experiment,
            nshots=nshots,
            device_ids=device_ids,
        )
        return self._wait_and_return_results(deadline=deadline, interval=interval, job_ids=job_ids)

    # REMOTE PLOTTING

    @typechecked
    async def _create_liveplot(
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
            path=f"{self._LIVE_PLOTTING_PATH}", data={}
        )
        if status_code != 200:
            raise RemoteExecutionException(
                message="Live-plotting connection data could not be retrieved.", status_code=status_code
            )
        plotting_response = PlottingResponse.from_response(**response)
        await self._live_plots.create_live_plot(
            plot_id=plotting_response.plot_id,
            websocket_url=plotting_response.websocket_url,
            plot_type=LivePlotType(plot_type),
            labels=LivePlotLabels(title=title, x_label=x_label, y_label=y_label, z_label=z_label),
            axis=LivePlotAxis(x_axis=x_axis, y_axis=y_axis),
        )
        return plotting_response.plot_id

    @typechecked
    async def _send_plot_points(
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
        return await self._live_plots.send_data(plot_id=plot_id, x=x, y=y, z=z)

    # SAVED EXPERIMENTS

    @typechecked
    def _save_experiment(
        self,
        name: str,
        description: str,
        experiment_dict: dict,
        results_dict: dict,
        device_id: int,
        user_id: int,
        qililab_version: str,
        favourite: bool = False,
    ):
        """Save an experiment and its results into the database af our servers, for them to be easily recovered when
        needed.
        Default behaviour is to create one if no previous occurrence with the same name exists, or to create a new one
        if none exists.

        Args:
            name: Name the experiment is going to be saved with.
            description: Short descriptive text to more easily identify this specific experiment instance.
            experiment_dict: Serialized qililab experiment (using its `.to_dict()` method)
            results_dict: Serialized qililab results (using their `.to_dict()` method )
            device_id: Id of the device the experiment was executed in
            user_id: Id of the user that is executing the experiment
            qililab_version: version of qililab the experiment was executed with
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
            qililab_version=qililab_version,
        )

        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self._SAVED_EXPERIMENTS_CALL_PATH,
            data=asdict(saved_experiment.saved_experiment_request(favourite=favourite)),
        )
        if status_code != 201:
            raise RemoteExecutionException(message="Experiment could not be saved.", status_code=status_code)
        logger.debug("Experiment saved successfully.")

        saved_experiment.id = response[API_CONSTANTS.SAVED_EXPERIMENT_ID]

        self._saved_experiment = saved_experiment
        return saved_experiment.id

    def _update_favourite_saved_experiment(self, saved_experiment_id: int, favourite: bool):
        """Ask the api to add or remove a saved experiment from the favourite relations, by using the update saved
        experiment's endpoint"""

        response, status_code = self._connection.send_put_auth_remote_api_call(
            path=f"{self._SAVED_EXPERIMENTS_CALL_PATH}/{saved_experiment_id}",
            data={API_CONSTANTS.FAVOURITE: favourite, API_CONSTANTS.USER_ID: self._connection.user.user_id},
        )

        if status_code != 200:
            raise RemoteExecutionException(
                message="Experiment favourite status could not be updated.", status_code=status_code
            )

        logger.debug(
            "Experiment %s updated successfully.",
            response[API_CONSTANTS.SAVED_EXPERIMENT_ID],
        )

    def _fav_saved_experiment(self, saved_experiment_id: int):
        """Adds a saved experiment to the list of favourite saved experiments"""
        return self._update_favourite_saved_experiment(saved_experiment_id=saved_experiment_id, favourite=True)

    def _fav_saved_experiments(self, saved_experiment_ids: List[int] | npt.NDArray[np.int_]):
        """Adds a list of saved experiments to the list of favourite saved experiments"""
        for saved_experiment_id in saved_experiment_ids:
            self._update_favourite_saved_experiment(saved_experiment_id=saved_experiment_id, favourite=True)

    def _unfav_saved_experiment(self, saved_experiment_id: int):
        """Removes a saved experiment from the list of favourite saved experiments"""
        return self._update_favourite_saved_experiment(saved_experiment_id=saved_experiment_id, favourite=False)

    def _unfav_saved_experiments(self, saved_experiment_ids: List[int] | npt.NDArray[np.int_]):
        """Removes a list of saved experiments from the list of favourite saved experiments"""
        for saved_experiment_id in saved_experiment_ids:
            self._update_favourite_saved_experiment(saved_experiment_id=saved_experiment_id, favourite=False)

    def _get_list_saved_experiments_response(
        self, favourites: bool = False
    ) -> List[SavedExperimentListingItemResponse]:
        """Performs the actual saved_experiments listing request
        Returns
            List[SavedExperimentListingItemResponse]: list of objects encoding the expected response structure"""
        responses, status_codes = unzip(
            self._connection.send_get_auth_remote_api_call_all_pages(
                path=self._SAVED_EXPERIMENTS_CALL_PATH, params={API_CONSTANTS.FAVOURITES: favourites}
            )
        )
        for status_code in status_codes:
            if status_code != 200:
                raise RemoteExecutionException(message="Job could not be listed.", status_code=status_code)

        items = [item for response in responses for item in response[REST.ITEMS]]
        return [SavedExperimentListingItemResponse(**item) for item in items]

    def _get_list_jobs_response(self, favourites: bool = False) -> List[JobListingItemResponse]:
        """Performs the actual jobs listing request
        Returns
            List[JobListingItemResponse]: list of objects encoding the expected response structure"""
        responses, status_codes = unzip(
            self._connection.send_get_auth_remote_api_call_all_pages(
                path=self._JOBS_CALL_PATH, params={API_CONSTANTS.FAVOURITES: favourites}
            )
        )
        for status_code in status_codes:
            if status_code != 200:
                raise RemoteExecutionException(message="Job could not be listed.", status_code=status_code)

        items = [item for response in responses for item in response[REST.ITEMS]]
        return [JobListingItemResponse.from_kwargs(**item) for item in items]

    @typechecked
    def _list_saved_experiments(self, favourites: bool = False) -> SavedExperimentListing:
        """List all saved experiments

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All SavedExperiments
        """
        saved_experiments_list_response = self._get_list_saved_experiments_response(favourites=favourites)
        saved_experiment_listing = SavedExperimentListing.from_response(saved_experiments_list_response)
        self._saved_experiments_listing = saved_experiment_listing
        return saved_experiment_listing

    @typechecked
    def list_jobs(self, favourites: bool = False) -> JobListing:
        """List all jobs metadata

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All Jobs
        """
        jobs_list_response = self._get_list_jobs_response(favourites=favourites)
        jobs_listing = JobListing.from_response(jobs_list_response)
        self._jobs_listing = jobs_listing
        return jobs_listing

    @typechecked
    def _get_saved_experiment_response(self, saved_experiment_id: int):
        """Gets complete information of a single saved experiment

        Raises:
            RemoteExecutionException: SavedExperiment could not be retrieved

        Returns:
            SavedExperimentResponse: response with the info of the requested saved experiment"""
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self._SAVED_EXPERIMENTS_CALL_PATH}/{saved_experiment_id}"
        )
        if status_code != 200:
            raise RemoteExecutionException(message="SavedExperiment could not be retrieved.", status_code=status_code)
        return SavedExperimentResponse(**response)

    @typechecked
    def _get_saved_experiment(self, saved_experiment_id: int) -> SavedExperiment:
        """Get full information of a single experiment

        Raises:
            RemoteExecutionException: SavedExperiments could not be retrieved

        Returns:
            SavedExperiment: complete saved experiment, including results
        """
        return SavedExperiment.from_response(
            self._get_saved_experiment_response(saved_experiment_id=saved_experiment_id)
        )

    @typechecked
    def get_job(self, job_id: int):
        """Get metadata, result and the correspondig Qibo circuit or Qililab experiment from a remote job execution.

        Args:
            job_id (int): Job identifier

        Raises:
            RemoteExecutionException: Job could not be retrieved.
            ValueError: Job status not supported.
            ValueError: Your job failed.

        Returns:
            JobData
        """

        job_response = self._get_job(job_id=job_id)
        log_job_status_info(job_response=job_response)
        return JobData(**vars(job_response))

    @typechecked
    def _get_saved_experiments(self, saved_experiment_ids: List[int] | npt.NDArray[np.int_]) -> List[SavedExperiment]:
        """Get full information of the chosen experiments

        Raises:
            RemoteExecutionException: SavedExperiments could not be retrieved

        Returns:
            List[SavedExperiment]: complete saved experiment list, including results
        """
        return [
            SavedExperiment.from_response(self._get_saved_experiment_response(saved_experiment_id=saved_experiment_id))
            for saved_experiment_id in saved_experiment_ids
        ]

    # RUNCARDS

    def _create_runcard_response(self, runcard: Runcard):
        """Make the runcard create request and parse the response"""
        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self._RUNCARDS_CALL_PATH,
            data=asdict(runcard.runcard_request()),
        )
        if status_code not in [200, 201]:
            raise RemoteExecutionException(message="Runcard could not be saved.", status_code=status_code)
        logger.debug("Experiment saved successfully.")
        return RuncardResponse.from_kwargs(**response)

    @typechecked
    def save_runcard(
        self,
        name: str,
        description: str,
        runcard_dict: dict,
        device_id: int,
        user_id: int,
        qililab_version: str,
    ):
        """Save a runcard into the database af our servers, for it to be easily recovered when needed.

          .. warning::

            This method is only available for Qilimanjaro members.

        Args:
            name: Name the experiment is going to be saved with.
            description: Short descriptive text to more easily identify this specific experiment instance.
            runcard_dict: Serialized runcard (using its `.to_dict()` method)
            device_id: Id of the device the experiment was executed in
            user_id: Id of the user that is executing the experiment
            qililab_version: version of qililab the experiment was executed with

        Returns:
            new saved runcard

        """

        runcard = Runcard(
            id=None,
            name=name,
            description=description,
            runcard=runcard_dict,
            device_id=device_id,
            user_id=user_id,
            qililab_version=qililab_version,
        )

        runcard_response = self._create_runcard_response(runcard=runcard)
        created_runcard = Runcard.from_response(response=runcard_response)

        self._runcard = created_runcard
        return created_runcard.id  # type: ignore[attr-defined]

    @typechecked
    def _get_runcard_response(self, runcard_id: int):
        """Gets complete information of a specific runcard

        Raises:
            RemoteExecutionException: Runcard could not be retrieved

        Returns:
            RuncardResponse: response with the info of the requested runcard"""
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self._RUNCARDS_CALL_PATH}/{runcard_id}"
        )
        if status_code != 200:
            raise RemoteExecutionException(message="Runcard could not be retrieved.", status_code=status_code)
        return RuncardResponse.from_kwargs(**response)

    @typechecked
    def _get_runcard_by_name_response(self, runcard_name: str):
        """Gets complete information of a specific runcard by name

        Raises:
            RemoteExecutionException: Runcard could not be retrieved

        Returns:
            RuncardResponse: response with the info of the requested runcard"""
        response, status_code = self._connection.send_get_auth_remote_api_call(
            path=f"{self._RUNCARDS_CALL_PATH}/by_keys", params={"name": runcard_name}
        )

        if status_code != 200:
            raise RemoteExecutionException(message="Runcard could not be retrieved.", status_code=status_code)

        return RuncardResponse.from_kwargs(**response)

    @typechecked
    def get_runcard(self, runcard_id: int | None = None, runcard_name: str | None = None) -> Runcard:
        """Get full information of a specific runcard

          .. warning::

            This method is only available for Qilimanjaro members.

        Args:
            runcard_id(int, optional): id of the runcard to retrieve. Incompatible with providing a name.
            runcard_name(str, optional): name of the runcard to retrieve. Incompatible with providing an id.

        Raises:
            RemoteExecutionException: Runcard could not be retrieved

        Returns:
            Runcard: serialized runcard dictionary
        """
        if runcard_id is not None and runcard_name is not None:
            raise ValueError("Both of of id and name cannot be simultaneously provided")
        if runcard_id is not None:
            return Runcard.from_response(self._get_runcard_response(runcard_id=runcard_id))
        if runcard_name is not None:
            return Runcard.from_response(self._get_runcard_by_name_response(runcard_name=runcard_name))
        raise ValueError("At least one of id and name must be provided")

    def _get_list_runcard_response(
        self,
    ) -> List[RuncardResponse]:
        """Performs the actual runcard listing request
        Returns
            List[RuncardResponse]: list of objects encoding the expected response structure"""
        responses, status_codes = unzip(
            self._connection.send_get_auth_remote_api_call_all_pages(path=self._RUNCARDS_CALL_PATH)
        )
        for status_code in status_codes:
            if status_code != 200:
                raise RemoteExecutionException(message="Runcards could not be listed.", status_code=status_code)

        items = [item for response in responses for item in response[REST.ITEMS]]
        return [RuncardResponse.from_kwargs(**item) for item in items]

    @typechecked
    def list_runcards(self) -> List[Runcard]:
        """List all saved experiments

        Raises:
            RemoteExecutionException: Devices could not be retrieved

        Returns:
            Devices: All SavedExperiments
        """
        runcards_response = self._get_list_runcard_response()
        return [Runcard.from_response(response=response) for response in runcards_response]

    @typechecked
    def update_runcard(self, runcard: Runcard) -> Runcard:
        """Update the info of a runcard in the database

          .. warning::

            This method is only available for Qilimanjaro members.

        Raises:
            RemoteExecutionException: Runcard could not be retrieved

        Returns:
            Runcard: serialized runcard dictionary
        """
        if runcard.id is None:  # type: ignore[attr-defined]
            raise ValueError("Runcard id must be defined for updating its info in the database.")

        runcard_response = self._update_runcard_response(runcard=runcard)
        updated_runcard = Runcard.from_response(response=runcard_response)

        self._runcard = updated_runcard
        return updated_runcard

    def _update_runcard_response(self, runcard: Runcard):
        """Make the runcard update request and parse the response"""
        response, status_code = self._connection.send_put_auth_remote_api_call(
            path=f"{self._RUNCARDS_CALL_PATH}/{runcard.id}",  # type: ignore[attr-defined]
            data=asdict(runcard.runcard_request()),
        )
        if status_code not in [200, 201]:
            raise RemoteExecutionException(message="Runcard could not be saved.", status_code=status_code)
        logger.debug("Runcard updated successfully.")
        return RuncardResponse.from_kwargs(**response)

    @typechecked
    def delete_runcard(self, runcard_id: int) -> None:
        """Deletes a job from the database.

          .. warning::

            This method is only available for Qilimanjaro members.

        Raises:
            RemoteExecutionException: Devices could not be retrieved
        """
        response, status_code = self._connection.send_delete_auth_remote_api_call(
            path=f"{self._RUNCARDS_CALL_PATH}/{runcard_id}"
        )
        if status_code != 204:
            raise RemoteExecutionException(message="Runcard could not be removed.", status_code=status_code)
        logger.info("Runcard %i deleted successfully with message: %s", runcard_id, response)

    @typechecked
    def delete_job(self, job_id: int) -> None:
        """Deletes a job from the database.

        .. warning::

            This method is only available for admin members.

        Raises:
            RemoteExecutionException: Devices could not be retrieved
        """
        response, status_code = self._connection.send_delete_auth_remote_api_call(  # pylint: disable=unused-variable
            path=f"{self._JOBS_CALL_PATH}/{job_id}"
        )
        if status_code != 204:
            raise RemoteExecutionException(message="Job could not be removed.", status_code=status_code)
        logger.info(f"Job {job_id} deleted successfully")
