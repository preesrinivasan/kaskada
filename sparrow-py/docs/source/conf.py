"""Sphinx configuration."""
import sys
from pathlib import Path
from typing import Any
from typing import Dict


sys.path.append(str(Path(".").resolve()))

project = "sparrow-py"
author = "Kaskada Contributors"
copyright = "2023, Kaskada Contributors"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_design",
    # "myst_parser",
    "myst_nb",
    "sphinx_copybutton",
    "_extensions.gallery_directive",
]
autodoc_typehints = "description"
language = "en"

html_theme = "sphinx_book_theme"
html_favicon = "_static/favicon.png"
html_logo = "_static/kaskada.svg"
html_title = "Kaskada Timestreams"

html_theme_options: Dict[str, Any] = {
    "repository_url": "https://github.com/kaskada-ai/kaskada",
    "use_repository_button": True,
    "use_source_button": True,
    "use_edit_page_button": True,
    "home_page_in_toc": True,
    "use_issues_button": True,
    "repository_branch": "main",
    "path_to_docs": "sparrow-py/docs/source",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/kaskada-ai/kaskada",  # required
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "Slack",
            "url": "https://join.slack.com/t/kaskada-hq/shared_invite/zt-1t1lms085-bqs2jtGO2TYr9kuuam~c9w",
            "icon": "fa-brands fa-slack",
        },
    ],
    "primary_sidebar_end": ["indices.html"],
}

templates_path = ["_templates"]
html_static_path = ["_static"]

html_context = {
    "github_user": "kaskada-ai",
    "github_repo": "kaskada",
    "github_version": "main",
    "doc_path": "sparrow-py/docs/source",
}

intersphinx_mapping: Dict[str, Any] = {
    "python": ("http://docs.python.org/3", None),
    "pandas": ("http://pandas.pydata.org/docs", None),
    "pyarrow": ("https://arrow.apache.org/docs", None),
}

# adds useful copy functionality to all the examples; also
# strips the '>>>' and '...' prompt/continuation prefixes.
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True

# Options for Todos
todo_include_todos = True

# Options for Myst (markdown)
# https://myst-parser.readthedocs.io/en/v0.17.1/syntax/optional.html
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "smartquotes",
    "replacements",
]
myst_heading_anchors = 3

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

autosummary_generate = True

napoleon_preprocess_types = True
