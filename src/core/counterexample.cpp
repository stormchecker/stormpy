
#include "counterexample.h"
#include "storm-counterexamples/api/counterexamples.h"
#include "storm/environment/Environment.h"

using namespace storm::counterexamples;

// Define python bindings
void define_counterexamples(py::module& m) {
    using FlatSet = boost::container::flat_set<uint64_t, std::less<uint64_t>, boost::container::new_allocator<uint64_t>>;

    py::class_<FlatSet>(m, "FlatSet", "Container to pass to program")
        .def(py::init<>())
        .def(py::init<FlatSet>(), "other"_a)
        .def("insert", [](FlatSet& flatset, uint64_t value) { flatset.insert(value); })
        .def("is_subset_of", [](FlatSet const& left, FlatSet const& right) { return std::includes(right.begin(), right.end(), left.begin(), left.end()); })
        .def("insert_set",
             [](FlatSet& left, FlatSet const& additional) {
                 for (auto const& i : additional) {
                     left.insert(i);
                 }
             })
        .def("__str__",
             [](FlatSet const& set) {
                 std::stringstream str;
                 str << "[";
                 for (auto const& i : set) {
                     str << i << ", ";
                 }
                 str << "]";
                 return str.str();
             })
        .def("__len__", [](FlatSet const& set) { return set.size(); })
        .def(
            "__iter__", [](FlatSet& v) { return py::make_iterator(v.begin(), v.end()); }, py::keep_alive<0, 1>()) /* Keep vector alive while iterator is used */
        ;

    using CexGeneratorStats = SMTMinimalLabelSetGenerator<double>::GeneratorStats;

    py::class_<CexGeneratorStats>(m, "SMTCounterExampleGeneratorStats", "Stats for highlevel counterexample generation")
        .def(py::init<>())
        .def_readonly("analysis_time", &CexGeneratorStats::analysisTime)
        .def_readonly("setup_time", &CexGeneratorStats::setupTime)
        .def_readonly("model_checking_time", &CexGeneratorStats::modelCheckingTime)
        .def_readonly("solver_time", &CexGeneratorStats::solverTime)
        .def_readonly("cut_time", &CexGeneratorStats::cutTime)
        .def_readonly("iterations", &CexGeneratorStats::iterations);

    using CexGeneratorOptions = SMTMinimalLabelSetGenerator<double>::Options;
    py::class_<CexGeneratorOptions>(m, "SMTCounterExampleGeneratorOptions", "Options for highlevel counterexample generation")
        .def(py::init<>())
        .def_readwrite("check_threshold_feasible", &CexGeneratorOptions::checkThresholdFeasible)
        .def_readwrite("encode_reachability", &CexGeneratorOptions::encodeReachability)
        .def_readwrite("silent", &CexGeneratorOptions::silent)
        .def_readwrite("add_backward_implication_cuts", &CexGeneratorOptions::addBackwardImplicationCuts)
        .def_readwrite("use_dynamic_constraints", &CexGeneratorOptions::useDynamicConstraints)
        .def_readwrite("maximum_counterexamples", &CexGeneratorOptions::maximumCounterexamples)
        .def_readwrite("continue_after_first_counterexample", &CexGeneratorOptions::continueAfterFirstCounterexampleUntil)
        .def_readwrite("maximum_iterations_after_counterexample", &CexGeneratorOptions::maximumExtraIterations);
    py::class_<SMTMinimalLabelSetGenerator<double>>(m, "SMTCounterExampleGenerator", "Highlevel Counterexample Generator with SMT as backend")
        .def_static("precompute", &SMTMinimalLabelSetGenerator<double>::precompute, "Precompute input for counterexample generation", py::arg("env"),
                    py::arg("symbolic_model"), py::arg("model"), py::arg("formula"))
        .def_static("build", &SMTMinimalLabelSetGenerator<double>::computeCounterexampleLabelSet, "Compute counterexample", py::arg("env"), py::arg("stats"),
                    py::arg("symbolic_model"), py::arg("model"), py::arg("cex_input"), py::arg("dontcare"), py::arg("options"))

        ;

    using CexInput = SMTMinimalLabelSetGenerator<double>::CexInput;
    py::class_<CexInput>(m, "SMTCounterExampleInput", "Precomputed input for counterexample generation")
        .def("add_reward_and_threshold", &CexInput::addRewardThresholdCombination, "add another reward structure and threshold", py::arg("reward_name"),
             py::arg("threshold"));
}
