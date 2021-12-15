""" Tests methods for algorithm """
from qiboconnection.algorithm import Algorithm, AlgorithmOptions
from qiboconnection.typings.algorithm import AlgorithmType, InitialValue


def test_algorithm_creation():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2, initial_value=InitialValue.ZERO),
    )
    assert isinstance(algorithm, Algorithm)
    assert algorithm.name == "alg001"
    assert algorithm.type == AlgorithmType.GATE_BASED
    assert algorithm.options.number_qubits == 2
    assert algorithm.options.initial_value == InitialValue.ZERO


def test_algorithm_creation_no_initial_value():
    algorithm = Algorithm(
        name="alg001",
        type=AlgorithmType.GATE_BASED,
        options=AlgorithmOptions(number_qubits=2),
    )
    assert isinstance(algorithm, Algorithm)
    assert algorithm.name == "alg001"
    assert algorithm.type == AlgorithmType.GATE_BASED
    assert algorithm.options.number_qubits == 2
    assert algorithm.options.initial_value == InitialValue.ZERO
