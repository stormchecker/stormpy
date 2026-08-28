# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Needed for version information
import pathlib

import stormpy

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
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    #'sphinx.ext.intersphinx',
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "myst_nb",
]
autosectionlabel_prefix_document = True

# Autodoc options
autoclass_content = "both"  # Add documentation for both the class and __init__

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
myst_nb_execution_timeout = -1  # parity with make check-docs: no per-cell timeout


# Documentation pages that are paired jupytext notebooks (used for binder badges)
_source_dir = pathlib.Path(__file__).parent
notebook_docs = sorted(str(p.relative_to(_source_dir).with_suffix("")) for p in _source_dir.rglob("*.md") if "jupytext:" in p.read_text(errors="ignore")[:500])
html_context = {"notebook_docs": notebook_docs}
