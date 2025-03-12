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

"""Export to a sphinx-needs document (JSON, RST)."""

import datetime
import json
from pathlib import Path
import shutil
from typing import List

import ansys.scade.almgw_sphinx_needs as sn
from ansys.scade.almgw_sphinx_needs.options import Options
from ansys.scade.almgw_sphinx_needs.trace import TraceDocument


def export_document(llrs: dict, trace: TraceDocument, options: Options):
    """Export the LLRs to sphinx-needs."""
    path = options.export_document
    assert path
    if path.suffix.lower() == '.json':
        _export_to_json(llrs, trace, options)
    elif path.suffix.lower() == '.rst':
        _export_to_rst(llrs, trace, options)


def _export_to_json(llrs: dict, trace: TraceDocument, options: Options):
    def export_section(context: List[str], section: dict):
        for element in section['elements']:
            export_element(context + [section['name']], element)

    def export_req(context: List[str], llr: dict):
        oid = llr['oid']
        title = llr['name']
        scade_type = llr['scadetype']
        scade_type = scade_type[0].upper() + scade_type[1:]
        scade_path = llr['pathname']
        scade_url = llr['url']
        icon = llr['icon']
        if not icon:
            icon = Path(__file__).parent / 'res' / '_null.png'
        image = llr.get('image', '')
        need = {}
        need['id'] = oid
        need['type'] = options.downstream_type
        need['title'] = title
        # content = f'`{scade_type} {scade_path} <{scade_url}>`_'
        # need['content'] = content
        need['scade_type'] = scade_type
        need['scade_path'] = scade_path
        need['scade_url'] = scade_url
        # copy the image to the target directory
        if image:
            src = Path(image)
            dst = target_dir / '_static' / src.name.replace(' ', '_')
            dst.parent.mkdir(exist_ok=True)
            shutil.copyfile(src, dst)
            need['image'] = dst.as_posix()
        else:
            need['image'] = '<null>'
        # copy the icon to the target directory
        src = Path(icon)
        dst = target_dir / '_static' / src.name.replace(' ', '_')
        dst.parent.mkdir(exist_ok=True)
        if not dst.exists():
            shutil.copyfile(src, dst)
        need['scade_icon'] = dst.as_posix()
        # additional attributes, must be declared in conf.py
        for attribute in llr.get('attributes', []):
            need[attribute['name']] = attribute['value']
        links = map_links.get(oid, [])
        need[options.link_type] = [_.target for _ in links]
        if context:
            # TODO: is that considered?
            need['sections'] = context
            need['section_name'] = context[-1]
            # TODO: does this make sense?
            need['sections'] = context
        # TODO: icon relevant here? if yes, copy to target dir
        # TODO: image relevant here?
        needs[oid] = need

    def export_element(context: List[str], element: dict):
        if element['almtype'] == 'section':
            export_section(context, element)
        elif element['almtype'] == 'req':
            export_req(context, element)

    assert options.export_document
    target_dir = options.export_document.parent
    images = target_dir / '_static'
    images.mkdir(exist_ok=True)

    # cache for links: list of targets for a source
    map_links = {}
    for link in trace.links.values():
        map_links.setdefault(link.source, []).append(link)

    root = {}
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    root['created'] = now
    root['current_version'] = ''
    root['project'] = llrs['name']
    version = {}
    root['versions'] = {options.version: version}
    version['created'] = now
    version['creator'] = {'program': sn.__name__, 'version': sn.__version__}
    needs = {}
    version['needs'] = needs

    for element in llrs['elements']:
        export_element([], element)

    options.export_document.write_text(json.dumps(root, indent=4))


def _export_to_rst(llrs: dict, trace: TraceDocument, options: Options):
    pass
