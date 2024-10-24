#include "generator.h"
#include "storm-pomdp/generator/GenerateMonitorVerifier.h"

template<typename ValueType> using GenerateMonitorVerifier = storm::generator::GenerateMonitorVerifier<ValueType>;
template<typename ValueType> using SparseDtmc = storm::models::sparse::Dtmc<ValueType>;
template<typename ValueType> using SparseMdp = storm::models::sparse::Mdp<ValueType>;
template<typename ValueType> using GenerateMonitorVerifierOptions = typename storm::generator::GenerateMonitorVerifier<ValueType>::Options;

template<typename ValueType>
void define_verimon_generator(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::generator::GenerateMonitorVerifier<ValueType>> gmv(m, ("GenerateMonitorVerifier" + vtSuffix).c_str(), "Generator of POMDP used in verifying monitors against markov chains");
    gmv.def(py::init<SparseDtmc<ValueType> const&, SparseMdp<ValueType> const&, GenerateMonitorVerifierOptions<ValueType> const&>(), py::arg("mc"), py::arg("monitor"), py::arg("options"));
    gmv.def("create_product", &storm::generator::GenerateMonitorVerifier<ValueType>::createProduct, "Created the verification POMDP");

    py::class_<GenerateMonitorVerifierOptions<ValueType>> gmvopts(m, ("GenerateMonitorVerifier" + vtSuffix + "Options").c_str(), "Options for corresponding generator");
    gmvopts.def(py::init<>());
    gmvopts.def_readwrite("good_label", &GenerateMonitorVerifierOptions<ValueType>::goodLabel);
    gmvopts.def_readwrite("accepting_label", &GenerateMonitorVerifierOptions<ValueType>::acceptingLabel);
    gmvopts.def_readwrite("step_prefix", &GenerateMonitorVerifierOptions<ValueType>::stepPrefix);
    gmvopts.def_readwrite("horizon_label", &GenerateMonitorVerifierOptions<ValueType>::horizonLabel);
}

template void define_verimon_generator<double>(py::module& m, std::string const& vtSuffix);
