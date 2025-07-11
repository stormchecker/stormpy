***********************
Installation
***********************

Requirements
==================

Before installing stormpy, make sure

- Python 3 is available on your system.
- `Storm <https://www.stormchecker.org/>`_ is available on your system.

.. _compatibility_stormpy_storm:

Compatibility of stormpy and Storm
----------------------------------
Note that stormpy and Storm are continuously extended and modified.
It is therefore important to use compatible versions of stormpy and Storm.
You have two choices for stormpy depending on the version of Storm you are using:

1. **Release version**:
   You use the latest `release of Storm <https://github.com/moves-rwth/storm/releases>`_ or the ``stable`` branch.
   In these cases, you need to use the latest `release of stormpy <https://github.com/moves-rwth/stormpy/releases>`_.
   For example, Storm |version| is compatible with stormpy |version|.

2. **Master branch**:
   You use the ``master`` branch of Storm.
   In this case, you need to use the ``master`` branch of stormpy as well.
   Note that due to ongoing development in Storm, after some commits, the stormpy ``master`` might not work with the Storm ``master`` anymore.
   We will fix such issues as fast as possible.

.. warning::
    Unfortunately, Stormpy currently does not work in conjunction with a homebrew installation of Storm.

Installation Steps
====================

Virtual Environments
--------------------

Virtual environments create isolated environments for your projects.
This helps to keep your system clean, work with different versions of packages and different version of python.
While it is not required, we recommend the use of such virtual environments. To get you started, we recommend
`this guide <https://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ or
`this primer <https://realpython.com/blog/python/python-virtual-environments-a-primer>`_.

In short you can create a virtual environment ``env`` with::

	$ pip install virtualenv
	$ virtualenv -p python3 env
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

**Build** stormpy in using your favourite python distribution way of installing: e.g.::

	$ pip install -v .


Optional build arguments
^^^^^^^^^^^^^^^^^^^^^^^^

The build step also takes optional CMake arguments via ``--config-settings=cmake.define.<cmake_option>=<value>`` for a more advanced configuration of stormpy.
We refer to the section ``[tool.scikit-build.cmake.define]`` in ``pyproject.toml`` for a full list of configuration options.

*	*Specifying which Storm library to use*

	If you have multiple versions of Storm or CMake is not able to find your Storm version,
	you can specify the directories via the following flags:

	* ``--config-settings=cmake.define.STORM_DIR_HINT=<dir>`` to set the hint for the Storm directory
	* ``--config-settings=cmake.define.CARL_DIR_HINT=<dir>`` to set the hint for the carl-storm directory
	* ``--config-settings=cmake.define.CARLPARSER_DIR_HINT=<dir>`` to set the hint for the carl-parser directory

*	*Disabling functionality*

	If you want to disable certain functionality in stormpy from being built you can add the following flags:

	* ``--config-settings=cmake.define.USE_STORM_DFT=OFF`` to disable support for dynamic fault trees (DFTs)
	* ``--config-settings=cmake.define.USE_STORM_GSPN=OFF`` to disable support for generalized stochastic Petri nets (GSPNs)
	* ``--config-settings=cmake.define.USE_STORM_PARS=OFF`` to disable support for parametric models
	* ``--config-settings=cmake.define.USE_STORM_POMDP=OFF`` to disable support for POMDPs
	* ``--config-settings=cmake.define.USE_PARSER=OFF`` to disable support for the carl-parser

*	*Building stormpy in debug mode*

	If you want to build stormpy in debug mode you can add the flag ``--config-settings=cmake.build-type='Debug'``.

*	*Setting number of build threads*

	If you want to configure the number of threads used to build stormpy, use the flag ``--config-settings=cmake.define.CMAKE_BUILD_PARALLEL_LEVEL=<number_of_jobs>``.


Testing stormpy installation
----------------------------

After building, you can run the test files by invoking pytest directly with::

	$ pip install pytest
	$ py.test tests/

If the tests pass, you can now use stormpy.
To get started, continue with our :doc:`getting_started`, consult the test files in ``tests/`` or the :doc:`api` (work in progress).

Building stormpy documentation
------------------------------

To build this documentation, you need additional python dependencies as well as `pandoc <https://pandoc.org/>`_.
You can install the required python dependencies automatically with::

	$ pip install .[doc,numpy]

Then build the documentation::

	$ cd doc
	$ make html
