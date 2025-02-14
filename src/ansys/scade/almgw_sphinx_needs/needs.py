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

"""Extraction of the requirements of a sphinx-needs document (JSON)."""

import json
from pathlib import Path
from typing import Dict, Tuple

from ansys.scade.almgw_sphinx_needs.options import Options
from ansys.scade.pyalmgw.documents import ReqDocument, ReqProject, Requirement, Section


class Parser:
    """Parser for sphinx-needs documents (JSON)."""

    def __init__(self):
        # dictionary of requirements
        self.requirements = {}

    def parse(self, req_doc: ReqDocument, needs: Dict[str, dict], options: Options):
        """Build the document model from a sphinx-needs document."""
        # dictionary of sections
        sections = {}

        for id, need in needs.items():
            if need['type'] != options.upstream_type:
                continue

            assert id == need['id']
            section_name = need.get('section_name')
            content = need['content']
            # convert paragraph separators obvioumarkers
            description = content.replace('\n\n', '\n').replace('``', '`')
            title = need['title']
            text = f'[{id}] {title}'

            if not section_name:
                # not sure this may happen: defensive programming
                section = req_doc
            else:
                section = sections.get(section_name)
                if not section:
                    section = Section(req_doc, '', section_name)
                    sections[section_name] = section
            req = Requirement(section, id, text=text, description=description)
            self.requirements[id] = req


def load_needs(path: Path, options: Options) -> Tuple[str, Dict[str, dict]]:
    """Load the dictionary of needs for a given configuration."""
    content = json.loads(path.read_text())
    name = content['project']
    version = content['versions'].get(options.version, {})
    needs = version['needs'] if version else {}
    return name, needs


def import_document(project: ReqProject, path: Path, options: Options) -> Dict[str, Requirement]:
    """Parse the input sphinx-needs document and return the contained requirements hierarchy."""
    name, needs = load_needs(path, options)
    req_doc = ReqDocument(project, path.as_posix(), name)
    parser = Parser()
    parser.parse(req_doc, needs, options)
    return parser.requirements
