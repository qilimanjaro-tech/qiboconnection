# data.py
""" Data to used alongside the test suite. """

from qiboconnection.typings.device import (
    DeviceInput,
    DeviceStatus,
    SimulatorDeviceCharacteristicsInput,
    SimulatorDeviceInput,
)

sample_model_data = {"attribute": "a random attribute"}

sample_schema_model_data = {"name": "qili_schema", "category": "schema", "buses": []}
sample_schema_update_model_data = {"name": "qili_schema_update", "category": "schema", "buses": []}

sample_bus_model_data = {
    "name": "bus",
    "category": "bus",
    "elements": [],
}

sample_bus_update_model_data = {
    "name": "bus_new",
    "category": "bus",
    "elements": [],
}

sample_component_model_data = {
    "name": "qblox_qcm",
    "category": "qubit_control",
    "ip": "192.168.0.3",
    "reference_clock": "internal",
    "sequencer": 0,
    "sync_enabled": True,
    "gain": 1,
}

sample_component_update_model_data = {
    "name": "qblox_qcm_2",
    "category": "qubit_control",
    "ip": "192.168.0.13",
    "reference_clock": "internal",
    "sequencer": 0,
    "sync_enabled": True,
    "gain": 1,
}

sample_platform_settings_model_data = {
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 4096,
    "software_average": 10,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

sample_platform_settings_updated_model_data = {
    "category": "platform",
    "number_qubits": 2,
    "hardware_average": 1024,
    "software_average": 20,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

sample_platform_settings_one_page_items = [{"id_": idx + 1} | sample_platform_settings_model_data for idx in range(5)]
sample_platform_settings_second_page_items = [
    {"id_": idx + 1} | sample_platform_settings_model_data for idx in range(5, 9)
]
sample_multi_page_platform_settings_items = (
    sample_platform_settings_one_page_items + sample_platform_settings_second_page_items
)

sample_one_page_platform_settings_paginated_data = {
    "items": sample_platform_settings_one_page_items,
    "total": 5,
    "per_page": 5,
    "self": "/testing?page=1&per_page=5",
    "links": {
        "first": "/testing?page=1&per_page=5",
        "prev": "/testing?page=1&per_page=5",
        "next": "/testing?page=1&per_page=5",
        "last": "/testing?page=1&per_page=5",
    },
}

sample_multi_platform_settings_first_page_paginated_data = {
    "items": sample_platform_settings_one_page_items,
    "total": 9,
    "per_page": 5,
    "self": "/testing?page=1&per_page=5",
    "links": {
        "first": "/testing?page=1&per_page=5",
        "prev": "/testing?page=1&per_page=5",
        "next": "/testing?page=2&per_page=5",
        "last": "/testing?page=2&per_page=5",
    },
}

sample_multi_platform_settings_second_page_paginated_data = {
    "items": sample_platform_settings_second_page_items,
    "total": 9,
    "per_page": 5,
    "self": "/testing?page=2&per_page=5",
    "links": {
        "first": "/testing?page=1&per_page=5",
        "prev": "/testing?page=1&per_page=5",
        "next": "/testing?page=2&per_page=5",
        "last": "/testing?page=2&per_page=5",
    },
}

sample_model_updated_data = {"attribute": "another random attribute", "updated": True}

sample_result_create_data = {"id": 1} | sample_model_data

sample_result_update_data = {"id": 1} | sample_model_updated_data

sample_one_page_items = [
    {
        "id": 1,
        "username": "qili-test",
    },
    {
        "user_id": 1235,
        "username": "qili-test-2",
    },
]

sample_second_page_items = [
    {
        "id": 2,
        "username": "qili-test",
    },
    {
        "user_id": 1236,
        "username": "qili-test-2",
    },
]

sample_multi_page_items = sample_one_page_items + sample_second_page_items

sample_one_page_paginated_data = {
    "items": sample_one_page_items,
    "total": 2,
    "per_page": 5,
    "self": "/testing?page=1&per_page=5",
    "links": {
        "first": "/testing?page=1&per_page=5",
        "prev": "/testing?page=1&per_page=5",
        "next": "/testing?page=1&per_page=5",
        "last": "/testing?page=1&per_page=5",
    },
}

sample_multi_first_page_paginated_data = {
    "items": sample_one_page_items,
    "total": 4,
    "per_page": 2,
    "self": "/testing?page=1&per_page=2",
    "links": {
        "first": "/testing?page=1&per_page=2",
        "prev": "/testing?page=1&per_page=2",
        "next": "/testing?page=2&per_page=2",
        "last": "/testing?page=2&per_page=2",
    },
}

sample_multi_second_page_paginated_data = {
    "items": sample_second_page_items,
    "total": 4,
    "per_page": 2,
    "self": "/testing?page=2&per_page=2",
    "links": {
        "first": "/testing?page=1&per_page=2",
        "prev": "/testing?page=1&per_page=2",
        "next": "/testing?page=2&per_page=2",
        "last": "/testing?page=2&per_page=2",
    },
}

device_inputs = [
    DeviceInput(device_id=1, device_name="one_device", status="available", channel_id=None),
    DeviceInput(device_id=2, device_name="second_device", status=DeviceStatus.AVAILABLE, channel_id=None),
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
        characteristics=simulator_device_characteristics_inputs[0],
    )
]

platform_settings_sample = {
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 4096,
    "software_average": 10,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

platform_settings_updated_sample = {
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 1024,
    "software_average": 5,
    "repetition_duration": 100000,
    "delay_between_pulses": 0,
    "delay_before_readout": 20,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

platform_locations_sample = [
    "/qiboconnection/src/qiboconnection/data/platform-schema_1",
    "/qiboconnection/src/qiboconnection/data/platform-schema_2",
]

platform_mocked_settings_sample = {
    "id": 1,
    "category": "platform",
    "number_qubits": 1,
    "hardware_average": 4096,
    "software_average": 10,
    "repetition_duration": 200000,
    "delay_between_pulses": 0,
    "delay_before_readout": 50,
    "drag_coefficient": 0,
    "number_of_sigmas": 4,
}

sample_all_platform_settings = {
    "platform": {
        "id_": 0,
        "name": "platform",
        "category": "platform",
        "number_qubits": 1,
        "hardware_average": 4096,
        "software_average": 10,
        "repetition_duration": 200000,
        "delay_between_pulses": 0,
        "delay_before_readout": 50,
        "drag_coefficient": 0,
        "number_of_sigmas": 4,
    },
    "schema": {
        "id_": 0,
        "name": "qili_schema",
        "category": "schema",
        "buses": [
            {
                "id_": 0,
                "name": "bus",
                "category": "bus",
                "elements": [
                    {
                        "id_": 0,
                        "name": "qblox_qcm",
                        "category": "qubit_control",
                        "ip": "192.168.0.3",
                        "reference_clock": "internal",
                        "sequencer": 0,
                        "sync_enabled": True,
                        "gain": 1,
                    },
                    {
                        "id_": 0,
                        "name": "rohde_schwarz",
                        "category": "signal_generator",
                        "ip": "192.168.0.10",
                        "power": 15,
                        "frequency": 3644000000,
                    },
                    {
                        "id_": 0,
                        "name": "mixer",
                        "category": "mixer",
                        "epsilon": 0,
                        "delta": 0,
                        "offset_i": 0,
                        "offset_q": 0,
                        "up_conversion": True,
                    },
                    {
                        "id_": 0,
                        "name": "resonator",
                        "category": "resonator",
                        "qubits": [
                            {
                                "id_": 0,
                                "name": "qubit",
                                "category": "qubit",
                                "pi_pulse_amplitude": 1,
                                "pi_pulse_duration": 100,
                                "pi_pulse_frequency": 100000000,
                                "qubit_frequency": 3544000000,
                                "min_voltage": 950,
                                "max_voltage": 1775,
                            }
                        ],
                    },
                ],
            },
            {
                "id_": 1,
                "name": "bus",
                "category": "bus",
                "elements": [
                    {
                        "id_": 0,
                        "name": "qblox_qrm",
                        "category": "qubit_readout",
                        "ip": "192.168.0.4",
                        "reference_clock": "external",
                        "sequencer": 0,
                        "sync_enabled": True,
                        "gain": 0.5,
                        "acquire_trigger_mode": "sequencer",
                        "hardware_average_enabled": True,
                        "start_integrate": 130,
                        "sampling_rate": 1000000000,
                        "integration_length": 2000,
                        "integration_mode": "ssb",
                        "sequence_timeout": 1,
                        "acquisition_timeout": 1,
                        "acquisition_name": "single",
                    },
                    {
                        "id_": 1,
                        "name": "rohde_schwarz",
                        "category": "signal_generator",
                        "ip": "192.168.0.7",
                        "power": 15,
                        "frequency": 7307720000,
                    },
                    {
                        "id_": 0,
                        "name": "resonator",
                        "category": "resonator",
                        "qubits": [
                            {
                                "id_": 0,
                                "name": "qubit",
                                "category": "qubit",
                                "pi_pulse_amplitude": 1,
                                "pi_pulse_duration": 100,
                                "pi_pulse_frequency": 100000000,
                                "qubit_frequency": 3544000000,
                                "min_voltage": 950,
                                "max_voltage": 1775,
                            }
                        ],
                    },
                    {
                        "id_": 1,
                        "name": "mixer",
                        "category": "mixer",
                        "epsilon": 0,
                        "delta": 0,
                        "offset_i": 0,
                        "offset_q": 0,
                        "up_conversion": True,
                    },
                ],
            },
            {
                "id_": 2,
                "name": "bus",
                "category": "bus",
                "elements": [
                    {
                        "id_": 0,
                        "name": "qblox_qrm",
                        "category": "qubit_readout",
                        "ip": "192.168.0.4",
                        "reference_clock": "external",
                        "sequencer": 0,
                        "sync_enabled": True,
                        "gain": 0.5,
                        "acquire_trigger_mode": "sequencer",
                        "hardware_average_enabled": True,
                        "start_integrate": 130,
                        "sampling_rate": 1000000000,
                        "integration_length": 2000,
                        "integration_mode": "ssb",
                        "sequence_timeout": 1,
                        "acquisition_timeout": 1,
                        "acquisition_name": "single",
                    },
                    {
                        "id_": 1,
                        "name": "rohde_schwarz",
                        "category": "signal_generator",
                        "ip": "192.168.0.7",
                        "power": 15,
                        "frequency": 7307720000,
                    },
                    {
                        "id_": 0,
                        "name": "resonator",
                        "category": "resonator",
                        "qubits": [
                            {
                                "id_": 0,
                                "name": "qubit",
                                "category": "qubit",
                                "pi_pulse_amplitude": 1,
                                "pi_pulse_duration": 100,
                                "pi_pulse_frequency": 100000000,
                                "qubit_frequency": 3544000000,
                                "min_voltage": 950,
                                "max_voltage": 1775,
                            }
                        ],
                    },
                    {
                        "id_": 2,
                        "name": "mixer",
                        "category": "mixer",
                        "epsilon": 0,
                        "delta": 0,
                        "offset_i": 0,
                        "offset_q": 0,
                        "up_conversion": False,
                    },
                ],
            },
        ],
    },
}
