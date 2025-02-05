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

"""Digital Transpilation Configuration"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qibo.transpiler.placer import Placer
    from qibo.transpiler.router import Router


@dataclass
class DigitalTranspilationConfig:
    """Dataclass containing the digital transpilation configuration. Used in the :meth:`.CircuitTranspiler.transpile_circuit()` method"""

    routing: bool = False  # TODO: Change to True, when user confirms it works well.
    """(bool, optional): Whether to route the circuit. Defaults to False."""

    placer: Placer | type[Placer] | tuple[type[Placer], dict] | None = None
    """(Placer | type[Placer] | tuple[type[Placer], dict], optional): ``Placer`` instance, or subclass ``type[Placer]`` to
        use, with optionally, its kwargs dict (other than connectivity), both in a tuple. Defaults to ``ReverseTraversal``."""

    router: Router | type[Router] | tuple[type[Router], dict] | None = None
    """(Router | type[Router] | tuple[type[Router], dict], optional): ``Router`` instance, or subclass ``type[Router]`` to
        use, with optionally, its kwargs dict (other than connectivity), both in a tuple. Defaults to ``Sabre``."""

    routing_iterations: int = 10
    """(int, optional): Number of times to repeat the routing pipeline, to get the best stochastic result. Defaults to 10."""

    optimize: bool = False  # TODO: Maybe also change to True, when user confirms it works well.
    """(bool, optional): Whether to optimize the circuit and/or transpilation. Defaults to False."""

    @property
    def _attributes_ordered(self) -> tuple:
        """Returns the attributes of the dataclass in order, as a tuple."""
        return self.routing, self.placer, self.router, self.routing_iterations, self.optimize
