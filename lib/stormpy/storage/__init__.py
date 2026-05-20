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
    nz_rows, nz_cols = array.nonzero()
    nz_vals = array[nz_rows, nz_cols]
    if len_group_indices > 0:
        builder = builder_class(rows=num_row, columns=num_col, entries=len(nz_rows), has_custom_row_grouping=True, row_groups=len_group_indices)
    else:
        builder = builder_class(rows=num_row, columns=num_col, entries=len(nz_rows))
    builder.add_next_values(nz_rows.tolist(), nz_cols.tolist(), nz_vals.tolist(), row_group_indices)
    return builder.build()


def get_maximal_end_components(model):
    """
    Get maximal end components from model.
    :param model: Model.
    :return: Maximal end components.
    """
    if model.supports_parameters:
        return stormpy.MaximalEndComponentDecomposition_ratfunc(model)
    elif model.supports_uncertainty and model.is_exact:
        return stormpy.MaximalEndComponentDecomposition_ratinterval(model)
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


# Extend class MemoryStructure
def product_model(self: MemoryStructure, model):
    """
    Compute the product of the memory structure with the model.
    """
    if model.supports_parameters:
        return self._product_model_parametric(model)
    elif model.is_exact:
        return self._product_model_exact(model)
    else:
        return self._product_model_double(model)


MemoryStructure.product_model = product_model


# Extend class SparseModelMemoryProductReverseData
def _reverse_scheduler(self, product_scheduler):
    if isinstance(product_scheduler, _storage.SchedulerParametric):
        return self._reverse_scheduler_parametric(product_scheduler)
    elif isinstance(product_scheduler, _storage.SchedulerExact):
        return self._reverse_scheduler_exact(product_scheduler)
    else:
        return self._reverse_scheduler_double(product_scheduler)


SparseModelMemoryProductReverseData.reverse_scheduler = _reverse_scheduler
