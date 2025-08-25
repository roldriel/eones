import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "Eones"
copyright = "2025, Rodrigo Ezequiel Roldán"
author = "Rodrigo Ezequiel Roldán"
release = "1.3.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

html_baseurl = "https://roldriel.github.io/eones/"
html_theme = "alabaster"
html_static_path = ["_static"]
autodoc_mock_imports = ["django", "sqlalchemy"]
html_theme_options = {
    "canonical_url": "https://roldriel.github.io/eones/",
}
html_context = {
    "display_github": True,
    "github_user": "roldriel",
    "github_repo": "eones",
    "github_version": "master",
    "conf_py_path": "/docs/",
}
