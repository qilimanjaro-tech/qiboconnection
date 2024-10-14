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

# Installation script for python
import os
import re
from pathlib import Path

from setuptools import find_packages, setup

PACKAGE = "qiboconnection"


# Returns the library version
def get_version():
    """Gets the version from the package's __init__ file
    if there is some problem, let it happily fail"""
    VERSIONFILE = os.path.join("src", PACKAGE, "__init__.py")
    with open(VERSIONFILE, "rt", encoding="utf-8") as version_file:
        initfile_lines = version_file.readlines()
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        for line in initfile_lines:
            mo = re.search(VSRE, line, re.MULTILINE)
            if mo:
                return mo.group(1)
        return None


# Read in requirements
with open("requirements.txt", encoding="utf-8") as requirements_file:
    requirements = [r.strip() for r in requirements_file]


# load long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


setup(
    name="qiboconnection",
    version=get_version(),
    description="Python interface to Qilimanjaro's Services for quantum job executions.",
    author="Qilimanjaro",
    author_email="info@qilimanjaro.tech",
    url="https://github.com/qilimanjaro-tech/qiboconnection",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.out"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=requirements,
    extras_require={
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "recommonmark",
            "sphinxcontrib-bibtex",
            "sphinx_markdown_tables",
            "nbsphinx",
            "IPython",
        ],
        "tests": ["pytest"],
    },
    python_requires=">=3.10.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
