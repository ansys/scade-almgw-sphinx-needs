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

"""Unit tests utils."""

import difflib
from pathlib import Path
from shutil import rmtree
from typing import Tuple

import pytest

# note: importing apitools modifies sys.path to access SCADE APIs
import ansys.scade.apitools  # noqa: F401

# must be imported after apitools
# isort: split
import scade
import scade.model.project.stdproject as std
import scade.model.suite as suite
import scade.model.testenv as qte

from ansys.scade.almgw_sphinx_needs import __version__
from ansys.scade.apitools.info import get_scade_home


@pytest.fixture(scope='session')
def local_tmpdir():
    """Create/empty the temporary directory for output files."""
    script_path = Path(__file__)
    path = script_path.parent / 'tmp'
    try:
        rmtree(str(path))
    except FileNotFoundError:
        pass
    path.mkdir()
    return path


def load_session(*paths: Path) -> suite.Session:
    """
    Create an instance of Session instance and load the requested models.
    """
    session = suite.Session()
    for path in paths:
        session.load2(str(path))
    return session


def load_project(path: Path) -> std.Project:
    """
    Load a Scade project in a separate environment.

    Note: Undocumented API.
    """
    # scade is a CPython module defined dynamically
    project = scade.load_project(str(path))  # type: ignore
    return project


def load_project_session(path: Path, *paths: Path) -> Tuple[std.Project, suite.Session]:
    project = load_project(path)
    if not paths:
        paths = (path,)
    session = load_session(*paths)
    if session.model:
        # bind the project to the main model
        session.model.project = project
    return project, session


def load_project_test(path: Path) -> Tuple[std.Project, qte.TestApplication]:
    project = load_project(path)
    application = qte.TestApplication()
    for file_ref in project.file_refs:
        if Path(file_ref.pathname).suffix.lower() == '.stp':
            application.load_procedure_tcl(file_ref.pathname)
    return project, application


def cmp_file(reference: Path, result: Path, n=3, linejunk=None):
    """Return the differences between the reference and the result file."""
    # reference: replace $(ROOT) and $(SCADE) with runtime data
    ref_lines = reference.open().read().split('\n')
    root = Path(__file__).parent.parent.as_posix()
    scade_home = get_scade_home().as_posix()
    ref_lines = [
        _.replace('$(ROOT)', root)
        .replace('$(SCADE)', scade_home)
        .replace('$(DIR)', result.parent.as_posix())
        .replace('$(VERSION)', __version__)
        for _ in ref_lines
    ]
    with result.open() as f:
        if linejunk:
            res_lines = [_ for _ in f if not linejunk(_)]
        else:
            res_lines = f.read().split('\n')

    diff = difflib.context_diff(ref_lines, res_lines, str(reference), str(result), n=n)
    return diff


def diff_files(ref: Path, dst: Path) -> bool:
    print('compare', str(ref), str(dst))
    diffs = cmp_file(ref, dst)
    failure = False
    for d in diffs:
        print(d.rstrip('\r\n'))
        failure = True
    return failure
