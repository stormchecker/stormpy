# Website
The website is built using [Sphinx](https://www.sphinx-doc.org).
The Markdown files in `doc/source` are used as base and can be modified.

## Generate documentation
To generate the documentation, first install the required dependencies:
```console
pip install .[doc]
```
Then build the documentation:
```console
cd doc
make html
```
Last, open the generated files [build/html/index.html](build/html/index.html) in a web-browser.
