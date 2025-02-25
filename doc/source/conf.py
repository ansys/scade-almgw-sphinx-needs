"""Sphinx documentation configuration file."""

from datetime import datetime
import os

from ansys_sphinx_theme import (
    ansys_favicon,
    get_version_match,
)

from ansys.scade.almgw_sphinx_needs import __version__

# Project information
project = 'ansys-scade-almgw-sphinx-needs'
copyright = f'(c) {datetime.now().year} ANSYS, Inc. All rights reserved'
author = 'ANSYS, Inc.'
release = version = __version__
switcher_version = get_version_match(version)

# Select desired logo, theme, and declare the html title
html_theme = 'ansys_sphinx_theme'
html_short_title = html_title = 'Ansys SCADE ALM Gateway connector for sphinx-needs'

# multi-version documentation
cname = os.getenv('DOCUMENTATION_CNAME', 'sphinx-needs.scade.docs.pyansys.com')
"""The canonical name of the webpage hosting the documentation."""

# specify the location of your github repo
html_theme_options = {
    'github_url': 'https://github.com/ansys-internal/scade-almgw-sphinx-needs',
    'show_prev_next': False,
    'show_breadcrumbs': True,
    'additional_breadcrumbs': [
        ('PyAnsys', 'https://docs.pyansys.com/'),
    ],
    'switcher': {
        'json_url': f'https://{cname}/versions.json',
        'version_match': switcher_version,
    },
    'check_switcher': False,
    'logo': 'pyansys',
}

# Sphinx extensions
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
]

# Optionally include api generation.
BUILD_API = os.environ.get('BUILD_API', 'false') == 'true'
if BUILD_API:
    extensions.append('ansys_sphinx_theme.extension.autoapi')
    html_theme_options['ansys_sphinx_theme_autoapi'] = {
        'project': project,
        'own_page_level': 'function',
        'class_content': 'both',  # documentation in https://sphinxdocs.ansys.com/version/stable/user-guide/autoapi.html
        'member_order': 'alphabetical',
    }

# Configuration for Sphinx autoapi
# dependencies might not be found when building the documentation
suppress_warnings = ['autoapi.python_import_resolution']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# Favicon
html_favicon = ansys_favicon

# static path
html_static_path = ['_static']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# TODO: remove ignore links after public release
linkcheck_ignore = [
    'https://github.com/ansys-internal/scade-almgw-sphinx-needs',
    'https://github.com/ansys-internal/scade-almgw-sphinx-needs/actions/workflows/ci_cd.yml',
    'https://pypi.org/project/ansys-scade-almgw-sphinx-needs',
    # The link below takes a long time to check
    'https://www.ansys.com/products/embedded-software/ansys-scade-suite',
    'https://www.ansys.com/*',
]

if switcher_version != 'dev':
    linkcheck_ignore.append(
        f'https://github.com/ansys-internal/scade-almgw-sphinx-needs/releases/tag/v{__version__}'
    )
