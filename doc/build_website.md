# Website
The website is built using [Sphinx](https://www.sphinx-doc.org).
The Markdown files in `doc/source` are used as base and can be modified.

## Generate documentation
To generate the documentation, first install the required dependencies:
```console
pip install .[doc]
```
Then the documentation can be built with `make doc`.
Last, open the generated files [build/html/index.html](build/html/index.html) in a web-browser.

## Jupyter notebooks
The documentation uses [Myst Markdown](https://mystmd.org/) together with [Jupytext](https://jupytext.org/) to support Jupyter notebooks.
The command `make notebooks` automatically builds all notebooks next to their corresponding Markdown files.
Use `check-doc` to ensure that all generated notebooks can be executed successfully. This is also checked in the CI.
