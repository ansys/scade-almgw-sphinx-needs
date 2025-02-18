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

from pathlib import Path

import ansys.scade.almgw_sphinx_needs.needs as needs
from tests.conftest import diff_files

_test_dir = Path(__file__).parent.parent / 'tests'
_ref_dir = _test_dir / 'ref'


def test_needs(local_tmpdir):
    """Make sure the result is identical to the reference."""
    ref = _ref_dir / 'needs.xml'
    dst = local_tmpdir / 'needs.xml'
    project = needs.ReqProject(dst)
    path = Path(__file__).parent / 'Documents' / '_build' / 'html' / 'needs.json'
    options = needs.Options()
    options.upstream_type = 'hlr'
    options.version = ''
    reqs = needs.import_document(project, path, options)
    assert len(reqs) > 1
    print(str(reqs))
    project.write()

    assert not diff_files(ref, dst)


if __name__ == '__main__':
    tmp = Path(__file__).parent / 'tmp'
    tmp.mkdir(exist_ok=True)
    test_needs(tmp)
