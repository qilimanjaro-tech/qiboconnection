import numpy as np
from qibo import gates
from qibo.models import Circuit


def clifford_circuits(
    qubit_idx: int, num_cliffords: int, num_circuits: int = 1, seed: int | None = None, inverse=False
) -> list[Circuit]:
    """Returns a list of circuits based of Clifford gates that evaluate to the identity.

    Args:
        qubit_idx (int): Qubit index.
        num_cliffords (int): Number of Clifford gates per circuit.
        num_circuits (int, optional): Number of circuits to return. Defaults to 1.
        seed (int, optional): Seed to use for the random number generator. Defaults to None.

    Returns:
        list[Circuit]: List of Clifford-based circuits. They all evaluate to the identity.
    """
    rng = np.random.default_rng() if seed is None else np.random.default_rng(seed)
    circuits = []
    for _ in range(num_circuits):
        circuit = Circuit(qubit_idx + 1)
        unitary = CliffordGate(0)  # identity
        for _ in range(num_cliffords):
            random_idx = rng.integers(0, len(CLIFFORD_GATES))
            tmp_gate = CliffordGate(random_idx)
            circuit += tmp_gate.circuit(qubit_idx=qubit_idx)
            unitary = tmp_gate * unitary

        if inverse:
            # add Clifford gate such that sequence is equivalent to X gate
            unitary = CliffordGate(3) * unitary.inverse  # CliffordGate(3) = X gate

        # add inverse to sequence
        circuit = circuit + unitary.inverse.circuit(qubit_idx=qubit_idx)
        # add measurement gates
        circuit.add(gates.M(qubit_idx))

        # append to lists
        circuits.append(circuit)

    return circuits


class CliffordGate:
    """Class to multiply and invert Clifford gates.

    Args:
        idx: (int) Index of the Clifford gate. This value must be between 0 and 23.
    """

    def __init__(self, idx: int) -> None:
        if not 0 <= idx <= 23:
            raise IndexError("Clifford index must be between 0 and 23")
        self.idx = idx
        self._gate = CLIFFORD_GATES[idx]

    @property
    def inverse(self):
        """
        Returns the inverse as a CliffordGate object
        """
        return CliffordGate(CLIFFORD_INVERSES[self.idx])

    def circuit(self, qubit_idx: int) -> Circuit:
        circuit = Circuit(qubit_idx + 1)
        for gate in list(map(int, str(self._gate))):
            circuit.add(PRIMITIVE_GATES[gate]["gate"](qubit_idx))

        return circuit

    def __mul__(self, right):
        """
        Overload of the left multiply operator: clifford_gate * right
        """
        if not isinstance(right, CliffordGate):
            raise ValueError("Using non CliffordGate object as multiplying factor")

        return CliffordGate(CLIFFORD_PRODUCTS[self.idx][right.idx])

    def __rmul__(self, left):
        """
        Overload of the right multiply operator: left * clifford_gate
        """
        if not isinstance(left, CliffordGate):
            raise ValueError("Using non CliffordGate object as multiplying factor")

        return CliffordGate(CLIFFORD_PRODUCTS[left.idx][self.idx])


PRIMITIVE_GATES = {
    0: {"name": "I", "inv": 0, "gate": gates.I},
    1: {"name": "X_pi/2", "inv": 31, "gate": lambda qubit_idx: gates.RX(qubit_idx, theta=np.pi / 2)},
    2: {"name": "Y_pi/2", "inv": 42, "gate": lambda qubit_idx: gates.RY(qubit_idx, theta=np.pi / 2)},
    3: {"name": "X_pi", "inv": 3, "gate": gates.X},
    4: {"name": "Y_pi", "inv": 4, "gate": gates.Y},
}
"""Dictionary containing the 5 primitive gates used in the RB experiment. Each gate is represented by an index."""

CLIFFORD_GATES = [0, 21, 123, 3, 214, 124, 4, 2134, 12, 34, 213, 1234, 23, 13]
"""List of clifford gates used in the RB experiment. Each element of the list contains several digits, which
represent the matrix multiplication of the primitive gates defined above."""
CLIFFORD_GATES += [1214, 24, 1, 121, 234, 14, 12134, 2, 134, 1213]

CLIFFORD_INVERSES = [0, 2, 1, 3, 8, 10, 6, 11, 4, 9, 5, 7, 12, 16, 23, 21, 13, 17, 18, 19, 20, 15, 22, 14]
"""List containing the inverse of each clifford gate in the CLIFFORD_GATES list."""

CLIFFORD_PRODUCTS = np.array(
    [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        [1, 2, 0, 4, 5, 3, 7, 8, 6, 10, 11, 9, 13, 14, 12, 16, 17, 15, 19, 20, 18, 22, 23, 21],
        [2, 0, 1, 5, 3, 4, 8, 6, 7, 11, 9, 10, 14, 12, 13, 17, 15, 16, 20, 18, 19, 23, 21, 22],
        [3, 10, 8, 0, 7, 11, 9, 4, 2, 6, 1, 5, 21, 16, 20, 18, 13, 23, 15, 22, 14, 12, 19, 17],
        [4, 11, 6, 1, 8, 9, 10, 5, 0, 7, 2, 3, 22, 17, 18, 19, 14, 21, 16, 23, 12, 13, 20, 15],
        [5, 9, 7, 2, 6, 10, 11, 3, 1, 8, 0, 4, 23, 15, 19, 20, 12, 22, 17, 21, 13, 14, 18, 16],
        [6, 4, 11, 9, 1, 8, 0, 10, 5, 3, 7, 2, 18, 22, 17, 21, 19, 14, 12, 16, 23, 15, 13, 20],
        [7, 5, 9, 10, 2, 6, 1, 11, 3, 4, 8, 0, 19, 23, 15, 22, 20, 12, 13, 17, 21, 16, 14, 18],
        [8, 3, 10, 11, 0, 7, 2, 9, 4, 5, 6, 1, 20, 21, 16, 23, 18, 13, 14, 15, 22, 17, 12, 19],
        [9, 7, 5, 6, 10, 2, 3, 1, 11, 0, 4, 8, 15, 19, 23, 12, 22, 20, 21, 13, 17, 18, 16, 14],
        [10, 8, 3, 7, 11, 0, 4, 2, 9, 1, 5, 6, 16, 20, 21, 13, 23, 18, 22, 14, 15, 19, 17, 12],
        [11, 6, 4, 8, 9, 1, 5, 0, 10, 2, 3, 7, 17, 18, 22, 14, 21, 19, 23, 12, 16, 20, 15, 13],
        [12, 23, 16, 15, 20, 13, 18, 17, 22, 21, 14, 19, 0, 5, 10, 3, 2, 7, 6, 11, 4, 9, 8, 1],
        [13, 21, 17, 16, 18, 14, 19, 15, 23, 22, 12, 20, 1, 3, 11, 4, 0, 8, 7, 9, 5, 10, 6, 2],
        [14, 22, 15, 17, 19, 12, 20, 16, 21, 23, 13, 18, 2, 4, 9, 5, 1, 6, 8, 10, 3, 11, 7, 0],
        [15, 14, 22, 12, 17, 19, 21, 20, 16, 18, 23, 13, 9, 2, 4, 6, 5, 1, 3, 8, 10, 0, 11, 7],
        [16, 12, 23, 13, 15, 20, 22, 18, 17, 19, 21, 14, 10, 0, 5, 7, 3, 2, 4, 6, 11, 1, 9, 8],
        [17, 13, 21, 14, 16, 18, 23, 19, 15, 20, 22, 12, 11, 1, 3, 8, 4, 0, 5, 7, 9, 2, 10, 6],
        [18, 20, 19, 21, 23, 22, 12, 14, 13, 15, 17, 16, 6, 8, 7, 9, 11, 10, 0, 2, 1, 3, 5, 4],
        [19, 18, 20, 22, 21, 23, 13, 12, 14, 16, 15, 17, 7, 6, 8, 10, 9, 11, 1, 0, 2, 4, 3, 5],
        [20, 19, 18, 23, 22, 21, 14, 13, 12, 17, 16, 15, 8, 7, 6, 11, 10, 9, 2, 1, 0, 5, 4, 3],
        [21, 17, 13, 18, 14, 16, 15, 23, 19, 12, 20, 22, 3, 11, 1, 0, 8, 4, 9, 5, 7, 6, 2, 10],
        [22, 15, 14, 19, 12, 17, 16, 21, 20, 13, 18, 23, 4, 9, 2, 1, 6, 5, 10, 3, 8, 7, 0, 11],
        [23, 16, 12, 20, 13, 15, 17, 22, 18, 14, 19, 21, 5, 10, 0, 2, 7, 3, 11, 4, 6, 8, 1, 9],
    ]
)
"""Matrix representation of the result of each clifford product. The element [i][j] of this matrix
corresponds to the product of the clifford gates i and j defined in the CLIFFORD_GATES list."""
