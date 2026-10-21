# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Needed for version information
import pathlib
import sys
from functools import partial
from importlib import import_module

import stormpy

# Load optional public owners before selecting the remaining developer bindings.
for module in ("stormpy.dft", "stormpy.gspn", "stormpy.pars", "stormpy.pomdp"):
    try:
        import_module(module)
    except ImportError as error:
        print(f"Could not import optional module {module}: {error}", file=sys.stderr)

sys.path.insert(0, str(pathlib.Path(__file__).parent / "_ext"))
from stormpy_autosummary import _filter_api_members, canonical_api_alias
from stormpy_templates import template_families, template_functions, template_info, template_function_info

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "stormpy"
copyright = "2016-2026 Storm Developers"
author = "Sebastian Junges, Matthias Volk"
release = stormpy.__version__
language = "en"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "stormpy_templates",
    "stormpy_developer",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    #'sphinx.ext.intersphinx',
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "myst_nb",
]
autosectionlabel_prefix_document = True

# Autodoc options
autoclass_content = "both"  # Add documentation for both the class and __init__

# Autosummary options
# Also list members that are re-exported (e.g. classes defined in the
# compiled _logic module and imported into stormpy.logic)
autosummary_imported_members = True

# Variables (and callables) available in autosummary templates
# Sphinx excludes bare functions from cached config. Partials preserve their
# callable behavior and can be pickled through the imported functions.
autosummary_context = {
    name: partial(function)
    for name, function in {
        "filter_api_members": _filter_api_members,
        "canonical_api_alias": canonical_api_alias,
        "template_families": template_families,
        "template_functions": template_functions,
        "template_info": template_info,
        "template_function_info": template_function_info,
    }.items()
}

# Wrap long signatures instead of scrolling them
python_maximum_signature_line_length = 100

templates_path = ["_templates"]
exclude_patterns = []

add_module_names = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_nefertiti"
html_theme_options = {
    ## Font options
    "sans_serif_font": "Nunito",
    "monospace_font": "Ubuntu Sans Mono",
    ## Style options
    "style": "blue",
    "style_header_neutral": False,
    "pygments_light_style": "pastie",
    "pygments_dark_style": "dracula",
    "logo": "storm_logo.png",
    "logo_width": 36,
    "logo_height": 36,
    "logo_alt": "Storm logo",
    ## Repos
    "repository_name": "stormpy",
    "repository_url": "https://github.com/stormchecker/stormpy",
    ## Header options
    "header_links_in_2nd_row": False,
    "header_links": [
        {
            "text": "Getting Started",
            "link": "getting_started",
        },
        {
            "text": "Documentation",
            "match": "doc/*",
            "dropdown": (
                {
                    "text": "Advanced Examples",
                    "link": "advanced_topics",
                },
                {
                    "divider": True,
                },
                {
                    "text": "Getting Started with Pycarl",
                    "link": "using_pycarl",
                },
            ),
        },
        {
            "text": "API",
            "link": "api",
            "match": "api/*",
        },
        {
            "text": "Extensions API",
            "link": "extensions_api",
            "match": "extensions_api/*",
        },
        {
            "text": "Developer API",
            "link": "developer_api",
            "match": "developer_api/*",
        },
        {
            "text": "Storm",
            "link": "https://www.stormchecker.org/",
        },
    ],
    ## Footer options
    "footer_links": [
        {
            "text": "Documentation",
            "link": "https://stormchecker.github.io/stormpy/",
        },
        {
            "text": "Package",
            "link": "https://pypi.org/project/stormpy/",
        },
        {
            "text": "Repository",
            "link": "https://github.com/stormchecker/stormpy/",
        },
        {
            "text": "Issues",
            "link": "https://github.com/stormchecker/stormpy/issues",
        },
    ],
    "show_powered_by": True,
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = "_static/favicon.png"

# Execute notebooks with missing cached outputs; reuse cached results when sources are unchanged
myst_nb_execution_mode = "cache"

# Allow header anchors for deeper level
myst_heading_anchors = 3


# Documentation pages that are paired jupytext notebooks (used for binder badges)
_source_dir = pathlib.Path(__file__).parent
notebook_docs = sorted(str(p.relative_to(_source_dir).with_suffix("")) for p in _source_dir.rglob("*.md") if "jupytext:" in p.read_text(errors="ignore")[:500])
html_context = {"notebook_docs": notebook_docs}


# -- Myst options --
myst_enable_extensions = [
    "colon_fence",
]
