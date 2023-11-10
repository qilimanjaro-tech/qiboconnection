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

r"""
This module contains a function to display all the details of the Qiboconnection installation.
"""
import platform
import sys
from subprocess import check_output  # nosec B404

import qibo


def about():
    """
    Prints the information for qiboconnection installation.
    """
    print(check_output([sys.executable, "-m", "pip", "show", "qiboconnection"]).decode())  # nosec B603
    print(f"Platform info:           {platform.platform(aliased=True)}")
    print(f"Python version:          {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    print(f"Qibo version:            {qibo.__version__}")
