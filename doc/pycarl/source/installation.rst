***********************
Installation
***********************

Requirements
==================

Before installing pycarl, make sure

- Python 3 is available on your system. Pycarl does not work with python 2.
- Storm's fork of `carl <https://github.com/moves-rwth/carl-storm/>`_ is available on your system.
- *(optional)* in order to have full parsing capabilities, you additionally need `carl-parser <https://github.com/moves-rwth/carl-parser>`_.

.. note:: Users of Apple Silicon systems need to make sure that they are using an arm64 version of Python 3. You can find out using ``where python3`` and  ``file /your/path/to/python3``.


Installation Steps
====================

Virtual Environments
--------------------

Virtual environments create isolated environments for your projects.
This helps to keep your system clean, work with different versions of packages and different version of python.
While it is not required, we recommend the use of such virtual environments. To get you started, we recommend
`this guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ or
`this primer <https://realpython.com/blog/python/python-virtual-environments-a-primer>`_.

In short you can create a virtual environment ``env`` with::

	$ pip install virtualenv
	$ virtualenv -p python3 env
	$ source env/bin/activate

The last step activates the virtual environment.
Whenever using the environment the console prompt is prefixed with ``(env)``.


Building pycarl
---------------

Clone pycarl into any suitable location::

	$ git clone https://github.com/moves-rwth/pycarl.git
	$ cd pycarl

Build pycarl in develop mode using your favourite python distribution way of installing: e.g.::

	$ python3 setup.py develop

or::

	$ pip install -ve .


Optional build arguments
^^^^^^^^^^^^^^^^^^^^^^^^

The build step also takes optional arguments for a more advanced configuration of pycarl.

*	*Specifying which carl library to use*

	If you have multiple versions of carl or cmake is not able to find your carl version,
	you can specify the ``--carl-dir YOUR-PATH-TO-CARL`` flag in the ``build_ext`` step::

	$ python3 setup.py build_ext --carl-dir YOUR-PATH-TO-CARL develop

*	*Disabling functionality*

	If you want to disable certain functionality in pycarl from being built you can use the following flags:

	* ``--disable-cln`` to disable support for CLN numbers
	* ``--disable-parser`` to disable support for full parsing capabilities

*	*Building pycarl in debug mode*

	If you want to build pycarl in debug mode you can add the ``--debug`` flag in the ``build_ext`` step::

	$ python3 setup.py build_ext --debug develop

*	*Setting number of build threads*

	The build of pycarl uses all available cores per default.
	If you want to configure the number of threads manually you can specify the ``--jobs`` (or ``-j``) flag::

	$ python3 setup.py build_ext --jobs 2 develop

Testing pycarl installation
---------------------------
After building, you can run the test files by either::

	$ python setup.py test

or by invoking pytest directly with::

	$ pip install pytest
	$ py.test tests/

If you do not experience any issues, you can now use pycarl. To get started, follow the :doc:`getting_started`, consult the test files in ``tests/`` or the :doc:`api` (work in progress).
