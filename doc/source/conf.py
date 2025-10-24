# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Needed for version information
import stormpy

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "stormpy"
copyright = "2016-2025 Storm Developers"
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
    "nbsphinx",
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
    "repository_url": "https://github.com/moves-rwth/stormpy",
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
            "link": "https://moves-rwth.github.io/stormpy/",
        },
        {
            "text": "Package",
            "link": "https://pypi.org/project/stormpy/",
        },
        {
            "text": "Repository",
            "link": "https://github.com/moves-rwth/stormpy/",
        },
        {
            "text": "Issues",
            "link": "https://github.com/moves-rwth/stormpy/issues",
        },
    ],
    "show_powered_by": True,
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = "_static/favicon.png"


# -- Nbsphinx options----- ---------------------------------------------------
# Need to set newer require.js version to fix javascript issues with older version
nbsphinx_requirejs_path = "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.7/require.min.js"

# Add binder badge
nbsphinx_prolog = """
{% set docname = env.doc2path(env.docname, base=False) %}

.. raw:: html

    <div class="admonition note">
      Try online: <span><a href="https://mybinder.org/v2/gh/moves-rwth/stormpy/master?filepath=notebooks/{{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="margin-bottom: 0rem"></a></span>
    </div>
"""
