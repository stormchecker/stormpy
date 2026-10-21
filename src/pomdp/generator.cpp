#include "generator.h"

#include <cstdint>
#include <storm-pomdp/generator/GenerateMonitorVerifier.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/expressions/ExpressionManager.h>
#include <string>

#include "src/binding_type_index.h"

template<typename ValueType>
using SparseDtmc = storm::models::sparse::Dtmc<ValueType>;
template<typename ValueType>
using SparseMdp = storm::models::sparse::Mdp<ValueType>;
template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;

template<typename ValueType>
void define_verimon_generator(py::module& m) {
    auto index = stormpy::bindings::typeIndex<ValueType>();

    using MonitorVerifier = storm::generator::MonitorVerifier<ValueType>;
    stormpy::bindings::bindTemplateClass<MonitorVerifier>(m, "MonitorVerifier", index, "Container for monitor verifier POMDP with associated objects")
        .def(py::init<SparsePomdp<ValueType> const&, std::map<std::pair<uint32_t, bool>, uint32_t> const&, std::map<uint32_t, std::string> const&>(),
             "product"_a, "observation_map"_a, "observation_default_action"_a)
        .def("get_product", &MonitorVerifier::getProduct, "Product POMDP", py::return_value_policy::reference_internal)
        .def_property_readonly("observation_map", &MonitorVerifier::getObservationMap, "Mapping from (monitor state, accepting) to observations of the product",
                               py::return_value_policy::reference_internal)
        .def_property_readonly("observation_default_action", &MonitorVerifier::getObservationDefaultAction, "Default action label for each observation",
                               py::return_value_policy::reference_internal);

    using Generator = storm::generator::GenerateMonitorVerifier<ValueType>;
    stormpy::bindings::bindTemplateClass<typename Generator::Options>(m, "GenerateMonitorVerifierOptions", index,
                                                                      "Options for generating the monitor verifier POMDP")
        .def(py::init<>())
        .def_readwrite("accepting_label", &Generator::Options::acceptingLabel, "Label of accepting monitor states")
        .def_readwrite("step_prefix", &Generator::Options::stepPrefix, "Prefix of the labels of monitor steps")
        .def_readwrite("horizon_label", &Generator::Options::horizonLabel, "Label of monitor states reaching the horizon")
        .def_readwrite("use_restart_semantics", &Generator::Options::useRestartSemantics, "Use restart semantics instead of a sink state");

    stormpy::bindings::bindTemplateClass<Generator>(m, "GenerateMonitorVerifier", index, "Generator of POMDP used in verifying monitors against Markov chains")
        .def(py::init<SparseDtmc<ValueType> const&, SparseMdp<ValueType> const&, std::shared_ptr<storm::expressions::ExpressionManager>&,
                      typename Generator::Options const&>(),
             "mc"_a, "monitor"_a, "expr_manager"_a, "options"_a, py::keep_alive<1, 2>(), py::keep_alive<1, 3>())
        .def("create_product", &Generator::createProduct, "Create the verification POMDP")
        .def("set_risk", &Generator::setRisk, "Set the risk of each state of the Markov chain", "risk"_a);
}

template void define_verimon_generator<double>(py::module& m);
template void define_verimon_generator<storm::RationalNumber>(py::module& m);
