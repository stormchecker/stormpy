# Website
The website is built using [Sphinx](https://www.sphinx-doc.org).
The Markdown files in `doc/source` are used as base and can be modified.

## Generate documentation
To generate the documentation, first install the required dependencies:
```console
pip install .[doc]
```
Then the documentation can be built with `nox -s doc` (from the repository root) or `make html` (from the `doc` directory).
Last, open the generated files [build/html/index.html](build/html/index.html) in a web-browser.

## Maintaining the API documentation

The API indexes use standard Sphinx autosummary blocks. When adding or moving
modules, update the appropriate index: [`source/api.md`](source/api.md) for core
modules, [`source/extensions_api.md`](source/extensions_api.md) for extensions,
or [`source/developer_api.md`](source/developer_api.md) for internal bindings.
Keep public modules alphabetical and each number backend next to its formula
module in the developer index.

## Jupyter notebooks
The documentation uses [Myst Markdown](https://mystmd.org/) together with [Jupytext](https://jupytext.org/) to support Jupyter notebooks.
The command `nox -s notebooks` automatically builds all notebooks next to their corresponding Markdown files, and `nox -s clean_notebooks` removes them again.
Use `nox -s check_doc` to ensure that all generated notebooks can be executed successfully. This is also checked in the CI.
