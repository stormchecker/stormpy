.PHONY: default format check check-doc check-format-doc notebooks doc clean-notebooks

# Use bash with pipefail, such that errors in all parts of a pipe are detected
SHELL := bash
.SHELLFLAGS := -o pipefail -c

PYTHON ?= python3
# Documentation pages written in MyST Markdown (paired with Jupyter notebooks via jupytext)
DOC_PAGES := $(shell grep -rl '^jupytext:' doc --include='*.md')

# No default target, only list the available targets
default:
	@echo "Available targets: format, check, check-format-doc, check-doc, notebooks, doc, clean-notebooks"

# Execute formatting on all C++ files, all Python files and the Python code in the documentation
format:
	./resources/scripts/auto-format.sh
	$(PYTHON) -m black .
	jupytext --sync --pipe "$(PYTHON) -m black {}" $(DOC_PAGES)

# Perform all checks
check: check-format-doc check-doc
	$(PYTHON) -m pytest .

# Check that all Python code in the documentation is formatted with black
check-format-doc:
	jupytext --pipe "$(PYTHON) -m black --check --diff {}" $(DOC_PAGES)

# Perform roundtrip check for documentation and execute all code cells
check-doc:
	jupytext --to ipynb --test-strict $(DOC_PAGES)
	@for f in $(DOC_PAGES); do \
		echo "Executing $$f"; \
		jupytext --to py:percent --output - $$f | $(PYTHON) - || { echo "Error while executing $$f"; exit 1; }; \
	done

# Create Jupyter notebooks from Myst files in documentation
notebooks:
	jupytext --to notebook $(DOC_PAGES)

# Build the documentation
doc:
	$(MAKE) -C doc html

# Remove all generated Jupyter notebooks
clean-notebooks:
	find doc -name '*.ipynb' -delete
