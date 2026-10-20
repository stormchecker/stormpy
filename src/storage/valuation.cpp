#include "valuation.h"

#include <stdexcept>
#include <storm/adapters/JsonAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/expressions/ExpressionManager.h>
#include <storm/expressions/SimpleValuation.h>
#include <storm/expressions/Variable.h>
#include <storm/storage/BitVector.h>
#include <storm/storage/valuations/ValuationDescription.h>
#include <storm/storage/valuations/ValuationDescriptionBuilder.h>
#include <storm/storage/valuations/ValuationTransformer.h>
#include <storm/storage/valuations/Valuations.h>
#include <storm/storage/valuations/ValuationsStorage.h>

#include "src/helpers.h"

using Valuations = storm::storage::sparse::Valuations;
using ValuationDescriptionBuilder = storm::storage::sparse::ValuationDescriptionBuilder;
using ValuationClassDescription = storm::storage::sparse::ValuationClassDescription;

void define_valuation(py::module& m) {
    // Opaque description type — constructed via ValuationDescriptionBuilder, passed to Valuations constructor
    py::classh<ValuationClassDescription>(m, "ValuationClassDescription", "Schema describing the variables of a valuation class");

    py::classh<ValuationDescriptionBuilder>(m, "ValuationDescriptionBuilder", "Incrementally builds a ValuationClassDescription")
        .def(py::init([](storm::expressions::ExpressionManager& manager) { return ValuationDescriptionBuilder(manager.getSharedPointer()); }),
             py::arg("manager"), py::keep_alive<1, 2>())
        .def("add_boolean_variable", &ValuationDescriptionBuilder::addBooleanVariable, py::arg("variable"), py::arg("optional") = false,
             "Add a boolean variable")
        .def("add_integer_variable",
             py::overload_cast<storm::expressions::Variable const&, int64_t const, int64_t const, bool>(&ValuationDescriptionBuilder::addIntegerVariable),
             py::arg("variable"), py::arg("lower_bound"), py::arg("upper_bound"), py::arg("optional") = false,
             "Add an integer variable with explicit bounds (required to determine storage bit width)")
        .def("add_integer_variable",
             py::overload_cast<storm::expressions::Variable const&, ValuationDescriptionBuilder::Integer const, ValuationDescriptionBuilder::Integer const,
                               bool>(&ValuationDescriptionBuilder::addIntegerVariable),
             py::arg("variable"), py::arg("lower_bound"), py::arg("upper_bound"), py::arg("optional") = false,
             "Add an integer variable with explicit arbitrary-precision bounds, for values that may not fit in an int64")
        .def("add_double_variable", &ValuationDescriptionBuilder::addDoubleVariable, py::arg("variable"), py::arg("optional") = false, "Add a double variable")
        .def("add_rational_variable", &ValuationDescriptionBuilder::addRationalVariable, py::arg("variable"), py::arg("bit_size"), py::arg("optional") = false,
             "Add a rational variable")
        .def("add_string_variable", &ValuationDescriptionBuilder::addStringVariable, py::arg("variable"), py::arg("optional") = false, "Add a string variable")
        .def("build_class_description", &ValuationDescriptionBuilder::buildClassDescription, "Finalise and return the class description");

    py::classh<Valuations>(m, "Valuations", "Valuations for explicit entities (states/observations)")
        .def(py::init<ValuationClassDescription, std::shared_ptr<storm::expressions::ExpressionManager const> const&, uint64_t>(), py::arg("class_description"),
             py::arg("manager") = nullptr, py::arg("num_entities") = uint64_t(0),
             "Construct valuations from a class description, optional expression manager and entity count")
        .def("get_boolean_value", &Valuations::getBooleanValue, py::arg("entity"), py::arg("variable"))
        .def("get_boolean_values", &Valuations::getBooleanValues, py::arg("variable"), "Values of a Boolean variable as a BitVector")
        .def("get_int64_value", &Valuations::getInt64Value, py::arg("entity"), py::arg("variable"))
        .def("get_int64_values", &Valuations::getInt64Values, py::arg("variable"),
             "Get the integer variable value for all entities. The i-th entry is the value of entity i.")
        .def(
            "get_integer_bigint_value",
            [](Valuations const& v, uint64_t entity, storm::expressions::Variable const& var) {
                if (!var.hasIntegerType()) {
                    throw std::invalid_argument("Variable is not an integer variable");
                }
                return v.getStorage().readValue<storm::storage::sparse::ValuationsStorage::Integer>(entity, var);
            },
            py::arg("entity"), py::arg("variable"),
            "Get the value of an integer variable as an arbitrary-precision integer. Only needed for integer "
            "variables declared with arbitrary-precision bounds whose value does not fit in an int64; get_value "
            "already handles the common case.")
        .def("get_rational_value", &Valuations::getRationalValue, py::arg("entity"), py::arg("variable"))
        .def("get_rational_values", &Valuations::getRationalValues, py::arg("variable"),
             "Get the rational variable value for all entities. The i-th entry is the value of entity i.")
        .def(
            "get_double_value",
            [](Valuations const& v, uint64_t entity, storm::expressions::Variable const& var) {
                if (!var.hasRationalType()) {
                    throw std::invalid_argument("Variable is not a rational variable");
                }
                return v.getDoubleValue(entity, var);
            },
            py::arg("entity"), py::arg("variable"),
            "Get the value of a rational variable that was declared with the double (64-bit IEEE754) storage "
            "encoding via add_double_variable, as a Python float. get_value/get_rational_value assume the exact "
            "encoding and cannot read a double-encoded variable.")
        .def(
            "get_double_values",
            [](Valuations const& v, storm::expressions::Variable const& var) {
                if (!var.hasRationalType()) {
                    throw std::invalid_argument("Variable is not a rational variable");
                }
                return v.getDoubleValues(var);
            },
            py::arg("variable"), "Get the value for all entities of a rational variable declared via add_double_variable.")
        .def("get_string_value", &Valuations::getStringValue, py::arg("entity"), py::arg("variable"))
        .def("get_string_values", &Valuations::getStringValues, py::arg("variable"))
        .def("to_string", &Valuations::toString, py::arg("entity"), py::arg("pretty") = true,
             py::arg("selected_variables") = std::optional<std::set<storm::expressions::Variable>>{})
        .def(
            "to_json",
            [](Valuations const& v, uint64_t entity, std::optional<std::set<storm::expressions::Variable>> const& selectedVariables) {
                return v.toJson<storm::RationalNumber>(entity, selectedVariables);
            },
            py::arg("entity"), py::arg("selected_variables") = std::optional<std::set<storm::expressions::Variable>>{})
        .def("get_number_of_entities", &Valuations::getNumberOfEntities, "Get number of entities")
        .def("get_all_variables", &Valuations::getAllVariables, "Get all variables with valuations")
        .def("entity_has_variable", &Valuations::entityHasVariable, py::arg("entity"), py::arg("variable"))
        .def("select_entities", py::overload_cast<storm::storage::BitVector const&>(&Valuations::selectEntities, py::const_), py::arg("selected_entities"))
        .def("select_entities", py::overload_cast<std::vector<uint64_t> const&>(&Valuations::selectEntities, py::const_), py::arg("selected_entities"))
        .def(
            "write_bool_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, bool value) {
                if (entity >= v.getNumberOfEntities())
                    throw py::index_error();
                v.getStorage().writeValue<bool>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"), "Write a boolean value for the given entity and variable")
        .def(
            "write_int64_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, int64_t value) {
                if (entity >= v.getNumberOfEntities())
                    throw py::index_error();
                v.getStorage().writeValue<int64_t>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"), "Write an integer (int64) value for the given entity and variable")
        .def(
            "write_rational_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, storm::RationalNumber value) {
                if (entity >= v.getNumberOfEntities())
                    throw py::index_error();
                v.getStorage().writeValue<storm::RationalNumber>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"), "Write a rational value for the given entity and variable")
        .def(
            "write_double_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, double value) {
                if (!var.hasRationalType()) {
                    throw std::invalid_argument("Variable is not a rational variable");
                }
                if (entity >= v.getNumberOfEntities()) {
                    throw py::index_error();
                }
                v.getStorage().writeValue<double>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"),
            "Write the value of a rational variable that was declared with the double (64-bit IEEE754) storage "
            "encoding via add_double_variable")
        .def(
            "write_string_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, std::string const& value) {
                if (entity >= v.getNumberOfEntities())
                    throw py::index_error();
                v.getStorage().writeValue<std::string>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"), "Write a string value for the given entity and variable")
        .def(
            "write_integer_bigint_value",
            [](Valuations& v, uint64_t entity, storm::expressions::Variable const& var, storm::storage::sparse::ValuationsStorage::Integer const& value) {
                if (!var.hasIntegerType()) {
                    throw std::invalid_argument("Variable is not an integer variable");
                }
                if (entity >= v.getNumberOfEntities()) {
                    throw py::index_error();
                }
                v.getStorage().writeValue<storm::storage::sparse::ValuationsStorage::Integer>(entity, var, value);
            },
            py::arg("entity"), py::arg("variable"), py::arg("value"),
            "Write an arbitrary-precision integer value for the given entity and variable. Only needed for integer "
            "variables declared with arbitrary-precision bounds whose value does not fit in an int64.")
        .def_property_readonly("manager", &Valuations::getManager);
}

void define_valuation_transformer(py::module& m) {
    py::classh<storm::storage::sparse::ValuationTransformer>(
        m, "ValuationTransformer",
        "Transforms the given valuations to a new valuations over a new variable set. The values of the new variables are determined by evaluating "
        "the provided expressions w.r.t. the old variable valuation. The freshly introduced variables may either replace or extend the existing variable set.")
        .def(py::init<Valuations const&>(), py::arg("old_valuations"), py::keep_alive<1, 2>())
        .def("add_expression", &storm::storage::sparse::ValuationTransformer::addExpression, py::arg("expression_variable"), py::arg("defining_expression"))
        .def("build", &storm::storage::sparse::ValuationTransformer::build, py::arg("extend"));
}

void define_simplevaluation(py::module& m) {
    py::classh<storm::expressions::Valuation> val(m, "Valuation", "Base class for valuations of expression variables");
    val.def_property_readonly("expression_manager", &storm::expressions::Valuation::getManager);

    py::classh<storm::expressions::SimpleValuation>(m, "SimpleValuation", "Values of the variables in a symbolic program state", val)
        .def("to_json", &storm::expressions::SimpleValuation::toJson, "Convert to JSON")
        .def("to_string", &storm::expressions::SimpleValuation::toString, py::arg("pretty") = true, "to string")
        .def("get_boolean_value", &storm::expressions::SimpleValuation::getBooleanValue, py::arg("variable"), "Get Boolean value for expression variable")
        .def("get_integer_value", &storm::expressions::SimpleValuation::getIntegerValue, py::arg("variable"), "Get integer value for expression variable")
        .def("get_rational_value", &storm::expressions::SimpleValuation::getRationalValue, py::arg("variable"), "Get rational value for expression variable")
        .def("get_bit_vector_value", &storm::expressions::SimpleValuation::getBitVectorValue, py::arg("variable"),
             "Get bitvector value for expression variable");
}
