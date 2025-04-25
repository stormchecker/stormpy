#include "valuation.h"
#include "src/helpers.h"

#include "storm/adapters/RationalNumberAdapter.h"
#include "storm/adapters/JsonAdapter.h"
#include "storm/storage/expressions/ExpressionManager.h"
#include "storm/storage/expressions/SimpleValuation.h"
#include "storm/storage/expressions/Variable.h"
#include "storm/storage/sparse/StateValuations.h"

// Thin wrappers
storm::json<storm::RationalNumber> toJson(storm::storage::sparse::StateValuations const& valuations, storm::storage::sparse::state_type const& stateIndex, boost::optional<std::set<storm::expressions::Variable>> const& selectedVariables) {
    return valuations.toJson(stateIndex, selectedVariables);
}

void add_state(storm::storage::sparse::StateValuationsBuilder& builder, storm::storage::sparse::state_type const& state, std::vector<bool>&& booleanValues, std::vector<int64_t>&& integerValues, std::vector<storm::RationalNumber>&& rationalValues) {
    return builder.addState(state, std::move(booleanValues), std::move(integerValues), std::move(rationalValues));
}


// Define python bindings
void define_statevaluation(py::module& m) {

    py::class_<storm::storage::sparse::StateValuations, std::shared_ptr<storm::storage::sparse::StateValuations>>(m,"StateValuation", "Valuations for explicit states")
        .def("get_boolean_value", &storm::storage::sparse::StateValuations::getBooleanValue, py::arg("state"), py::arg("variable"))
        .def("get_integer_value", &storm::storage::sparse::StateValuations::getIntegerValue, py::arg("state"), py::arg("variable"))
        .def("get_rational_value", &storm::storage::sparse::StateValuations::getRationalValue, py::arg("state"), py::arg("variable"))
        .def("get_boolean_values_states", &storm::storage::sparse::StateValuations::getBooleanValues, py::arg("variable"), "Get the value of the Boolean variable of all states. The i'th entry represents the value of state i.")
        .def("get_integer_values_states", &storm::storage::sparse::StateValuations::getIntegerValues, py::arg("variable"), "Get the value of the integer variable of all states. The i'th entry represents the value of state i.")
        .def("get_rational_values_states", &storm::storage::sparse::StateValuations::getRationalValues, py::arg("variable"), "Get the value of the rational variable of all states. The i'th entry represents the value of state i.")
        .def("get_string", &storm::storage::sparse::StateValuations::toString, py::arg("state"), py::arg("pretty")=true, py::arg("selected_variables")=boost::none)
        .def("get_json", &toJson, py::arg("state"), py::arg("selected_variables")=boost::none)
        .def("get_nr_of_states", &storm::storage::sparse::StateValuations::getNumberOfStates);
    ;


    py::class_<storm::storage::sparse::StateValuationsBuilder, std::shared_ptr<storm::storage::sparse::StateValuationsBuilder>>(m,"StateValuationsBuilder")
            .def(py::init<>())
            .def("add_variable", &storm::storage::sparse::StateValuationsBuilder::addVariable, py::arg("variable"), "Adds a new variable")
            .def("add_state", &add_state, py::arg("state"), py::arg("boolean_values") = std::vector<bool>(), py::arg("integer_values") = std::vector<int64_t>(), py::arg("rational_values") = std::vector<storm::RationalNumber>(), "Adds a new state, no more variables should be added afterwards")
            .def("build", &storm::storage::sparse::StateValuationsBuilder::build, "Creates the finalized state valuations object")
            ;

}

void define_simplevaluation(py::module& m) {
    py::class_<storm::expressions::Valuation> val(m, "Valuation");
    val.def_property_readonly("expression_manager", &storm::expressions::Valuation::getManager);
    py::class_<storm::expressions::SimpleValuation> sval(m, "SimpleValuation", val);
    sval.def("to_json", &storm::expressions::SimpleValuation::toJson, "Convert to JSON");
    sval.def("to_string", &storm::expressions::SimpleValuation::toString, py::arg("pretty")=true, "to string");
    sval.def("get_boolean_value", &storm::expressions::SimpleValuation::getBooleanValue, py::arg("variable"), "Get Boolean Value for expression variable");
    sval.def("get_integer_value", &storm::expressions::SimpleValuation::getIntegerValue, py::arg("variable"), "Get Integer Value for expression variable");

}