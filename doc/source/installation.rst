***********************
Installation
***********************

Installing stormpy
==================

In most cases, it suffices to install the stormpy Python package, for example via::

        $ pip install stormpy

After the stormpy package was successfully installed, you can continue with :doc:`getting_started`.


Manually Building Stormpy
=========================

The remainder describes the steps to manually build stormpy.


Requirements
------------

Before installing stormpy, make sure

- Python 3 is available on your system.
- (optional) `Storm <https://www.stormchecker.org/>`_ is available


.. _compatibility_stormpy_storm:

Compatibility of stormpy and Storm
----------------------------------
By default, stormpy will automatically install a compatible Storm.
Alternatively, stormpy can use an existing installation of Storm.
We refer to the `Storm documentation <https://www.stormchecker.org/documentation/obtain-storm/build.html>`_ for detailed installation instructions of Storm.
The location of an existing Storm installation can be provided as an :ref:`optional argument<optional_build_arguments>` during the build step of stormpy.

Note that stormpy and Storm are continuously extended and modified.
It is therefore important to use compatible versions of stormpy and Storm.
Stormpy and Storm are compatible if they share the same major and minor version ``x.y``.
Stormpy version ``x.y.z`` is compatible with Storm version ``x.y.z'``.

You have two choices for stormpy depending on the version of Storm you are using:

1. **Release version**:
   You use the latest `release of Storm <https://github.com/moves-rwth/storm/releases>`_ or the ``stable`` branch.
   In these cases, you need to use the latest `release of stormpy <https://github.com/moves-rwth/stormpy/releases>`_.

2. **Master branch**:
   You use the ``master`` branch of Storm.
   In this case, you need to use the ``master`` branch of stormpy as well.
   Note that due to ongoing development in Storm, after some commits, the stormpy ``master`` might not work with the Storm ``master`` anymore.
   We will fix such issues as fast as possible.

.. warning::
    Unfortunately, Stormpy currently does not work in conjunction with a homebrew installation of Storm.


Virtual Environments
--------------------
Virtual environments create isolated environments for your projects.
This helps to keep your system clean, work with different versions of packages and different version of Python.
While it is not required, we recommend the use of such virtual environments. To get you started, we recommend
`this guide <https://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ or
`this primer <https://realpython.com/blog/python/python-virtual-environments-a-primer>`_.

In short you can create a virtual environment ``env`` with::

	$ python -m venv env
	$ source env/bin/activate

The last step activates the virtual environment.
Whenever using the environment, the console prompt is prefixed with ``(env)``.


Building stormpy
----------------
**Clone** the :ref:`compatible stormpy version<compatibility_stormpy_storm>` into any suitable location.
For the ``master`` of stormpy use::

	$ git clone https://github.com/moves-rwth/stormpy.git
	$ cd stormpy

or for the latest release use the ``stable`` branch::

	$ git clone https://github.com/moves-rwth/stormpy.git -b stable
	$ cd stormpy

**Build** stormpy using your favourite Python distribution way of installing, for example::

	$ pip install -v .


.. _optional_build_arguments:

Optional build arguments
^^^^^^^^^^^^^^^^^^^^^^^^

The build step also takes optional CMake arguments via ``--config-settings=cmake.define.<cmake_option>=<value>`` (or short ``-Ccmake.define.<cmake_option>=<value>``) for a more advanced configuration of stormpy.
We refer to the section ``[tool.scikit-build.cmake.define]`` in ``pyproject.toml`` for a full list of configuration options.

Using system version of Storm
"""""""""""""""""""""""""""""
By default, stormpy is first searching for a local installation of Storm.
Usage of the system version of Storm can be configured with the following flags:

* ``--config-settings=cmake.define.ALLOW_STORM_SYSTEM=OFF`` disables searching for a system version of Storm.
* ``--config-settings=cmake.define.STORM_DIR_HINT=<dir>`` sets the hint for the Storm directory.
  In case of a manually built Storm, the path should point to the build directory.

Using fetched version of Storm
""""""""""""""""""""""""""""""
If no system version of Storm could be found, Storm is automatically fetched and installed.
Fetching a Storm version can be configured with the following flags:

* ``--config-settings=cmake.define.ALLOW_STORM_FETCH=OFF`` disables fetching of Storm.
* ``--config-settings=cmake.define.STORM_GIT_REPO=<url>`` changes the Git repository used for fetching Storm.
* ``--config-settings=cmake.define.STORM_GIT_TAG=<tag>`` changes the Git tag used for fetching Storm.

Using carl-parser
"""""""""""""""""
The `carl-parser <https://github.com/moves-rwth/carl-parser>`_ library supports parsing of carl-storm data structures.
Usage of carl-parser can be configured with the following flags:

* ``--config-settings=cmake.define.USE_PARSER=OFF`` disables support for the carl-parser.
* ``--config-settings=cmake.define.CARLPARSER_DIR_HINT=<dir>`` sets the hint for the carl-parser directory.
  In case of a manually built carl-parser, the path should point to the build directory.

Disabling functionality
"""""""""""""""""""""""
If you want to disable certain functionality in stormpy from being built you can add the following flags:

* ``--config-settings=cmake.define.USE_STORM_DFT=OFF`` to disable support for dynamic fault trees (DFTs).
* ``--config-settings=cmake.define.USE_STORM_GSPN=OFF`` to disable support for generalized stochastic Petri nets (GSPNs).
* ``--config-settings=cmake.define.USE_STORM_PARS=OFF`` to disable support for parametric models.
* ``--config-settings=cmake.define.USE_STORM_POMDP=OFF`` to disable support for POMDPs.

Building stormpy in debug mode
""""""""""""""""""""""""""""""
If you want to build stormpy in debug mode you can add the flag ``--config-settings=cmake.build-type='Debug'``.

Setting number of build threads
"""""""""""""""""""""""""""""""
If you want to configure the number of threads used to build stormpy, use the flag ``--config-settings=cmake.define.CMAKE_BUILD_PARALLEL_LEVEL=<number_of_jobs>``.
Alternatively, you can set the prefix ``CMAKE_BUILD_PARALLEL_LEVEL=<number_of_jobs> pip install ...``.


Testing stormpy installation
----------------------------

After building, you can run the test files by invoking pytest directly with::

	$ pip install pytest
	$ py.test tests/

If the tests pass, you can now use stormpy.
To get started, continue with our :doc:`getting_started`, consult the test files in ``tests/`` or the :doc:`api` (work in progress).


Building stormpy documentation
==============================

To build this documentation, you need a local installation of stormpy.
In addition, the `pandoc <https://pandoc.org/>`_ library is required as well as additional Python libraries.
You can install the required Python dependencies automatically with::

	$ pip install .[doc,numpy]

Then build the documentation::

	$ cd doc
	$ make html
