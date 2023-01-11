# data.py
""" Data to used alongside the test suite. """

from qiboconnection.typings.device import (
    DeviceInput,
    DeviceStatus,
    OfflineDeviceInput,
    QuantumDeviceCharacteristicsInput,
    QuantumDeviceInput,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)
from qiboconnection.typings.live_plot import UnitPoint

from .web_responses import WebResponses

device_inputs = [
    DeviceInput(device_id=1, device_name="one_device", status="available", channel_id=None),
    DeviceInput(device_id=2, device_name="second_device", status=DeviceStatus.AVAILABLE, channel_id=None),
]

offline_device_inputs = [
    OfflineDeviceInput(device_id=1, device_name="one_device", status="offline", channel_id=None),
    OfflineDeviceInput(device_id=2, device_name="second_device", status=DeviceStatus.OFFLINE, channel_id=None),
]

simulator_device_characteristics_inputs = [
    SimulatorDeviceCharacteristicsInput(
        type="simulator",
        cpu="Intel Core i9-9900K @ 16x 5GHz",
        gpu="NVIDIA GeForce RTX 3090",
        os="Ubuntu 20.04 focal",
        kernel="x86_64 Linux 5.4.0-80-generic",
        ram="64185MiB",
    )
]

simulator_device_inputs = [
    SimulatorDeviceInput(
        device_id=1,
        device_name="radagast-simulator",
        status="available",
        channel_id=None,
        characteristics={
            "type": "simulator",
            "cpu": "Intel Core i9-9900K @ 16x 5GHz",
            "gpu": "NVIDIA GeForce RTX 3090",
            "os": "Ubuntu 20.04 focal",
            "kernel": "x86_64 Linux 5.4.0-80-generic",
            "ram": "64185MiB",
        },
    )
]

quantum_device_characteristics_inputs = [QuantumDeviceCharacteristicsInput(type="quantum", description="Cluster")]
quantum_device_inputs = [
    QuantumDeviceInput(
        device_id=1,
        device_name="galadriel-cluster",
        status="available",
        last_calibration_time="0",
        channel_id=None,
        characteristics={"type": "quantum", "description": "Cluster"},
        calibration_details={"t1": 10, "frequency": 988, "elapsed_time": 10},
    )
]

unit_plot_point = [UnitPoint(x=0, y=0, z=None, idx=None, idy=None)]

heatmap_unit_plot_points = [
    UnitPoint(x=0, y=0, z=0, idx=0, idy=0),
    UnitPoint(x=0, y=1, z=1, idx=0, idy=1),
    UnitPoint(x=1, y=0, z=2, idx=1, idy=0),
    UnitPoint(x=1, y=1, z=3, idx=1, idy=1),
]


web_responses = WebResponses()


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
