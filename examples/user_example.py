import os
from time import sleep

from qibo import gates
from qibo.core.circuit import Circuit

from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration


def user_example_remote_execution() -> None:
    """
    Example code that a user could run for executing a circuit remotely.
    """

    # Connect using credentials
    myconf = ConnectionConfiguration(user_id=1, username="my-user-name", api_key="abcdefg-hijk-lmno-pqrs-tuvwxyzABCDE")
    qibo_api = API(configuration=myconf)

    # Connect if credentials are already saved in your environment
    qibo_api = API()

    # Check connection
    qibo_api.ping()

    # List devices (if needed)
    devices = qibo_api.list_devices()
    print(devices)
    qibo_api.select_device_id(device_id=1)

    # Design circuit
    circuit = Circuit(1)
    circuit.add(gates.X(0))
    circuit.add(gates.M(0))

    # Issue an async remote execution of the circuit
    job_ids = qibo_api.execute(circuit=circuit)
    print(f"job id: {job_ids}")
    sleep(1)
    result = qibo_api.get_results(job_ids=job_ids)
    if result is not None:
        print(result)

    # Block device, do stuff directly over the device, release device
    qibo_api.block_device_id(device_id=1)
    # --- do stuff here ---
    qibo_api.release_device(device_id=1)


def user_example_experiment_saving() -> None:
    """
    Example code that a user could run for executing a circuit remotely.
    """

    # Connect using credentials
    myconf = ConnectionConfiguration(user_id=1, username="my-user-name", api_key="abcdefg-hijk-lmno-pqrs-tuvwxyzABCDE")
    qibo_api = API(configuration=myconf)

    # Connect if credentials are already saved in your environment
    qibo_api = API()

    # Check connection
    qibo_api.ping()

    # List experiments
    qibo_api.list_saved_experiments()

    # Save an experiment
    experiment_dict = {
        "platform": {
            "settings": {
                "id_": 0,
                "category": "platform",
                "alias": None,
                "name": "galadriel",
                "delay_between_pulses": 0,
                "delay_before_readout": 80.0,
                "master_amplitude_gate": 1,
                "master_duration_gate": 100,
                "gates": [
                    {
                        "name": "M",
                        "amplitude": "master_amplitude_gate",
                        "phase": 0,
                        "duration": 2000,
                        "shape": {"name": "rectangular"},
                    },
                    {"name": "I", "amplitude": 0, "phase": 0, "duration": 0, "shape": {"name": "rectangular"}},
                    {
                        "name": "X",
                        "amplitude": "master_amplitude_gate",
                        "phase": 0,
                        "duration": "master_duration_gate",
                        "shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                    },
                    {
                        "name": "Y",
                        "amplitude": "master_amplitude_gate",
                        "phase": 1.5707963267948966,
                        "duration": "master_duration_gate",
                        "shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                    },
                ],
            },
            "schema": {
                "chip": {
                    "id_": 0,
                    "category": "chip",
                    "nodes": [
                        {"name": "port", "id_": 0, "category": "node", "alias": None, "nodes": [3]},
                        {"name": "port", "id_": 1, "category": "node", "alias": None, "nodes": [2]},
                        {
                            "name": "resonator",
                            "id_": 2,
                            "category": "node",
                            "alias": "resonator",
                            "nodes": [1, 3],
                            "frequency": 7347300000.0,
                        },
                        {
                            "name": "qubit",
                            "id_": 3,
                            "category": "node",
                            "alias": "qubit",
                            "nodes": [0, 2],
                            "frequency": 3451000000.0,
                            "qubit_idx": 0,
                        },
                    ],
                },
                "instruments": [
                    {
                        "name": "QCM",
                        "id_": 0,
                        "category": "awg",
                        "alias": "QCM",
                        "firmware": "0.7.0",
                        "frequency": 1.0,
                        "num_sequencers": 1,
                        "gain": [1],
                        "epsilon": [0],
                        "delta": [0],
                        "offset_i": [0],
                        "offset_q": [0],
                        "multiplexing_frequencies": [100000000.0],
                        "sync_enabled": True,
                        "num_bins": 100,
                    },
                    {
                        "name": "QRM",
                        "id_": 1,
                        "category": "awg",
                        "alias": "QRM",
                        "firmware": "0.7.0",
                        "frequency": 20000000,
                        "num_sequencers": 1,
                        "gain": [0.5],
                        "epsilon": [0],
                        "delta": [0],
                        "offset_i": [0],
                        "offset_q": [0],
                        "multiplexing_frequencies": [20000000.0],
                        "acquisition_delay_time": 100,
                        "sync_enabled": True,
                        "num_bins": 100,
                        "scope_acquire_trigger_mode": "sequencer",
                        "scope_hardware_averaging": True,
                        "sampling_rate": 1000000000,
                        "integration": True,
                        "integration_length": 2000,
                        "integration_mode": "ssb",
                        "sequence_timeout": 1,
                        "acquisition_timeout": 1,
                    },
                    {
                        "name": "rohde_schwarz",
                        "id_": 0,
                        "category": "signal_generator",
                        "alias": "rs_0",
                        "firmware": "4.30.046.295",
                        "power": 15,
                    },
                    {
                        "name": "rohde_schwarz",
                        "id_": 1,
                        "category": "signal_generator",
                        "alias": "rs_1",
                        "firmware": "4.30.046.295",
                        "power": 15,
                    },
                    {
                        "name": "mini_circuits",
                        "id_": 1,
                        "category": "attenuator",
                        "alias": "attenuator",
                        "firmware": None,
                        "attenuation": 30,
                    },
                    {
                        "name": "keithley_2600",
                        "id_": 1,
                        "category": "dc_source",
                        "alias": "keithley_2600",
                        "firmware": None,
                        "max_current": 0.1,
                        "max_voltage": 20.0,
                    },
                ],
                "buses": [
                    {
                        "id_": 0,
                        "category": "bus",
                        "subcategory": "control",
                        "system_control": {
                            "id_": 0,
                            "category": "system_control",
                            "subcategory": "mixer_based_system_control",
                            "awg": "QCM",
                            "signal_generator": "rs_0",
                        },
                        "port": 0,
                    },
                    {
                        "id_": 0,
                        "category": "bus",
                        "subcategory": "readout",
                        "system_control": {
                            "id_": 1,
                            "category": "system_control",
                            "subcategory": "mixer_based_system_control",
                            "awg": "QRM",
                            "signal_generator": "rs_1",
                        },
                        "attenuator": "attenuator",
                        "port": 1,
                    },
                ],
                "instrument_controllers": [
                    {
                        "name": "qblox_pulsar",
                        "id_": 0,
                        "alias": "pulsar_controller_qcm_0",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.3"},
                        "modules": [{"awg": "QCM", "slot_id": 0}],
                        "reference_clock": "internal",
                    },
                    {
                        "name": "qblox_pulsar",
                        "id_": 1,
                        "alias": "pulsar_controller_qrm_0",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.4"},
                        "modules": [{"awg": "QRM", "slot_id": 0}],
                        "reference_clock": "external",
                    },
                    {
                        "name": "rohde_schwarz",
                        "id_": 2,
                        "alias": "rohde_schwarz_controller_0",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.10"},
                        "modules": [{"signal_generator": "rs_0", "slot_id": 0}],
                    },
                    {
                        "name": "rohde_schwarz",
                        "id_": 3,
                        "alias": "rohde_schwarz_controller_1",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.7"},
                        "modules": [{"signal_generator": "rs_1", "slot_id": 0}],
                    },
                    {
                        "name": "mini_circuits",
                        "id_": 4,
                        "alias": "attenuator_controller_0",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.222"},
                        "modules": [{"attenuator": "attenuator", "slot_id": 0}],
                    },
                    {
                        "name": "keithley_2600",
                        "id_": 5,
                        "alias": "keithley_2600_controller_0",
                        "category": "instrument_controller",
                        "subcategory": "single_instrument",
                        "connection": {"name": "tcp_ip", "address": "192.168.0.112"},
                        "modules": [{"dc_source": "keithley_2600", "slot_id": 0}],
                    },
                ],
            },
        },
        "settings": {"hardware_average": 1024, "software_average": 1, "repetition_duration": 200000},
        "sequences": [
            {
                "elements": [
                    {
                        "timeline": [
                            {
                                "pulse": {
                                    "name": "pulse",
                                    "amplitude": 1.0,
                                    "frequency": None,
                                    "phase": 0.0,
                                    "duration": 100,
                                    "pulse_shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                                },
                                "start_time": 0,
                            },
                            {
                                "pulse": {
                                    "name": "pulse",
                                    "amplitude": 1.0,
                                    "frequency": None,
                                    "phase": 1.5707963267948966,
                                    "duration": 100,
                                    "pulse_shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                                },
                                "start_time": 100,
                            },
                            {
                                "pulse": {
                                    "name": "pulse",
                                    "amplitude": 0.6788726177728143,
                                    "frequency": None,
                                    "phase": 3.141592653589793,
                                    "duration": 100,
                                    "pulse_shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                                },
                                "start_time": 200,
                            },
                            {
                                "pulse": {
                                    "name": "pulse",
                                    "amplitude": 0.7746482927568603,
                                    "frequency": None,
                                    "phase": 1.5707963267948966,
                                    "duration": 100,
                                    "pulse_shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                                },
                                "start_time": 300,
                            },
                            {
                                "pulse": {
                                    "name": "pulse",
                                    "amplitude": 0.45633840657306957,
                                    "frequency": None,
                                    "phase": 6.150444078461241,
                                    "duration": 100,
                                    "pulse_shape": {"name": "drag", "num_sigmas": 4, "drag_coefficient": 0},
                                },
                                "start_time": 400,
                            },
                        ],
                        "port": 0,
                    },
                    {
                        "timeline": [
                            {
                                "pulse": {
                                    "name": "readout_pulse",
                                    "amplitude": 1,
                                    "frequency": None,
                                    "phase": 0,
                                    "duration": 2000,
                                    "pulse_shape": {"name": "rectangular"},
                                },
                                "start_time": 580.0,
                            }
                        ],
                        "port": 1,
                    },
                ]
            }
        ],
        "loops": [
            {
                "alias": None,
                "instrument": "signal_generator",
                "id_": 0,
                "parameter": "frequency",
                "start": 0,
                "stop": 1,
                "num": 2,
                "step": None,
                "loop": {
                    "alias": "platform",
                    "instrument": None,
                    "id_": None,
                    "parameter": "delay_before_readout",
                    "start": 40,
                    "stop": 100,
                    "num": None,
                    "step": 40,
                    "loop": {
                        "alias": None,
                        "instrument": "awg",
                        "id_": 0,
                        "parameter": "frequency",
                        "start": 0,
                        "stop": 1,
                        "num": 2,
                        "step": None,
                        "loop": None,
                    },
                },
            }
        ],
        "name": "experiment",
    }
    results_dict = {
        "software_average": 1,
        "num_sequences": 1,
        "shape": [2, 2, 2],
        "loops": [
            {
                "alias": None,
                "instrument": "signal_generator",
                "id_": 0,
                "parameter": "frequency",
                "start": 0,
                "stop": 1,
                "num": 2,
                "step": None,
                "loop": {
                    "alias": "platform",
                    "instrument": None,
                    "id_": None,
                    "parameter": "delay_before_readout",
                    "start": 40,
                    "stop": 100,
                    "num": None,
                    "step": 40,
                    "loop": {
                        "alias": None,
                        "instrument": "awg",
                        "id_": 0,
                        "parameter": "frequency",
                        "start": 0,
                        "stop": 1,
                        "num": 2,
                        "step": None,
                        "loop": None,
                    },
                },
            }
        ],
        "results": [
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
            {
                "name": "qblox",
                "pulse_length": 2000,
                "bins": [
                    {
                        "integration": {"path0": [-0.08875841551660968], "path1": [-0.4252879595139228]},
                        "threshold": [0.48046875],
                        "avg_cnt": [1024],
                    }
                ],
            },
        ],
    }
    saved_experiment_id = qibo_api.save_experiment(
        name="MyBelovedSavedExperiment",
        description="Experiment saved from jupyterhub",
        experiment_dict=experiment_dict,
        results_dict=results_dict,
        device_id=1,
        user_id=qibo_api._connection._user_id,
        favourite=False,
        qililab_version="0.0.0",
    )

    # Retrieve an experiment
    saved_experiment = qibo_api.get_saved_experiment(saved_experiment_id=saved_experiment_id)
    print(saved_experiment.results)


if __name__ == "__main__":
    os.environ["QIBOCONNECTION_ENVIRONMENT"] = "development"
    print(f'QIBOCONNECTION_ENVIRONMENT={os.environ["QIBOCONNECTION_ENVIRONMENT"]}')
    user_example_remote_execution()
    user_example_experiment_saving()
