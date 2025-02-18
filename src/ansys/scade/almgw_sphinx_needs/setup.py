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

"""
Command line utility to setup a project for the connector.

.. code:: text

    usage: setup_ansys_scade_almgw_sphinx_needs [-h] [-p <project>] [-u <upstream>]
                                                [-d <downstream>] [-l <link>] [-v <version>]
                                                [-s <schema>] [-o <output>] [-i [<inputs> ...]]
                                                [-g]

    options:
      -h, --help            show this help message and exit
      -p <project>, --project <project>
                            Ansys SCADE project (ETP)
      -u <upstream>, --upstream <upstream>
                            upstream type
      -d <downstream>, --downstream <downstream>
                            downstream type
      -l <link>, --link <link>
                            link type
      -v <version>, --version <version>
                            version of requirements
      -s <schema>, --schema <schema>
                            json export schema
      -o <output>, --output <output>
                            export document
      -i [<inputs> ...], --inputs [<inputs> ...]
                            requirements documents
      -g, --graphics        export diagrams
"""

from argparse import ArgumentParser, Namespace

# shall modify sys.path to access SCACE APIs
from ansys.scade.apitools import declare_project

# isort: split

from scade.model.project.stdproject import Project, get_roots as get_projects

import ansys.scade.almgw_sphinx_needs as sn
import ansys.scade.pyalmgw as pyamlgw


def setup(project: Project, options: Namespace) -> int:
    """Update the project with the settings."""
    project.set_tool_prop_def(
        sn.TOOL, sn.IMPORT_DOCUMENTS, options.inputs, sn.IMPORT_DOCUMENTS_DEFAULT, None
    )

    if options.upstream:
        project.set_scalar_tool_prop_def(
            sn.TOOL, sn.UPSTREAM_TYPE, options.upstream, sn.UPSTREAM_TYPE_DEFAULT, None
        )

    if options.downstream:
        project.set_scalar_tool_prop_def(
            sn.TOOL, sn.DOWNSTREAM_TYPE, options.downstream, sn.DOWNSTREAM_TYPE_DEFAULT, None
        )

    if options.link:
        project.set_scalar_tool_prop_def(
            sn.TOOL, sn.LINK_TYPE, options.link, sn.LINK_TYPE_DEFAULT, None
        )

    if options.version:
        project.set_scalar_tool_prop_def(
            sn.TOOL, sn.VERSION, options.version, sn.VERSION_DEFAULT, None
        )

    if options.schema:
        project.set_scalar_tool_prop_def(
            pyamlgw.TOOL, pyamlgw.LLRSCHEMA, options.schema, pyamlgw.LLRSCHEMA_DEFAULT, None
        )

    if options.output:
        project.set_scalar_tool_prop_def(
            sn.TOOL, sn.EXPORT_DOCUMENT, options.output, sn.EXPORT_DOCUMENT_DEFAULT, None
        )

    if options.graphics:
        project.set_bool_tool_prop_def(pyamlgw.TOOL, 'DIAGRAMS', options.graphics, False, None)

    project.save(project.pathname)
    return 0


def main() -> int:
    """Implement the ``ansys.scade.almgw_sphinx_needs.setup:main`` packages's project script."""
    parser = ArgumentParser()
    parser.add_argument(
        '-p', '--project', metavar='<project>', help='Ansys SCADE project (ETP)', default=''
    )
    parser.add_argument('-u', '--upstream', metavar='<upstream>', help='upstream type', default='')
    parser.add_argument(
        '-d', '--downstream', metavar='<downstream>', help='downstream type', default=''
    )
    parser.add_argument('-l', '--link', metavar='<link>', help='link type', default='')
    parser.add_argument(
        '-v', '--version', metavar='<version>', help='version of requirements', default=''
    )
    parser.add_argument('-s', '--schema', metavar='<schema>', help='json export schema', default='')
    parser.add_argument('-o', '--output', metavar='<output>', help='export document', default='')
    parser.add_argument(
        '-i', '--inputs', metavar='<inputs>', help='requirements documents', nargs='*', default=[]
    )
    parser.add_argument(
        '-g', '--graphics', action='store_true', help='export diagrams', default=False
    )

    options = parser.parse_args()

    assert declare_project
    declare_project(options.project)
    # must be one and only one project
    project = get_projects()[0]

    return setup(project, options)


if __name__ == '__main__':
    main()
