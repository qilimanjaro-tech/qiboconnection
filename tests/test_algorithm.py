""" Tests methods for Algorithms """

from qiboconnection.typings.algorithm import (
    AlgorithmDefinition,
    AlgorithmName,
    AlgorithmOptions,
    AlgorithmType,
    InitialValue,
)


def test_algorithm_options_constructor():
    """Tests the AlgorithmOptions class constructor"""
    algorithm_options = AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO)
    assert isinstance(algorithm_options, AlgorithmOptions)


def test_algorithm_options_dict_representation():
    """Tests the AlgorithmOptions().__dict__ method"""
    algorithm_options = AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO)
    expected_dict = {"number_qubits": 2, "initial_value": InitialValue.ZERO.value}
    assert algorithm_options.__dict__ == expected_dict


def test_algorithm_definition_constructor():
    """Tests the AlgorithmDefinition class constructor"""
    algorithm_definition = AlgorithmDefinition(
        name=AlgorithmName.BELLSTATE,
        algorithm_type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    assert isinstance(algorithm_definition, AlgorithmDefinition)


def test_algorithm_definition_dict_representation():
    """Tests the AlgorithmDefinition().__dict__ method"""
    algorithm_definition = AlgorithmDefinition(
        name=AlgorithmName.BELLSTATE,
        algorithm_type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    expected_dict = {
        "name": AlgorithmName.BELLSTATE.value,
        "type": AlgorithmType.GATE_BASED.value,
        "options": AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO).__dict__,
    }
    assert algorithm_definition.__dict__ == expected_dict
