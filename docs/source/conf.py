import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

project = 'Eones'
copyright = '2025, Rodrigo Ezequiel Roldán'
author = 'Rodrigo Ezequiel Roldán'
release = '1.0.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
autodoc_mock_imports = ["django", "sqlalchemy"]
