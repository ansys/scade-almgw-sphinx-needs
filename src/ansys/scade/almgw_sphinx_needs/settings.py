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

"""Provides the ``sphinx-needs Settings`` command."""

from enum import Enum
import os
from pathlib import Path

from scade.model.project.stdproject import Project, get_roots as get_projects
from scade.tool.suite.gui.commands import Command, Menu
from scade.tool.suite.gui.dialogs import Dialog, file_open, file_save
from scade.tool.suite.gui.widgets import Button, CheckBox, EditBox, Label, ListBox, ObjectComboBox

import ansys.scade.almgw_sphinx_needs as sn
import ansys.scade.pyalmgw as pyamlgw

script_path = Path(__file__)
script_dir = script_path.parent

# -----------------------------------------------------------------------
# globals
# -----------------------------------------------------------------------

# default value, for compatibility with property pages
H_BUTTON = 20
H_COMBO = 130
H_EDIT = 20
H_LABEL = 20
H_LIST = 130
H_TREE = 30
# width of ... buttons
W_DOTS = 20

# left/right margin
hm = 15
# position / size for labels
xl = hm
wl = 140
# position / size for fields
xf = 160
wf = 250
# vertical start position
y = 7
# space between two lines
dy = 30

# width of the dialog, without margins
wd = xf - xl + wf

# ---------------------------------------------------------------------------
# reusable control library
# ---------------------------------------------------------------------------


# FileSelectorMode
class FSM(Enum):
    """Modes of the file selector bundle."""

    LOAD, SAVE = range(2)


class LabelEditBox(EditBox):
    """Bundles an edit box with a label."""

    def __init__(self, owner, text: str, wl: int, x=10, y=10, w=50, h=14, **kwargs):
        self.label = Label(owner, text, x=x, y=y + 4, w=wl, h=H_LABEL)
        super().__init__(owner, x=x + wl, y=y, w=w - wl, h=H_EDIT, **kwargs)
        self.owner = owner


class FileSelector(LabelEditBox):
    """Bundles a file selector widget with a label, edit and button."""

    def __init__(
        self,
        owner,
        text: str,
        extension: str,
        dir: str,
        filter: str,
        mode: FSM,
        wl: int,
        x=10,
        y=10,
        w=50,
        h=14,
        **kwargs,
    ):
        super().__init__(owner, text, wl, x=x, y=y, w=w - W_DOTS - 5, h=h, **kwargs)
        self.btn_dots = Button(
            owner, '...', x=x + w - W_DOTS, y=y, w=W_DOTS, h=H_BUTTON, on_click=self.on_click
        )
        self.owner = owner
        self.extension = extension
        self.dir = dir
        self.filter = filter
        self.mode = mode
        # set at runtime
        self.reldir = ''

    def on_click(self, button: Button):
        """Prompt the user for a configuration file."""
        name = self.get_name()
        name = '' if '$' in name else name
        dir = '' if '$' in self.dir else self.dir
        if dir and self.reldir:
            dir = str(Path(self.reldir) / dir)
        if self.mode == FSM.SAVE:
            pathname = file_save(name, self.extension, dir, self.filter)
        else:
            pathname = file_open(self.filter, dir)
        if pathname:
            if self.reldir:
                try:
                    pathname = os.path.relpath(pathname, self.reldir)
                except ValueError:
                    pass
            self.set_name(pathname)


class LabelComboBox(ObjectComboBox):
    """Bundles a combo box with a label."""

    def __init__(self, owner, text: str, wl: int, items, x=10, y=10, w=50, h=14, **kwargs):
        self.label = Label(owner, text, x=x, y=y + 4, w=wl, h=H_LABEL)
        super().__init__(owner, items, x=x + wl, y=y, w=w - wl, h=H_COMBO, **kwargs)
        self.owner = owner


# -----------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------

# overall dimensions
w_settings = wd + hm * 2
# something strange, need to add one level of margin more
w_settings += 15
h_settings = 410


class Settings(Dialog):
    """Settings editor for the connector."""

    # cache selected project between calls
    project = None

    def __init__(self):
        super().__init__('sphinx-needs Settings', w_settings, h_settings)

        # controls
        self.cb_projects = None
        self.ed_upstream_type = None
        self.ed_downstream_type = None
        self.ed_link_type = None
        self.ed_version = None
        self.ed_export_schema = None
        self.ed_export_document = None
        self.lb_import_documents = None
        self.pb_ok = None
        self.pb_cancel = None
        self.cb_graphics = None

        # runtime
        self.project = None

    def add_edit(self, y: int, text: str) -> EditBox:
        """Add an edit bundle with normalized positions."""
        edit = LabelEditBox(self, text, wl, x=xl, y=y, w=wd)
        return edit

    def add_file(
        self, y: int, text: str, extension: str, dir: str, filter: str, mode: FSM
    ) -> FileSelector:
        """Add a file selector bundle with normalized positions."""
        file = FileSelector(self, text, extension, dir, filter, mode, wl, x=xl, y=y, w=wd, h=H_EDIT)
        return file

    def on_build(self):
        """Build the dialog."""
        # alignment for the first line
        y = 7

        projects = get_projects()
        # reuse last selected project if any and still exists
        project = self.project if self.project in projects else projects[0]
        assert isinstance(project, Project)
        # reset current project
        self.project = None
        style = ['dropdownlist', 'sort']
        self.cb_projects = LabelComboBox(
            self,
            '&Project:',
            wl,
            projects,
            x=xl,
            y=y,
            w=wd,
            selection=project,
            style=style,
            on_change_selection=self.on_project_selection,
        )
        y += dy
        self.ed_upstream_type = self.add_edit(y, '&Upstream type:')
        y += dy
        self.ed_downstream_type = self.add_edit(y, '&Downstream type:')
        y += dy
        self.ed_link_type = self.add_edit(y, '&Traceability link type:')
        y += dy
        self.ed_version = self.add_edit(y, '&Version:')
        y += dy
        filter = 'Export schema (*.json)|*.json|All Files (*.*)|*.*||'
        # ? default_dir = os.path.dirname(project.pathname)
        default_dir = ''
        self.ed_export_schema = self.add_file(
            y, '&Export schema:', '.json', default_dir, filter, FSM.LOAD
        )
        y += dy
        filter = 'Raw export file (*.json)|*.json|Document (*.rst)|*.rst|All Files (*.*)|*.*||'
        # ? default_dir = os.path.dirname(project.pathname)
        default_dir = ''
        self.ed_export_document = self.add_file(
            y, 'E&xport document:', '.json', default_dir, filter, FSM.LOAD
        )
        y += dy
        self.cb_graphics = CheckBox(self, 'Export &graphics', x=xf, y=y, w=wf, h=H_BUTTON)
        y += dy
        Label(self, '&Requirements documents:', x=xl, y=y + 4, w=wl, h=H_LABEL)
        y += dy
        hd = h_settings - 85 - y
        self.lb_import_documents = ListBox(self, [], x=15, y=y, w=wd, h=hd, style=['sort'])
        y += hd + 10

        # width of a button
        wb = 65
        # space between buttons
        mb = 10
        self.pb_ok = Button(self, '&Add', x=xl, y=y, w=wb, h=H_BUTTON, on_click=self.on_add)
        self.pb_cancel = Button(
            self, 'Re&move', x=xl + wb + mb, y=y, w=wb, h=H_BUTTON, on_click=self.on_remove
        )
        self.pb_ok = Button(
            self, 'OK', x=xl + wd - wb * 2 - mb, y=y, w=wb, h=H_BUTTON, on_click=self.on_ok
        )
        self.pb_cancel = Button(
            self, 'Cancel', x=xl + wd - wb, y=y, w=wb, h=H_BUTTON, on_click=self.on_cancel
        )

        # side effect
        self.on_set_project(project)

    def on_set_project(self, project: Project):
        """Update the settings and the dialog after a project is selected."""
        if project == self.project:
            return
        if self.project:
            self.write_settings()
        self.project = project
        self.read_settings()

    def on_project_selection(self, cb: ObjectComboBox, index: int):
        """Update current project."""
        project = cb.get_selection()
        assert isinstance(project, Project)
        self.on_set_project(project)

    def on_ok(self, *args):
        """Save the changes and close the dialog."""
        self.write_settings()
        self.close()

    def on_cancel(self, *args):
        """Close the dialog."""
        self.close()

    def on_add(self, *args):
        """Prompt the user for a new document."""
        assert self.project

        path = file_open('Requirements Documents (*.json)|*.json|All Files (*.*)|*.*||')
        if path:
            assert self.lb_import_documents
            try:
                document = os.path.relpath(path, Path(self.project.pathname).parent)
            except ValueError:
                document = path
            documents = self.lb_import_documents.get_items()
            assert isinstance(documents, list)
            if document not in documents:
                documents.append(document)
                self.lb_import_documents.set_items(documents)

    def on_remove(self, *args):
        """Remove the selected documents."""
        assert self.lb_import_documents
        selected = self.lb_import_documents.get_selection()
        if selected:
            documents = [_ for _ in self.lb_import_documents.get_items() if _ not in selected]
            self.lb_import_documents.set_items(documents)

    def read_settings(self):
        """Update the dialog with the project's settings."""
        assert self.project

        assert self.lb_import_documents
        documents = self.project.get_tool_prop_def(
            sn.TOOL, sn.IMPORT_DOCUMENTS, sn.IMPORT_DOCUMENTS_DEFAULT, None
        )
        self.lb_import_documents.set_items(documents)

        assert self.ed_upstream_type
        upstream_type = self.project.get_scalar_tool_prop_def(
            sn.TOOL, sn.UPSTREAM_TYPE, sn.UPSTREAM_TYPE_DEFAULT, None
        )
        self.ed_upstream_type.set_name(upstream_type)

        assert self.ed_downstream_type
        downstream_type = self.project.get_scalar_tool_prop_def(
            sn.TOOL, sn.DOWNSTREAM_TYPE, sn.DOWNSTREAM_TYPE_DEFAULT, None
        )
        self.ed_downstream_type.set_name(downstream_type)

        assert self.ed_link_type
        link_type = self.project.get_scalar_tool_prop_def(
            sn.TOOL, sn.LINK_TYPE, sn.LINK_TYPE_DEFAULT, None
        )
        self.ed_link_type.set_name(link_type)

        assert self.ed_version
        version = self.project.get_scalar_tool_prop_def(
            sn.TOOL, sn.VERSION, sn.VERSION_DEFAULT, None
        )
        self.ed_version.set_name(version)

        assert self.ed_export_schema
        export_schema = self.project.get_scalar_tool_prop_def(
            pyamlgw.TOOL, pyamlgw.LLRSCHEMA, pyamlgw.LLRSCHEMA_DEFAULT, None
        )
        self.ed_export_schema.set_name(export_schema)
        self.ed_export_schema.reldir = str(Path(self.project.pathname).parent)

        assert self.ed_export_document
        export_document = self.project.get_scalar_tool_prop_def(
            sn.TOOL, sn.EXPORT_DOCUMENT, sn.EXPORT_DOCUMENT_DEFAULT, None
        )
        self.ed_export_document.set_name(export_document)
        self.ed_export_document.reldir = str(Path(self.project.pathname).parent)

        assert self.cb_graphics
        graphics = self.project.get_bool_tool_prop_def(pyamlgw.TOOL, 'DIAGRAMS', False, None)
        self.cb_graphics.set_check(graphics)

    def write_settings(self):
        """Update the project's settings from the dialog."""
        assert self.project

        assert self.lb_import_documents
        documents = self.lb_import_documents.get_items()
        self.project.set_tool_prop_def(
            sn.TOOL, sn.IMPORT_DOCUMENTS, documents, sn.IMPORT_DOCUMENTS_DEFAULT, None
        )

        assert self.ed_upstream_type
        upstream_type = self.ed_upstream_type.get_name()
        self.project.set_scalar_tool_prop_def(
            sn.TOOL, sn.UPSTREAM_TYPE, upstream_type, sn.UPSTREAM_TYPE_DEFAULT, None
        )

        assert self.ed_downstream_type
        downstream_type = self.ed_downstream_type.get_name()
        self.project.set_scalar_tool_prop_def(
            sn.TOOL, sn.DOWNSTREAM_TYPE, downstream_type, sn.DOWNSTREAM_TYPE_DEFAULT, None
        )

        assert self.ed_link_type
        link_type = self.ed_link_type.get_name()
        self.project.set_scalar_tool_prop_def(
            sn.TOOL, sn.LINK_TYPE, link_type, sn.LINK_TYPE_DEFAULT, None
        )

        assert self.ed_version
        version = self.ed_version.get_name()
        self.project.set_scalar_tool_prop_def(
            sn.TOOL, sn.VERSION, version, sn.VERSION_DEFAULT, None
        )

        assert self.ed_export_schema
        export_schema = self.ed_export_schema.get_name()
        self.project.set_scalar_tool_prop_def(
            pyamlgw.TOOL, pyamlgw.LLRSCHEMA, export_schema, pyamlgw.LLRSCHEMA_DEFAULT, None
        )

        assert self.ed_export_document
        export_document = self.ed_export_document.get_name()
        self.project.set_scalar_tool_prop_def(
            sn.TOOL, sn.EXPORT_DOCUMENT, export_document, sn.EXPORT_DOCUMENT_DEFAULT, None
        )

        assert self.cb_graphics
        graphics = self.cb_graphics.get_check()
        self.project.set_bool_tool_prop_def(pyamlgw.TOOL, 'DIAGRAMS', graphics, False, None)


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------


class CommandSettings(Command):
    """Defines a command to edit the settings."""

    def __init__(self):
        image = str(script_dir / 'res' / 'sphinx-needs.bmp')
        super().__init__(
            name='sphinx-needs Settings...',
            status_message='sphinx-needs Settings',
            tooltip_message='sphinx-needs Settings',
            image_file=image,
        )

    def on_activate(self):
        """Open the dialog."""
        Settings().do_modal()

    def on_enable(self):
        """Return whether the command is available."""
        return len(get_projects()) != 0


# -----------------------------------------------------------------------------
# GUI items
# -----------------------------------------------------------------------------

Menu([CommandSettings()], '&Project/ALM Gateway')
