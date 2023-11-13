# pylint: disable=logging-fstring-interpolation
# pylint: disable=protected-access
# pylint: disable=import-error
# pylint: disable=no-name-in-module
import logging
import logging.config
import os

import pytest
import qibo
from _pytest.config import Config
from qibo import gates
from qibo.models.circuit import Circuit
from src.end2end.utils.utils import get_api_or_fail_test, get_logging_conf_or_fail_test

from qiboconnection.api import API
from qiboconnection.errors import HTTPError
from qiboconnection.models.devices import Device
from qiboconnection.models.runcard import Runcard


def pytest_configure(config: Config):  # pylint: disable=unused-argument
    """Initialize the logging configuration. This is executed once per test session.

    Args:
        config : configuration object
    """
    file_logging_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.ini")

    logging.config.fileConfig(file_logging_cfg, disable_existing_loggers=False)


def pytest_runtest_setup(item):
    """Configure the runtest

    Args:
        item: each of the test functions
    """

    # By default, do not run the tests marked as slow.
    # To run them, we have to use the option --slow when running pytest, to force its execution.
    if "slow" in item.keywords and not item.config.getoption(name="--slow"):
        pytest.skip("need --slow to run this test")


# ------------------------------------------------------------------------------
#  Options
# ------------------------------------------------------------------------------


def pytest_addoption(parser):
    """Add custom  command line options

    Args:
        parser: pytest parser object
    """
    parser.addoption("--slow", action="store_true", help="Run the tests that take long time")


# ------------------------------------------------------------------------------
#  Fixtures
# ------------------------------------------------------------------------------


@pytest.fixture(name="api")
def get_api_fixture() -> API:
    """Gives a usable API instance"""
    return get_api_or_fail_test(logging_conf=get_logging_conf_or_fail_test())


@pytest.fixture(name="devices")
def get_devices(api) -> list[Device]:
    try:
        devices = api.list_devices()
        return devices._devices
    except HTTPError:
        return []


# In pytest, caplog is a built-in fixture that allows you to capture log output
# generated by your code during test execution.
# It stands for "captured log" and provides a convenient way to assert and analyze
# log messages produced by your code.


@pytest.fixture(name="numpy_circuit")
@pytest.mark.usefixtures("caplog")
def get_qibo_circuit_numpy_fixture(caplog) -> Circuit:
    """Builds a numpy backend qibo circuit"""
    caplog.set_level("ERROR")

    qibo.set_backend("numpy")  # Must precede circuit definition. Else, execution will fail.
    circuit = Circuit(nqubits=1)
    circuit.add(gates.H(0))
    circuit.add(gates.M(0))

    caplog.clear()
    try:
        return circuit
    except Exception as e:
        pytest.fail(f"Circuit creation failed. {e}.", pytrace=False)


@pytest.fixture(name="one_qubits_500_gates_circuit")
@pytest.mark.usefixtures("caplog")
def one_qubits_500_gates_circuit(caplog) -> Circuit:
    """Build a 500 gates 1 qubit circuit"""
    caplog.set_level("ERROR")

    # init circuit
    c = Circuit(nqubits=1)

    for _ in range(100):
        c.add(gates.Y(0))
        c.add(gates.X(0))
        c.add(gates.I(0))
        c.add(gates.S(0))
        c.add(gates.Z(0))

    # measurement
    c.add(gates.M(0))

    caplog.clear()
    try:
        return c
    except Exception as e:
        pytest.fail(f"Circuit creation failed. {e}.", pytrace=False)


@pytest.fixture(name="two_qubits_500_gates_circuit")
@pytest.mark.usefixtures("caplog")
def two_qubits_500_gates_circuit(caplog) -> Circuit:
    """Build a 500 gates 2 qubit circuit"""
    caplog.set_level("ERROR")

    # init circuit
    c = Circuit(nqubits=2)

    for _ in range(100):
        c.add(gates.Y(0))
        c.add(gates.CNOT(0, 1))
        c.add(gates.I(0))
        c.add(gates.S(1))
        c.add(gates.Z(0))

    # measurement
    c.add(gates.M(0))
    c.add(gates.M(1))

    caplog.clear()
    try:
        return c
    except Exception as e:
        pytest.fail(f"Circuit creation failed. {e}.", pytrace=False)


@pytest.fixture(name="five_qubits_500_gates_circuit")
@pytest.mark.usefixtures("caplog")
def five_qubits_500_gates_circuit(caplog) -> Circuit:
    """Build a 500 gates 5 qubit circuit"""
    caplog.set_level("ERROR")

    # init circuit
    c = Circuit(nqubits=5)

    for _ in range(50):
        c.add(gates.Y(2))
        c.add(gates.X(1))
        c.add(gates.I(0))
        c.add(gates.CNOT(0, 3))
        c.add(gates.Z(0))
        c.add(gates.FSWAP(3, 2))
        c.add(gates.CNOT(1, 4))
        c.add(gates.TOFFOLI(0, 1, 2))
        c.add(gates.TDG(3))
        c.add(gates.CZ(0, 4))

    # measurement
    c.add(gates.M(0))
    c.add(gates.M(1))
    c.add(gates.M(2, 3, 4))

    caplog.clear()
    try:
        return c
    except Exception as e:
        pytest.fail(f"Circuit creation failed. {e}.", pytrace=False)


@pytest.fixture(name="runcard")
def runcard() -> Runcard:
    """Build a simple runcard"""

    return Runcard(
        name="fixture_runcard",
        user_id=3,
        device_id=1,
        description="runcard for testing",
        runcard={"Hello": "world!"},
        qililab_version="bsc-300",
    )


@pytest.fixture(name="results_dict")
def get_results_dict() -> dict:
    """Create a likely qililab results serialization dictionary"""
    return {
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


@pytest.fixture(name="experiment_dict")
def get_experiment_dict() -> dict:
    """Create a likely qililab experiments serialization dictionary"""
    return {
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
