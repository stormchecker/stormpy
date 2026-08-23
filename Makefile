.PHONY: default format notebooks doc check-docs clean-notebooks

# No default target
default:

# Execute formatting on all C++ files, all Python files and the Python code in the documentation
format:
	./resources/scripts/auto-format.sh
	black .
	jupytext --sync --pipe "python -m black {}" $$(grep -rl '^jupytext:' doc --include='*.md')

# Create Jupyter notebooks from Myst files in documentation
notebooks:
	jupytext --to notebook $$(grep -rl '^jupytext:' doc --include='*.md')

# Build the documentation
doc:
	$(MAKE) -C doc html

# Perform roundtrip check for documentation and execute all code cells
check-doc:
	jupytext --to ipynb --test-strict $$(grep -rl '^jupytext:' doc --include='*.md')
	for f in $$(grep -rl '^jupytext:' doc --include='*.md'); do \
		jupytext --to py:percent --output - $$f | python3 - || exit 1; \
	done

# Remove all generated Jupyter notebooks
clean-notebooks:
	find doc -name '*.ipynb' -delete
