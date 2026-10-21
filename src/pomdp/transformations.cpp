#include "transformations.h"

#include <storm-pomdp/transformer/ApplyFiniteSchedulerToPomdp.h>
#include <storm-pomdp/transformer/BinaryPomdpTransformer.h>
#include <storm-pomdp/transformer/ObservationTraceUnfolder.h>
#include <storm-pomdp/transformer/PomdpMemoryUnfolder.h>
#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/expressions/ExpressionManager.h>
#include <storm/transformer/MakePOMDPCanonic.h>

#include "src/binding_type_index.h"

template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;

void define_transformations_nt(py::module& m) {
    py::native_enum<storm::transformer::PomdpFscApplicationMode>(m, "PomdpFscApplicationMode", "enum.Enum", "Mode for applying an unknown FSC to a POMDP")
        .value("STANDARD", storm::transformer::PomdpFscApplicationMode::STANDARD)
        .value("SIMPLE_LINEAR", storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR)
        .value("SIMPLE_LINEAR_INVERSE", storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR_INVERSE)
        .value("SIMPLE_LOG", storm::transformer::PomdpFscApplicationMode::SIMPLE_LOG)
        .value("FULL", storm::transformer::PomdpFscApplicationMode::FULL)
        .finalize();

    py::classh<storm::pomdp::ObservationTraceUnfolderOptions> options(m, "ObservationTraceUnfolderOptions", "Options for unfolding observation traces");
    options.def(py::init<>());
    options.def_readwrite("use_restart_semantics", &storm::pomdp::ObservationTraceUnfolderOptions::useRestartSemantics,
                          "Use restart semantics instead of a sink state");
}

template<typename ValueType>
void define_transformations(py::module& m) {
    auto index = stormpy::bindings::typeIndex<ValueType>();

    using MakeCanonic = storm::transformer::MakePOMDPCanonic<ValueType>;
    stormpy::bindings::bindTemplateClass<MakeCanonic>(m, "MakePOMDPCanonic", index, "Transformer making the representation of a POMDP canonic")
        .def(py::init<SparsePomdp<ValueType> const&>(), "pomdp"_a, py::keep_alive<1, 2>())
        .def("transform", &MakeCanonic::transform, "Return the canonic POMDP");

    using MemoryUnfolder = storm::transformer::PomdpMemoryUnfolder<ValueType>;
    stormpy::bindings::bindTemplateClass<MemoryUnfolder>(m, "PomdpMemoryUnfolder", index, "Transformer unfolding a memory structure into a POMDP")
        .def(py::init<SparsePomdp<ValueType> const&, storm::storage::PomdpMemory const&, bool, bool>(), "pomdp"_a, "memory"_a, "add_memory_labels"_a = false,
             "keep_state_valuations"_a = false, py::keep_alive<1, 2>(), py::keep_alive<1, 3>())
        .def("transform", &MemoryUnfolder::transform, "Return the product of the POMDP and the memory", "drop_unreachable_states"_a = true);

    using TransformationResult = storm::transformer::PomdpTransformationResult<ValueType>;
    stormpy::bindings::bindTemplateClass<TransformationResult>(m, "PomdpTransformationResult", index, "Result of a POMDP transformation")
        .def_readonly("transformed_pomdp", &TransformationResult::transformedPomdp, "Transformed POMDP")
        .def_readonly("transformed_state_to_original_state_map", &TransformationResult::transformedStateToOriginalStateMap,
                      "Mapping from states of the transformed POMDP to states of the original POMDP");

    using BinaryTransformer = storm::transformer::BinaryPomdpTransformer<ValueType>;
    stormpy::bindings::bindTemplateClass<BinaryTransformer>(m, "BinaryPomdpTransformer", index,
                                                            "Transformer making a POMDP binary, i.e., each state has at most two actions")
        .def(py::init<>())
        .def("transform", &BinaryTransformer::transform, "Transform the POMDP", "pomdp"_a, "transform_simple"_a, "keep_state_valuations"_a = false);

    using FscApplication = storm::transformer::ApplyFiniteSchedulerToPomdp<ValueType>;
    stormpy::bindings::bindTemplateClass<FscApplication>(m, "ApplyFiniteSchedulerToPomdp", index,
                                                         "Transformer applying an unknown finite-state controller to a POMDP")
        .def(py::init<SparsePomdp<ValueType> const&>(), "pomdp"_a, py::keep_alive<1, 2>())
        .def("transform", &FscApplication::transform, "Return the parametric Markov chain induced by the unknown FSC",
             "application_mode"_a = storm::transformer::PomdpFscApplicationMode::SIMPLE_LINEAR);
}

template<typename ValueType>
void define_observation_trace_unfolder(py::module& m) {
    using Unfolder = storm::pomdp::ObservationTraceUnfolder<ValueType>;
    stormpy::bindings::bindTemplateClass<Unfolder>(m, "ObservationTraceUnfolder", stormpy::bindings::typeIndex<ValueType>(),
                                                   "Unfolds observation traces in models")
        .def(py::init<SparsePomdp<ValueType> const&, std::vector<ValueType> const&, std::shared_ptr<storm::expressions::ExpressionManager>,
                      storm::pomdp::ObservationTraceUnfolderOptions const&>(),
             "model"_a, "risk"_a, "expr_manager"_a, "options"_a)
        .def("is_restart_semantics_set", &Unfolder::isRestartSemanticsSet, "Whether restart semantics are used")
        .def("transform", &Unfolder::transform, "Unfold the given observation trace", "observations"_a)
        .def("reset", &Unfolder::reset, "Restart the unfolding with the given observation", "observation"_a)
        .def("extend", &Unfolder::extend, "Extend the unfolding by the given observations", "observations"_a);
}

template void define_transformations<double>(py::module& m);
template void define_transformations<storm::RationalNumber>(py::module& m);
template void define_transformations<storm::RationalFunction>(py::module& m);

template void define_observation_trace_unfolder<double>(py::module& m);
template void define_observation_trace_unfolder<storm::RationalNumber>(py::module& m);
template void define_observation_trace_unfolder<storm::RationalFunction>(py::module& m);
template void define_observation_trace_unfolder<storm::Interval>(py::module& m);
template void define_observation_trace_unfolder<storm::RationalInterval>(py::module& m);
