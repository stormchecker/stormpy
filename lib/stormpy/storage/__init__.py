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


# Extend class Valuations
def _get_value(self, state, var):
    """
    Get the value of the given variable at the given state/entity.
    :param state: State or entity index.
    :param var: Variable.
    :return Value of var in state.
    """
    if var.has_boolean_type():
        return self._get_boolean_value(state, var)
    elif var.has_integer_type():
        return self._get_int64_value(state, var)
    elif var.has_rational_type():
        return self._get_rational_value(state, var)
    elif var.has_string_type():
        return self._get_string_value(state, var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


def _get_values_states(self, var):
    """
    Get the value of the given variable of all states/entities.
    :param var: Variable.
    :return Values of var. The i'th entry represents the value of entity i.
    """
    if var.has_boolean_type():
        return self._get_boolean_values_states(var)
    elif var.has_integer_type():
        return self._get_int64_values_states(var)
    elif var.has_rational_type():
        return self._get_rational_values_states(var)
    elif var.has_string_type():
        return self._get_string_values_states(var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


def _write_value(self, entity, var, value):
    """
    Write the value of the given variable at the given entity.
    :param entity: Entity index.
    :param var: Variable.
    :param value: Value to write.
    """
    if var.has_boolean_type():
        self.write_bool_value(entity, var, value)
    elif var.has_integer_type():
        self.write_int64_value(entity, var, value)
    elif var.has_rational_type():
        self.write_rational_value(entity, var, value)
    elif var.has_string_type():
        self.write_string_value(entity, var, value)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


def _get_boolean_values_states_as_bitvector(self, var):
    """
    Get the value of the given Boolean variable of all states/entities, as a BitVector.
    More efficient than get_values_states, since it avoids materializing a per-entity Python
    list. Note that iterating the result yields the indices of the entities where the value
    is true (BitVector's standard iteration semantics), not a per-entity true/false sequence;
    use indexing (result[i]) or get_values_states if you need per-entity values.
    :param var: Boolean variable.
    :return: BitVector where bit i is set iff var is true for entity i.
    """
    if not var.has_boolean_type():
        raise ValueError(f"Variable {var} is not a Boolean variable")
    return self._get_boolean_values_states_as_bitvector(var)


def _get_integer_bigint_value(self, state, var):
    """
    Get the value of the given integer variable at the given state/entity, as an
    arbitrary-precision integer. Only needed for integer variables declared with
    arbitrary-precision bounds (via the Integer-bounds overload of add_integer_variable)
    whose value does not fit in an int64; get_value already handles the common case.
    :param state: State or entity index.
    :param var: Integer variable.
    :return: Value of var in state, as a stormpy.pycarl.gmp.Integer.
    """
    if not var.has_integer_type():
        raise ValueError(f"Variable {var} is not an integer variable")
    return self._get_integer_bigint_value(state, var)


def _write_integer_bigint_value(self, entity, var, value):
    """
    Write an arbitrary-precision integer value for the given entity and variable. Only needed
    for integer variables declared with arbitrary-precision bounds whose value does not fit in
    an int64; write_value already handles the common case.
    :param entity: Entity index.
    :param var: Integer variable.
    :param value: Value to write, as a stormpy.pycarl.gmp.Integer (or anything convertible to it).
    """
    if not var.has_integer_type():
        raise ValueError(f"Variable {var} is not an integer variable")
    self._write_integer_bigint_value(entity, var, value)


def _get_double_value(self, state, var):
    """
    Get the value of the given rational variable at the given state/entity, decoded from the
    double (64-bit IEEE754) storage encoding. Note that "double" is not a distinct variable
    type: it is an approximate storage encoding for rational variables, chosen on the builder
    via add_double_variable as an alternative to the exact encoding of add_rational_variable.
    Only use this if you know the variable was declared that way; get_value/get_values_states
    cannot tell the two encodings apart from the variable alone.
    :param state: State or entity index.
    :param var: Rational variable that was declared via add_double_variable.
    :return: Value of var in state, as a Python float.
    """
    if not var.has_rational_type():
        raise ValueError(f"Variable {var} is not a rational variable")
    return self._get_double_value(state, var)


def _get_double_values_states(self, var):
    """
    Get the value of the given rational variable of all states/entities, decoded from the
    double (64-bit IEEE754) storage encoding. See get_double_value for when to use this.
    :param var: Rational variable that was declared via add_double_variable.
    :return: Values of var. The i'th entry represents the value of entity i.
    """
    if not var.has_rational_type():
        raise ValueError(f"Variable {var} is not a rational variable")
    return self._get_double_values_states(var)


def _write_double_value(self, entity, var, value):
    """
    Write a value for the given rational variable and entity, using the double (64-bit
    IEEE754) storage encoding. See get_double_value for when to use this.
    :param entity: Entity index.
    :param var: Rational variable that was declared via add_double_variable.
    :param value: Value to write, as a Python float.
    """
    if not var.has_rational_type():
        raise ValueError(f"Variable {var} is not a rational variable")
    self._write_double_value(entity, var, value)


Valuations.get_value = _get_value
Valuations.get_values_states = _get_values_states
Valuations.write_value = _write_value
Valuations.get_boolean_values_states_as_bitvector = _get_boolean_values_states_as_bitvector
Valuations.get_integer_bigint_value = _get_integer_bigint_value
Valuations.write_integer_bigint_value = _write_integer_bigint_value
Valuations.get_double_value = _get_double_value
Valuations.get_double_values_states = _get_double_values_states
Valuations.write_double_value = _write_double_value


# Deprecated functions
@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_boolean_value(self, state, var):
    return self._get_boolean_value(state, var)


Valuations.get_boolean_value = _get_boolean_value


@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_integer_value(self, state, var):
    return self._get_int64_value(state, var)


Valuations.get_integer_value = _get_integer_value


@deprecated("Use general method 'get_value' instead.", version="1.10.0")
def _get_rational_value(self, state, var):
    return self._get_rational_value(state, var)


Valuations.get_rational_value = _get_rational_value


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_boolean_values_states(self, var):
    return self._get_boolean_values_states(var)


Valuations.get_boolean_values_states = _get_boolean_values_states


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_integer_values_states(self, var):
    return self._get_int64_values_states(var)


Valuations.get_integer_values_states = _get_integer_values_states


@deprecated("Use general method 'get_values_states' instead.", version="1.10.0")
def _get_rational_values_states(self, var):
    return self._get_rational_values_states(var)


Valuations.get_rational_values_states = _get_rational_values_states


@deprecated("Use get_nr_of_entities instead.", version="1.13.2")
def _get_nr_of_states(self):
    return self.get_nr_of_entities()


Valuations.get_nr_of_states = _get_nr_of_states

# Deprecated class alias
StateValuation = Valuations


@deprecated("Use ValuationDescriptionBuilder and Valuations instead.", version="1.10.0")
class StateValuationsBuilder:
    """
    Deprecated shim for the old state-valuations builder API.

    Buffers the variables and per-state values passed via add_variable/add_state, and only
    constructs the new ValuationDescriptionBuilder/Valuations objects once build() is called
    (integer bounds are derived automatically from the buffered values, since the new API
    requires them upfront but the old one did not).
    """

    def __init__(self):
        self._boolean_vars = []
        self._integer_vars = []
        self._rational_vars = []
        self._states = {}
        self._manager = None

    def add_variable(self, variable):
        """
        Adds a new variable.
        :param variable: Variable.
        """
        if self._manager is None:
            self._manager = variable.manager
        if variable.has_boolean_type():
            self._boolean_vars.append(variable)
        elif variable.has_integer_type():
            self._integer_vars.append(variable)
        elif variable.has_rational_type():
            self._rational_vars.append(variable)
        else:
            raise ValueError(f"Variable {variable} has unsupported type")

    def add_state(self, state, boolean_values=None, integer_values=None, rational_values=None):
        """
        Adds a new state, no more variables should be added afterwards.
        :param state: State.
        :param boolean_values: Values for the boolean variables, in the order they were added.
        :param integer_values: Values for the integer variables, in the order they were added.
        :param rational_values: Values for the rational variables, in the order they were added.
        """
        values = {}
        for var, val in zip(self._boolean_vars, boolean_values or []):
            values[var] = val
        for var, val in zip(self._integer_vars, integer_values or []):
            values[var] = val
        for var, val in zip(self._rational_vars, rational_values or []):
            values[var] = val
        self._states[state] = values

    def build(self):
        """
        Creates the finalized valuations object.
        """
        if self._manager is None:
            raise ValueError("No variables were added to the builder")

        desc_builder = ValuationDescriptionBuilder(self._manager)
        for var in self._boolean_vars:
            desc_builder.add_boolean_variable(var)
        for var in self._integer_vars:
            observed = [values[var] for values in self._states.values() if var in values]
            lower_bound = min(observed) if observed else 0
            upper_bound = max(observed) if observed else 0
            desc_builder.add_integer_variable(var, int(lower_bound), int(upper_bound))
        for var in self._rational_vars:
            desc_builder.add_rational_variable(var, 128)
        class_description = desc_builder.build_class_description()

        num_entities = max(self._states.keys()) + 1 if self._states else 0
        valuations = Valuations(class_description, self._manager, num_entities)
        for state, values in self._states.items():
            for var, val in values.items():
                valuations.write_value(state, var, val)
        return valuations


@deprecated("Use ValuationTransformer instead.", version="1.10.0")
class StateValuationTransformer(ValuationTransformer):
    """
    Deprecated shim for the old state-valuation transformer API.
    """

    @deprecated("Use general method 'add_expression' instead.", version="1.10.0")
    def add_boolean_expression(self, expression_variable, defining_expression):
        self.add_expression(expression_variable, defining_expression)

    @deprecated("Use general method 'add_expression' instead.", version="1.13.2")
    def add_integer_expression(self, expression_variable, defining_expression):
        self.add_expression(expression_variable, defining_expression)


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
    elif model.supports_uncertainty:
        raise NotImplementedError(f"product_model is not supported for interval models")
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
    elif isinstance(product_scheduler, _storage.Scheduler):
        return self._reverse_scheduler_double(product_scheduler)
    else:
        raise ValueError(f"Unsupported scheduler type: {type(product_scheduler)}")


SparseModelMemoryProductReverseData.reverse_scheduler = _reverse_scheduler
