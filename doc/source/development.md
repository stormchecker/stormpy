# Developer information
The following contains some general guidelines for developers.

## Structure
- C++ bindings are defined in ``src``.
- Python methods are defined in ``lib/stormpy``.
- Tests are given in ``tests``.
- The Sphinx documentation can be found in ``doc/source``.


## Coding conventions
### Formatting
- Code should be formatted according to the given rules set by [black](https://black.readthedocs.io) (for Python).
  Proper formatting can be ensured by executing ``black .``.
  The CI automatically checks for proper formatting as well.


## Dependencies
- The bindings are created with [pybind11](https://pybind11.readthedocs.io).
  The pybind11 version is set in ``pyproject.toml`` through ``requires``, and in ``CMakeLists.txt`` through ``find_package(pybind11 ...)``.
- The minimal Python version is set in ``pyproject.toml`` through ``requires-python``, and in ``CMakeLists.txt`` through ``find_package(Python ...)``.
- The [Storm](https://www.stormchecker.org) version is set in ``pyproject.toml`` through ``STORM_GIT_TAG``, and in ``CMakeLists.txt`` through ``STORM_MIN_VERSION``.
