# -*- coding: utf-8 -*-

# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Ansys SCADE ALM Gateway connector for sphinx-needs."""

from pathlib import Path
import sys

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__.replace('.', '-'))
except importlib_metadata.PackageNotFoundError:
    # happens with pre-commit, the package is not installed in the virtual environment
    __version__ = '<unknown>'


_SPHINX_NEEDS = 'ALMGW Connector for sphinx-needs'

# settings
TOOL = 'SPHINX_NEEDS'
# import
UPSTREAM_TYPE = 'UPSTREAM_TYPE'
UPSTREAM_TYPE_DEFAULT = 'req'
IMPORT_DOCUMENTS = 'IMPORT_DOCUMENTS'
IMPORT_DOCUMENTS_DEFAULT = []
VERSION = 'VERSION'
VERSION_DEFAULT = ''
# traceabiity
LINK_TYPE = 'LINK_TYPE'
LINK_TYPE_DEFAULT = 'links'
# export
DOWNSTREAM_TYPE = 'DOWNSTREAM_TYPE'
DOWNSTREAM_TYPE_DEFAULT = 'sc'
EXPORT_DOCUMENT = 'EXPORT_DOCUMENT'
EXPORT_DOCUMENT_DEFAULT = ''


def get_srg_name() -> str:
    """
    Return the name of the registration file for Ansys SCADE IDE.

    It addresses SCADE 2024 R1 and prior releases.
    SCADE 2024 R2 and later use the package's
    ``ansys.scade.registry`` entry point.
    """
    # registrations depending on Python interpreter
    python_version = str(sys.version_info.major) + str(sys.version_info.minor)
    suffix = '23r1' if python_version == '37' else '24r1'
    return 'almgw_sphinx_needs%s.srg' % suffix


def srg() -> str:
    """
    Return the path of the SCADE Studio registry file.

    This function implements the entry point "ansys.scade.registry/srg"
    introduced in SCADE 2025 R1. It avoids creating an explicit srg file
    in ``%APPDATA%/Scade/Customize`` when the package is installed.
    """
    # the package's srg file is located in the same directory
    return str(Path(__file__).parent / 'almgw_sphinx_needs.srg')


def exe() -> tuple[str, str]:
    """
    Return the path of the connector's executable.

    This function implements the entry point "ansys.almgw.connector/exe"
    introduced in SCADE 2025 R1. It avoids creating an explicit properties file
    in ``$(SCADE)/SCADE LifeCycle/ALM Gateway/external`` when the package is installed.
    """
    # the connector is either in:
    # * Lib/site-packages/ansys/scade/almgw_sphinx_needs (pip install)
    # * site-packages/ansys/scade/almgw_sphinx_needs (pip install --user)
    # * src/ansys/scade/almgw_sphinx_needs (pip install --editable)
    site_packages = Path(__file__).parent.parent.parent.parent
    if site_packages.name == 'src':
        # install in user mode, consider the default namings
        python_dir = site_packages.parent / '.venv'
    else:
        python_dir = site_packages.parent
        if python_dir.name.lower() == 'lib':
            python_dir = python_dir.parent
    # the exe is in Scripts
    return _SPHINX_NEEDS, str(python_dir / 'Scripts' / 'ansys_scade_almgw_sphinx_needs.exe')
