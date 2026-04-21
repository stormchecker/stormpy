#include "transformations.h"

#include "storm-pomdp/transformer/ApplyFiniteSchedulerToPomdp.h"
#include "storm-pomdp/transformer/BinaryPomdpTransformer.h"
#include "storm-pomdp/transformer/ObservationTraceUnfolder.h"
#include "storm-pomdp/transformer/PomdpMemoryUnfolder.h"
#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/storage/expressions/ExpressionManager.h"
#include "storm/transformer/MakePOMDPCanonic.h"

template<typename ValueType>
std::shared_ptr<storm::models::sparse::Pomdp<ValueType>> make_canonic(storm::models::sparse::Pomdp<ValueType> const &pomdp) {
    storm::transformer::MakePOMDPCanonic<ValueType> makeCanonic(pomdp);
    return makeCanonic.transform();
}

template<typename ValueType>
std::shared_ptr<storm::models::sparse::Pomdp<ValueType>> unfold_memory(storm::models::sparse::Pomdp<ValueType> const &pomdp,
                                                                       storm::storage::PomdpMemory const &memory, bool addMemoryLabels,
                                                                       bool keepStateValuations) {
    storm::transformer::PomdpMemoryUnfolder<ValueType> unfolder(pomdp, memory, addMemoryLabels, keepStateValuations);
    return unfolder.transform();
}

template<typename ValueType>
std::shared_ptr<storm::models::sparse::Pomdp<ValueType>> make_simple(storm::models::sparse::Pomdp<ValueType> const &pomdp, bool keepStateValuations) {
    storm::transformer::BinaryPomdpTransformer<ValueType> transformer;
    return transformer.transform(pomdp, true, keepStateValuations).transformedPomdp;
}

template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<storm::RationalFunction>> apply_unknown_fsc(storm::models::sparse::Pomdp<ValueType> const &pomdp,
                                                                                         storm::transformer::PomdpFscApplicationMode const &applicationMode) {
    storm::transformer::ApplyFiniteSchedulerToPomdp<ValueType> transformer(pomdp);
    return transformer.transform(applicationMode);
}

template<typename ValueType>
std::shared_ptr<storm::models::sparse::Mdp<ValueType>> unfold_trace(storm::models::sparse::Pomdp<ValueType> const &pomdp,
                                                                    std::shared_ptr<storm::expressions::ExpressionManager> &exprManager,
                                                                    std::vector<uint32_t> const &observationTrace, std::vector<ValueType> const &riskDef,
                                                                    bool restartSemantics = true) {
    storm::pomdp::ObservationTraceUnfolderOptions options = storm::pomdp::ObservationTraceUnfolderOptions();
    options.useRestartSemantics = restartSemantics;
    storm::pomdp::ObservationTraceUnfolder<ValueType> transformer(pomdp, riskDef, exprManager, options);
    return transformer.transform(observationTrace);
}

// STANDARD, SIMPLE_LINEAR, SIMPLE_LINEAR_INVERSE, SIMPLE_LOG, FULL
void define_transformations_nt(py::module &m) {
    py::enum_<storm::transformer::PomdpFscApplicationMode>(m, "PomdpFscApplicationMode")
            .value("standard", storm::transformer::PomdpFscApplicationMode::STANDARD)
            .value("simple_linear", storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR)
            .value("simple_linear_inverse", storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR_INVERSE)
            .value("simple_log", storm::transformer::PomdpFscApplicationMode::SIMPLE_LOG)
            .value("full", storm::transformer::PomdpFscApplicationMode::FULL)
            ;
    py::class_<storm::pomdp::ObservationTraceUnfolderOptions> options(m, "ObservationTraceUnfolderOptions", "Options for unfolding observation traces");
    options.def(py::init<>());
    options.def_readwrite("restart_semantics", &storm::pomdp::ObservationTraceUnfolderOptions::useRestartSemantics,
                          "Use restart semantics instead of a sink state");
}

template<typename ValueType>
void define_transformations(py::module &m, std::string const &vtSuffix) {
    m.def(("_make_canonic_" + vtSuffix).c_str(), &make_canonic<ValueType>, "Return a canonicly-ordered POMDP", py::arg("pomdp"));
    m.def(("_unfold_memory_" + vtSuffix).c_str(), &unfold_memory<ValueType>, "Unfold memory into a POMDP", py::arg("pomdp"), py::arg("memorystructure"), py::arg("memorylabels") = false, py::arg("keep_state_valuations")=false);
    m.def(("_make_simple_"+ vtSuffix).c_str(), &make_simple<ValueType>, "Make POMDP simple", py::arg("pomdp"), py::arg("keep_state_valuations")=false);
    m.def(("_apply_unknown_fsc_" + vtSuffix).c_str(), &apply_unknown_fsc<ValueType>, "Apply unknown FSC",py::arg("pomdp"), py::arg("application_mode")=storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR);
}

template<typename ValueType>
void define_transformations_int(py::module &m, std::string const &vtSuffix) {
    py::class_<storm::pomdp::ObservationTraceUnfolder<ValueType>> unfolder(m, ("ObservationTraceUnfolder" + vtSuffix).c_str(),
                                                                           "Unfolds observation traces in models");
    unfolder.def(py::init<storm::models::sparse::Pomdp<ValueType>, std::vector<ValueType> const &, std::shared_ptr<storm::expressions::ExpressionManager> &,
                          storm::pomdp::ObservationTraceUnfolderOptions const &>(),
                 py::arg("model"), py::arg("risk"), py::arg("expression_manager"), py::arg("options"), py::keep_alive<2, 1>());
    unfolder.def("is_restart_semantics_set", &storm::pomdp::ObservationTraceUnfolder<ValueType>::isRestartSemanticsSet);
    unfolder.def("transform", &storm::pomdp::ObservationTraceUnfolder<ValueType>::transform, py::arg("trace"));
    unfolder.def("reset", &storm::pomdp::ObservationTraceUnfolder<ValueType>::reset, py::arg("new_observation"));
    unfolder.def("extend", &storm::pomdp::ObservationTraceUnfolder<ValueType>::extend, py::arg("new_observation"));
}

template void define_transformations<double>(py::module &m, std::string const &vtSuffix);
template void define_transformations<storm::RationalNumber>(py::module &m, std::string const &vtSuffix);
template void define_transformations<storm::RationalFunction>(py::module &m, std::string const &vtSuffix);

template void define_transformations_int<double>(py::module &m, std::string const &vtSuffix);
template void define_transformations_int<storm::RationalNumber>(py::module &m, std::string const &vtSuffix);
template void define_transformations_int<storm::RationalFunction>(py::module &m, std::string const &vtSuffix);
template void define_transformations_int<storm::Interval>(py::module &m, std::string const &vtSuffix);
template void define_transformations_int<storm::RationalInterval>(py::module &m, std::string const &vtSuffix);
