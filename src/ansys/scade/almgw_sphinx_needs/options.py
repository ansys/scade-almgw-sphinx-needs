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

"""Options of the sphinx-needs ALMW connector."""

from pathlib import Path

from scade.model.project.stdproject import Project

import ansys.scade.almgw_sphinx_needs as sn
import ansys.scade.pyalmgw as pyamlgw


class Options:
    """Gathers the settings of the ALMGW Connector for sphinx-needs."""

    def __init__(self) -> None:
        self.upstream_type = ''
        self.downstream_type = ''
        self.link_type = ''
        self.version = ''
        self.import_documents = []
        self.export_schema = ''
        self.export_document = None
        self.graphics = True

    def load(self, project: Project):
        """Update the dialog with the project's settings."""
        files = project.get_tool_prop_def(
            sn.TOOL, sn.IMPORT_DOCUMENTS, sn.IMPORT_DOCUMENTS_DEFAULT, None
        )
        directory = Path(project.pathname).resolve().parent
        for file in files:
            path = Path(file)
            if not path.is_absolute():
                path = directory.joinpath(path)
            self.import_documents.append(path.resolve())

        self.upstream_type = project.get_scalar_tool_prop_def(
            sn.TOOL, sn.UPSTREAM_TYPE, sn.UPSTREAM_TYPE_DEFAULT, None
        )

        self.downstream_type = project.get_scalar_tool_prop_def(
            sn.TOOL, sn.DOWNSTREAM_TYPE, sn.DOWNSTREAM_TYPE_DEFAULT, None
        )

        self.link_type = project.get_scalar_tool_prop_def(
            sn.TOOL, sn.LINK_TYPE, sn.LINK_TYPE_DEFAULT, None
        )

        self.version = project.get_scalar_tool_prop_def(
            sn.TOOL, sn.VERSION, sn.VERSION_DEFAULT, None
        )

        self.export_schema = project.get_scalar_tool_prop_def(
            pyamlgw.TOOL, pyamlgw.LLRSCHEMA, pyamlgw.LLRSCHEMA_DEFAULT, None
        )

        value = project.get_scalar_tool_prop_def(
            sn.TOOL, sn.EXPORT_DOCUMENT, sn.EXPORT_DOCUMENT_DEFAULT, None
        )
        if value:
            path = Path(value)
            if path and not path.is_absolute():
                path = directory.joinpath(path)
            self.export_document = path.resolve()

        self.graphics = project.get_bool_tool_prop_def(pyamlgw.TOOL, 'DIAGRAMS', False, None)
