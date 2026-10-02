#include "environment.h"

#include <storm-dft/environment/AllDftEnvironments.h>
#include <storm-dft/environment/DftEnvironment.h>

void define_dft_environment(py::module& m) {
    py::classh<storm::dft::DftEnvironment>(m, "DftEnvironment", "Environment for DFT")
        .def(py::init<>(), "Construct default DFT environment")
        .def_property_readonly(
            "core_environment", [](storm::dft::DftEnvironment& env) -> auto& { return env.core(); }, "Core Storm environment")
        .def_property_readonly(
            "analysis_environment", [](storm::dft::DftEnvironment& env) -> auto& { return env.analysis(); }, "Analysis environment")
        .def_property_readonly(
            "model_builder_environment", [](storm::dft::DftEnvironment& env) -> auto& { return env.modelBuilder(); }, "Model building environment")
        .def_property_readonly(
            "transformation_environment", [](storm::dft::DftEnvironment& env) -> auto& { return env.transformation(); }, "Transformation environment");

    py::classh<storm::dft::AnalysisEnvironment>(m, "AnalysisEnvironment", "Environment configuring the DFT analysis")
        .def_property("use_modularisation", &storm::dft::AnalysisEnvironment::isUseModularisation, &storm::dft::AnalysisEnvironment::setUseModularisation,
                      "Whether modularisation is used")
        .def_property("solve_with_smt", &storm::dft::AnalysisEnvironment::isSolveWithSMT, &storm::dft::AnalysisEnvironment::setSolveWithSMT,
                      "Whether SMT solving is used")
        .def_property("chunksize", &storm::dft::AnalysisEnvironment::getChunksize, &storm::dft::AnalysisEnvironment::setChunksize,
                      "Size of the chunks of values for DD analysis")
        .def_property("mttf_precision", &storm::dft::AnalysisEnvironment::getMttfPrecision, &storm::dft::AnalysisEnvironment::setMttfPrecision,
                      "Precision used for the MTTF computation via DD")
        .def_property("mttf_stepsize", &storm::dft::AnalysisEnvironment::getMttfStepsize, &storm::dft::AnalysisEnvironment::setMttfStepsize,
                      "Step size used for the MTTF computation via DD")
        .def_property("mttf_algorithm", &storm::dft::AnalysisEnvironment::getMttfAlgorithm, &storm::dft::AnalysisEnvironment::setMttfAlgorithm,
                      "Algorithm used for the MTTF computation via DD")
        .def_property(
            "approximation_error",
            [](storm::dft::AnalysisEnvironment const& env) -> py::object {
                if (env.isApproximationErrorSet())
                    return py::cast(env.getApproximationError());
                return py::none();
            },
            [](storm::dft::AnalysisEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetApproximationError();
                else
                    env.setApproximationError(obj.cast<double>());
            },
            "Allowed approximation error. Value None sets exact analysis.")
        .def_property("approximation_heuristic", &storm::dft::AnalysisEnvironment::getApproximationHeuristic,
                      &storm::dft::AnalysisEnvironment::setApproximationHeuristic, "Heuristic used for selecting states to explore next");

    py::classh<storm::dft::ModelBuilderEnvironment>(m, "ModelBuilderEnvironment", "Environment configuring the Markov model building from a DFT")
        .def_property("use_symmetry_reduction", &storm::dft::ModelBuilderEnvironment::isUseSymmetryReduction,
                      &storm::dft::ModelBuilderEnvironment::setUseSymmetryReduction, "Whether symmetry reduction is used")
        .def_property("allow_dc_for_relevant_events", &storm::dft::ModelBuilderEnvironment::isAllowDCForRelevantEvents,
                      &storm::dft::ModelBuilderEnvironment::setAllowDCForRelevantEvents, "Whether Don't Care propagation is allowed for relevant events")
        .def_property("add_labels_claiming", &storm::dft::ModelBuilderEnvironment::isAddLabelsClaiming,
                      &storm::dft::ModelBuilderEnvironment::setAddLabelsClaiming, "Whether labels representing claiming operations are added to the model")
        .def_property(
            "max_depth",
            [](storm::dft::ModelBuilderEnvironment const& env) -> py::object {
                if (env.isMaxDepthSet())
                    return py::cast(env.getMaxDepth());
                return py::none();
            },
            [](storm::dft::ModelBuilderEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetMaxDepth();
                else
                    env.setMaxDepth(obj.cast<uint_fast64_t>());
            },
            "Maximal depth up to which the model is explored. Value None sets unbounded exploration.")
        .def_property("take_first_dependency", &storm::dft::ModelBuilderEnvironment::isTakeFirstDependency,
                      &storm::dft::ModelBuilderEnvironment::setTakeFirstDependency, "Whether to always select the first dependency to resolve non-determinism")
        .def_property("unique_failed_be", &storm::dft::ModelBuilderEnvironment::isUniqueFailedBE, &storm::dft::ModelBuilderEnvironment::setUniqueFailedBE,
                      "Whether one unique state is used for all failed states");

    py::classh<storm::dft::TransformationEnvironment>(m, "TransformationEnvironment", "Environment configuring transformation of the built model")
        .def_property("use_bisimulation", &storm::dft::TransformationEnvironment::isUseBisimulation, &storm::dft::TransformationEnvironment::setUseBisimulation,
                      "Whether bisimulation is applied on the built model")
        .def_property("eliminate_chains", &storm::dft::TransformationEnvironment::isEliminateChains, &storm::dft::TransformationEnvironment::setEliminateChains,
                      "Whether non-Markovian chains are eliminated from the built model")
        .def_property("label_behavior", &storm::dft::TransformationEnvironment::getLabelBehavior, &storm::dft::TransformationEnvironment::setLabelBehavior,
                      "Behavior for labels when eliminating non-Markovian chains");
}
