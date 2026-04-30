#include "generator.h"
#include <cstdint>
#include <string>
#include "storm-pomdp/generator/GenerateMonitorVerifier.h"
#include "storm/adapters/RationalNumberAdapter.h"
#include "storm/storage/expressions/ExpressionManager.h"

template<typename ValueType>
using GenerateMonitorVerifier = storm::generator::GenerateMonitorVerifier<ValueType>;
template<typename ValueType>
using SparseDtmc = storm::models::sparse::Dtmc<ValueType>;
template<typename ValueType>
using SparseMdp = storm::models::sparse::Mdp<ValueType>;
template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;
template<typename ValueType>
using GenerateMonitorVerifierOptions = typename storm::generator::GenerateMonitorVerifier<ValueType>::Options;

template<typename ValueType>
void define_verimon_generator(py::module &m, std::string const &vtSuffix) {
    py::class_<storm::generator::MonitorVerifier<ValueType>, std::shared_ptr<storm::generator::MonitorVerifier<ValueType>>> mv(
        m, ("MonitorVerifier" + vtSuffix).c_str(), "Container for monitor verifier POMDP with associated objects");
    mv.def(py::init<const SparsePomdp<ValueType> &, const std::map<std::pair<uint32_t, bool>, uint32_t> &, const std::map<uint32_t, std::string> &>(),
           py::arg("product"), py::arg("observation_map"), py::arg("default_action_map"));
    mv.def("get_product", &storm::generator::MonitorVerifier<ValueType>::getProduct, py::return_value_policy::reference_internal);
    mv.def_property_readonly("observation_map", &storm::generator::MonitorVerifier<ValueType>::getObservationMap, py::return_value_policy::reference_internal);
    mv.def_property_readonly("default_action_map", &storm::generator::MonitorVerifier<ValueType>::getObservationDefaultAction, py::return_value_policy::reference_internal);

    py::class_<storm::generator::GenerateMonitorVerifier<ValueType>> gmv(m, ("GenerateMonitorVerifier" + vtSuffix).c_str(),
                                                                         "Generator of POMDP used in verifying monitors against markov chains");
    gmv.def(py::init<SparseDtmc<ValueType> const &, SparseMdp<ValueType> const &, std::shared_ptr<storm::expressions::ExpressionManager> &,
                     GenerateMonitorVerifierOptions<ValueType> const &>(),
            py::arg("mc"), py::arg("monitor"), py::arg("expr_manager"), py::arg("options"));
    gmv.def("create_product", &storm::generator::GenerateMonitorVerifier<ValueType>::createProduct, "Create the verification POMDP");
    gmv.def("set_risk", &storm::generator::GenerateMonitorVerifier<ValueType>::setRisk, py::arg("risk"));

    py::class_<GenerateMonitorVerifierOptions<ValueType>> gmvopts(m, ("GenerateMonitorVerifier" + vtSuffix + "Options").c_str(),
                                                                  "Options for corresponding generator");
    gmvopts.def(py::init<>());
    gmvopts.def_readwrite("accepting_label", &GenerateMonitorVerifierOptions<ValueType>::acceptingLabel);
    gmvopts.def_readwrite("step_prefix", &GenerateMonitorVerifierOptions<ValueType>::stepPrefix);
    gmvopts.def_readwrite("horizon_label", &GenerateMonitorVerifierOptions<ValueType>::horizonLabel);
    gmvopts.def_readwrite("use_restart_semantics", &GenerateMonitorVerifierOptions<ValueType>::useRestartSemantics);
}

template void define_verimon_generator<double>(py::module &m, std::string const &vtSuffix);
template void define_verimon_generator<storm::RationalNumber>(py::module &m, std::string const &vtSuffix);
