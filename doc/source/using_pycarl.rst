****************************
Getting Started with Pycarl
****************************

Pycarl is shipped with the stormpy library and can be installed following the instructions for :doc:`installation`.

A Quick Tour through pycarl
===========================

We start by launching the python 3 interpreter::

	$ python3

First we import pycarl::

    >>>	from stormpy import pycarl

Pycarl can use two different number types: ``gmp`` and ``cln``.
In this example we will use ``gmp`` numbers and therefore import the corresponding module::

    >>> from stormpy.pycarl import gmp

	
Simple arithmetic operations
----------------------------
.. seealso:: `01-getting-started.py <https://github.com/moves-rwth/stormpy/blob/master/examples/pycarl/01-pycarl-getting-started.py>`_

We start by doing some simple arithmetic operations.
First we create two variables ``x`` and ``y``::

	>>> pycarl.clear_variable_pool()
	>>> x = pycarl.Variable("x")
	>>> y = pycarl.Variable("y")

We perform some operations on polynomials by using the common arithmetic operations of python::

	>>> pol1 = x * x + pycarl.gmp.Integer(2)
	>>> pol2 = y + pycarl.gmp.Integer(1)
	>>> result = pol1 * pol2
	>>> print("({}) * ({}) = {}".format(pol1, pol2, result))
	(x^2+2) * (y+1) = x^2*y+2*y+x^2+2
