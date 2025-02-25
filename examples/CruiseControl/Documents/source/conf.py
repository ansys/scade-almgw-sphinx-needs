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

"""Sphinx documentation configuration file."""

# Project information
project = 'Cruise control'
author = 'ANSYS, Inc.'
release = '0.1.dev0'

# Select desired logo, theme, and declare the html title
html_short_title = html_title = 'sphinx-needs'

# Sphinx extensions
extensions = [
    # "sphinx_design",
    'sphinx_needs',
]

# static path
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# sphinx-needs configuration
needs_types = [
    # high level requirement
    {
        'directive': 'hlr',
        'title': 'REQ',
        'prefix': '',
    },
    # low level requirement
    {
        'directive': 'llr',
        'title': 'SC',
        'prefix': '',
    },
]

# traceability link produced by the connector
needs_extra_links = [
    {
        'option': 'covers',
        'incoming': 'is covered by',
        'outgoing': 'covers',
    },
]

needs_extra_options = [
    # mandatory connector options
    'scade_path',
    'scade_type',
    'scade_url',
    'scade_icon',
    # when export graphics is selected: image of the element
    'image',
    # field 'Nature' of the DesignElement annotation
    'Nature',
]

# define a custom layout to
# * add the icon
# * hide the id
needs_layouts = {
    'scade-suite': {
        'grid': 'simple',
        'layout': {
            'head': [
                '<<meta("type_name")>>: <<image("{{scade_icon}}")>> '
                '**<<meta("title")>>**>> '
                '<<collapse_button("meta", collapsed="icon:arrow-down-circle", '
                'visible="icon:arrow-right-circle", initial=True)>>'
            ],
            'meta': [
                '<<meta_all(exclude=["scade_icon", "image", "layout"], no_links=True)>>',
                'covers: <<meta_links("covers", incoming=False)>>',
            ],
        },
    }
}

# override the default regular expression for SCADE Suite OIDs
needs_id_regex = r'^[A-Za-z0-9_!/]{5,}'

# export the needs to a json file, to be imported by the connector
needs_build_json = True

# reduce the size of the file
needs_json_remove_defaults = True
