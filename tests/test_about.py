"""Unit tests for the `about` function."""
import io
import platform
import sys
from subprocess import check_output

import qibo

import qiboconnection as qc


def test_about():
    """Test that the `about` function prints the correct information."""
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect output
    qc.about()
    sys.stdout = sys.__stdout__  # Reset redirect

    expected_string = f"""{check_output([sys.executable, "-m", "pip", "show", "qiboconnection"]).decode()}
Platform info:           {platform.platform(aliased=True)}
Python version:          {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}
Qibo version:            {qibo.__version__}
"""

    assert expected_string == captured_output.getvalue()
