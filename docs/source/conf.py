import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "Eones"
copyright = "2025, Rodrigo Ezequiel Roldán"
author = "Rodrigo Ezequiel Roldán"
import eones

release = eones.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

myst_heading_anchors = 3

# Internationalization
locale_dirs = ["locale/"]  # path is example but original file: root is `docs/source`
gettext_compact = False  # optional

templates_path = ["_templates"]
exclude_patterns: list[str] = [
    "README.md",
    "examples/advanced_patterns.md",
    "examples/quick_start.md",
]

html_title = f"Eones {release}"
html_baseurl = "https://roldriel.github.io/eones/"
html_theme = "furo"
html_static_path = ["_static"]
autodoc_mock_imports = ["django", "sqlalchemy"]
html_theme_options = {
    "source_repository": "https://github.com/roldriel/eones",
    "source_branch": "master",
    "source_directory": "docs/source/",
}
