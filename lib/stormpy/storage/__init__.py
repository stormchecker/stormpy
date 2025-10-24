import stormpy.utility
from . import _storage
from ._storage import *
from deprecated.sphinx import deprecated


def build_sparse_matrix(array, row_group_indices=[]):
    """
    Build a sparse matrix from numpy array.
    Zero entries are skipped.

    :param numpy array: The array.
    :param List[double] row_group_indices: List containing the starting row of each row group in ascending order.
    :return: Sparse matrix.
    """
    return _build_sparse_matrix(_storage.SparseMatrixBuilder, array, row_group_indices=row_group_indices)


def build_parametric_sparse_matrix(array, row_group_indices=[]):
    """
    Build a sparse matrix from numpy array.
    Zero entries are skipped.

    :param numpy array: The array.
    :param List[double] row_group_indices: List containing the starting row of each row group in ascending order.
    :return: Parametric sparse matrix.
    """
    return _build_sparse_matrix(_storage.ParametricSparseMatrixBuilder, array, row_group_indices=row_group_indices)


def _build_sparse_matrix(builder_class, array, row_group_indices=[]):
    """
    General method to build a sparse matrix from numpy array.
    Zero entries are skipped.

    :param class builder_class: The class type used to create the matrix builder.
    :param numpy array: The array.
    :param List[double] row_group_indices: List containing the starting row of each row group in ascending order.
    :return: Sparse matrix.
    """
    num_row = array.shape[0]
    num_col = array.shape[1]

    len_group_indices = len(row_group_indices)
    if len_group_indices > 0:
        builder = builder_class(rows=num_row, columns=num_col, has_custom_row_grouping=True, row_groups=len_group_indices)
    else:
        builder = builder_class(rows=num_row, columns=num_col)

    row_group_index = 0
    for r in range(num_row):
        # check whether to start a custom row group
        if row_group_index < len_group_indices and r == row_group_indices[row_group_index]:
            builder.new_row_group(r)
            row_group_index += 1
        # insert values of the current row
        for c in range(num_col):
            if array[r, c] != 0:
                builder.add_next_value(r, c, array[r, c])

    return builder.build()


def get_maximal_end_components(model):
    """
    Get maximal end components from model.
    :param model: Model.
    :return: Maximal end components.
    """
    if model.supports_parameters:
        return stormpy.MaximalEndComponentDecomposition_ratfunc(model)
    elif model.is_exact:
        return stormpy.MaximalEndComponentDecomposition_exact(model)
    elif model.supports_uncertainty:
        return stormpy.MaximalEndComponentDecomposition_interval(model)
    else:
        return stormpy.MaximalEndComponentDecomposition_double(model)


# Extend class StateValuation
def _get_value(self, state, var):
    """
    Get the value of the given variable at the given state.
    :param state: State.
    :param var: Variable.
    :return Value of var in state.
    """
    if var.has_boolean_type():
        return self._get_boolean_value(state, var)
    elif var.has_integer_type():
        return self._get_integer_value(state, var)
    elif var.has_rational_type():
        return self._get_rational_value(state, var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


def _get_values_states(self, var):
    """
    Get the value of the given variable of all states.
    :param var: Variable.
    :return Values of var. The i'th entry represents the value of state i.
    """
    if var.has_boolean_type():
        return self._get_boolean_values_states(var)
    elif var.has_integer_type():
        return self._get_integer_values_states(var)
    elif var.has_rational_type():
        return self._get_rational_values_states(var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


StateValuation.get_value = _get_value
StateValuation.get_values_states = _get_values_states


# Deprecated functions
@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_boolean_value(self, state, var):
    return self._get_boolean_value(state, var)


StateValuation.get_boolean_value = _get_boolean_value


@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_integer_value(self, state, var):
    return self._get_integer_value(state, var)


StateValuation.get_integer_value = _get_integer_value


@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_rational_value(self, state, var):
    return self._get_rational_value(state, var)


StateValuation.get_rational_value = _get_rational_value


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_boolean_values_states(self, var):
    return self._get_boolean_values_states(var)


StateValuation.get_boolean_values_states = _get_boolean_values_states


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_integer_values_states(self, var):
    return self._get_integer_values_states(var)


StateValuation.get_integer_values_states = _get_integer_values_states


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_rational_values_states(self, var):
    return self._get_rational_values_states(var)


StateValuation.get_rational_values_states = _get_rational_values_states


# Extend class SimpleValuation
def _get_value(self, var):
    """
    Get the value of the given variable.
    :param var: Variable.
    :return Value of var.
    """
    if var.has_boolean_type():
        return self._get_boolean_value(var)
    elif var.has_integer_type():
        return self._get_integer_value(var)
    elif var.has_rational_type():
        return self._get_rational_value(var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


SimpleValuation.get_value = _get_value


# Deprecated functions
@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_boolean_value(self, var):
    return self._get_boolean_value(var)


SimpleValuation.get_boolean_value = _get_boolean_value


@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_integer_value(self, var):
    return self._get_integer_value(var)


SimpleValuation.get_integer_value = _get_integer_value
