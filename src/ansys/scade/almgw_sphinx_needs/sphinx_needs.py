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

import json
from pathlib import Path
import shutil
import webbrowser

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools  # noqa: F401

# must be imported after apitools
# isort: split
from ansys.scade.almgw_sphinx_needs.export import export_document
from ansys.scade.almgw_sphinx_needs.needs import import_document, load_needs
from ansys.scade.almgw_sphinx_needs.options import Options
from ansys.scade.almgw_sphinx_needs.trace import TraceDocument
from ansys.scade.pyalmgw.connector import Connector
from ansys.scade.pyalmgw.documents import ReqProject


class SphinxNeeds(Connector):
    """Specialization of the connector for sphinx-needs."""

    def __init__(self):
        super().__init__('sphinx-needs')
        # all requirements
        self.map_requirements = {}

    def get_reqs_file(self) -> Path:
        """Return the path of the temporary file containing the requirements and traceability."""
        assert self.project
        return Path(self.project.pathname).with_suffix('.' + self.id + '.reqs')

    def get_trace_file(self) -> Path:
        """Return the path of the file containing the traceability."""
        assert self.project
        return Path(self.project.pathname).with_suffix('.' + self.id + '.trace')

    def on_settings(self, pid: int) -> int:
        """
        Stub the command ``settings``.

        Nothing to do, the settings are managed by a dedicated plug-in.

        Parameters
        ----------
        pid : int
            SCADE product process ID.

        Returns
        -------
        int

            * -1: if an error occurs, therefore previous settings information shall be kept
            * 0: set settings information shall be OK
            * 1: ALM Gateway project shall be removed, i.e., ALM connection shall be reset
        """
        print('settings: command not supported.')
        return 0

    def on_import(self, file: Path, pid: int) -> int:
        """
        Import requirements and traceability links to ALM Gateway.

        The function reads the requirements from the documents and
        adds the traceability data stored in a separate file.

        Parameters
        ----------
        path : Path
            Absolute path where the XML requirements file is saved.
        pid : int
            SCADE product process ID.

        Returns
        -------
        int

            * -1: if an error occurs, therefore previous export status
              and requirement tree shall be kept
            * 0: requirements and traceability links shall be correctly imported
        """
        assert self.project
        options = Options()
        options.load(self.project)
        if not options.import_documents:
            print('import: No documents')
            return -1

        self.map_requirements = {}
        project = ReqProject(file)
        self.read_requirements(project, options)

        links = TraceDocument(project, self.get_trace_file(), self.map_requirements)
        links.read()
        # write the file to remove pending links to unexisting requirements, if any
        links.write()

        project.write()

        # cache the requirements, for debug purpose
        cache = self.get_reqs_file()
        shutil.copyfile(file, cache)

        # req_file is updated
        print('requirements imported.')
        return 0

    def on_export(self, links: Path, pid: int) -> int:
        """
        Update the traceability data and produce a downstream document.

        This function updates the tracability data in a separate file.

        It produces the downstream when an export configuration
        file is specified in the project.

        Parameters
        ----------
        links : Path
            Path of a JSON file that contains the links to add and remove.
        pid : int
            SCADE product process ID.

        Returns
        -------
        int

            * -1: if an error occurs, therefore previous export status
              and requirement tree shall be kept
            * 0: requirements and traceability links shall not be exported
            * 1: requirements and traceability links shall be exported
            * 2: previous export status and requirement tree shall be kept
        """
        # update the cache, if exists
        cache = self.get_reqs_file()
        if not cache.exists():
            cache = None
            project = ReqProject()
        else:
            project = ReqProject(cache)
            project.read()
            # reset the tracebaility
            project.traceability_links = []
        # cache the links into a separate trace file since there's no way
        # to store traceability links within sphinx-needs (AFAIK)
        trace = TraceDocument(project, self.get_trace_file())
        trace.read()
        trace.merge_links(links)
        trace.write()

        if cache:
            # save the updated cache
            project.write()

        assert self.project
        options = Options()
        options.load(self.project)
        if not options.export_document:
            # error but return 1 since the traceability has been updated
            print('export: No document')
            return 1

        # TODO: add an option to export images
        model = self.export_llrs()
        if not model:
            # error but return 1 since the traceability has been updated
            print('llr generation failure')
            return 1

        # generation the rst document
        llrs = json.loads(model.read_text())
        assert llrs
        export_document(llrs, trace, options)
        print('requirements exported.')
        return 1

    def on_manage(self, pid: int) -> int:
        """
        Run a browser with the main page.

        Parameters
        ----------
        pid : int
            SCADE product process ID.

        Returns
        -------
        int

            * -1: if an error occurs launching the command
            * 0: if ‘Management Requirements’ UI of ALM tool is successfully launched
            * 1: to clean requirement list on the SCADE IDE ‘Requirements’ window
        """
        assert self.project
        options = Options()
        options.load(self.project)
        if not options.import_documents:
            print('manage: No documents')
            return -1
        first = options.import_documents[0]
        path = first.parent / 'index.html'
        return self.open_document(path, '')

    def on_locate(self, req: str, pid: int) -> int:
        """
        Run a browser with the document containing the requirement and locate it.

        Parameters
        ----------
        req : str
            Identifier of a requirement defined in a document.
        pid : int
            SCADE product process ID.

        Returns
        -------
        int

            * -1: if an error occurs while executing the command
            * 0: if the command is successfully executed
        """
        assert self.project
        options = Options()
        options.load(self.project)

        for path in options.import_documents:
            if path.suffix.lower() == '.json':
                _, needs = load_needs(path, options)
                need = needs.get(req)
                if need:
                    break
        else:
            print('locate: %s requirement not found' % req)
            return -1

        file = path.parent / (need['docname'] + '.html')
        return self.open_document(file, req)

    def open_document(self, file: Path, req: str):
        """Open the document, and locate the requirement when not empty."""
        if req:
            if False:
                # uses default browser but can't locate reqn with Firefox for example
                uri = file.as_uri()
            else:
                # might run Edge instead of a default browser
                uri = file.as_posix()
            uri += f'#{req}'
        else:
            uri = file.as_uri()
        return 0 if webbrowser.open(uri) else -1

    def read_requirements(self, project: ReqProject, options: Options):
        """Read all the requirements from the documents."""
        assert self.project

        self.map_requirements = {}

        for path in options.import_documents:
            if path.suffix.lower() == '.json':
                self.map_requirements.update(import_document(project, path, options))


def main():
    """Implement the ``ansys.scade.almgw_sphinx_needs:main`` packages's project script."""
    proxy = SphinxNeeds()
    return proxy.main()


if __name__ == '__main__':
    main()
