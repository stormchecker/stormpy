#include "builder.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/builder/BuilderOptions.h>
#include <storm/builder/ExplicitModelBuilder.h>
#include <storm/builder/ExplorationOrder.h>
#include <storm/languages/SymbolicModelDescription.h>
#include <storm/logic/Formula.h>

#include "src/binding_type_index.h"

namespace stormpy {

using BuilderOptions = storm::builder::BuilderOptions;

void define_builder(py::module& m) {
    py::native_enum<storm::builder::ExplorationOrder>(m, "ExplorationOrder", "enum.Enum", "Order in which states are explored")
        .value("DFS", storm::builder::ExplorationOrder::Dfs)
        .value("BFS", storm::builder::ExplorationOrder::Bfs)
        .finalize();

    py::classh<BuilderOptions>(m, "BuilderOptions", "Options for building process")
        .def(py::init<std::vector<std::shared_ptr<storm::logic::Formula const>> const&, storm::languages::SymbolicModelDescription const&>(),
             "Create options preserving the given formulas", py::arg("formulas"), py::arg("model_description") = storm::languages::SymbolicModelDescription())
        .def(py::init<bool, bool>(), "Create options without formulas", py::arg("build_all_reward_models") = false, py::arg("build_all_labels") = false)
        .def("get_label_names", &BuilderOptions::getLabelNames, "Get the names of the labels to build")
        .def("is_build_all_reward_models_set", &BuilderOptions::isBuildAllRewardModelsSet, "Whether all reward models are built")
        .def("is_build_all_labels_set", &BuilderOptions::isBuildAllLabelsSet, "Whether all labels are built")
        .def("is_build_choice_labels_set", &BuilderOptions::isBuildChoiceLabelsSet, "Whether choice labels are built")
        .def("is_build_state_valuations_set", &BuilderOptions::isBuildStateValuationsSet, "Whether state valuations are built")
        .def("is_build_observation_valuations_set", &BuilderOptions::isBuildObservationValuationsSet, "Whether observation valuations are built")
        .def("is_build_choice_origins_set", &BuilderOptions::isBuildChoiceOriginsSet, "Whether choice origins are built")
        .def("set_build_all_reward_models", &BuilderOptions::setBuildAllRewardModels, "Build all reward models", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_build_all_labels", &BuilderOptions::setBuildAllLabels, "Build all state labels", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_apply_maximal_progress_assumption", &BuilderOptions::setApplyMaximalProgressAssumption, "Apply the maximal progress assumption",
             py::arg("new_value") = true, py::return_value_policy::reference_internal)
        .def("set_build_choice_labels", &BuilderOptions::setBuildChoiceLabels, "Build choice labels", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_build_state_valuations", &BuilderOptions::setBuildStateValuations, "Build state valuations", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_build_observation_valuations", &BuilderOptions::setBuildObservationValuations, "Build observation valuations", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_build_choice_origins", &BuilderOptions::setBuildChoiceOrigins, "Build choice origins", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_exploration_checks", &BuilderOptions::setExplorationChecks, "Perform extra checks during exploration", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_scale_and_lift_transition_rewards", &BuilderOptions::setScaleAndLiftTransitionRewards, "Scale and lift transition rewards",
             py::arg("new_value") = true, py::return_value_policy::reference_internal)
        .def("set_add_out_of_bounds_state", &BuilderOptions::setAddOutOfBoundsState, "Add a state for out-of-bounds valuations", py::arg("new_value") = true,
             py::return_value_policy::reference_internal)
        .def("set_add_overlapping_guards_label", &BuilderOptions::setAddOverlappingGuardsLabel, "Label states with overlapping guards",
             py::arg("new_value") = true, py::return_value_policy::reference_internal);

    py::classh<storm::builder::ExplicitStateLookup<uint32_t>>(m, "ExplicitStateLookup", "Lookup of state ids by their variable valuation")
        .def(
            // Thin wrapper returning None instead of size() if the state does not exist
            "lookup",
            [](storm::builder::ExplicitStateLookup<uint32_t> const& lookup,
               std::map<storm::expressions::Variable, storm::expressions::Expression> const& stateDescription) -> py::object {
                auto res = lookup.lookup(stateDescription);
                if (res == lookup.size()) {
                    return py::none();
                }
                return py::cast(res);
            },
            "Get the id of the state with the given valuation, or None if no such state exists", py::arg("state_description"))
        .def("size", &storm::builder::ExplicitStateLookup<uint32_t>::size, "Number of states");
}

template<typename ValueType>
void define_builder_typed(py::module& m) {
    using Builder = storm::builder::ExplicitModelBuilder<ValueType>;
    auto const index = stormpy::bindings::typeIndex<ValueType>();

    stormpy::bindings::bindTemplateClass<typename Builder::Options>(m, "ExplicitModelBuilderOptions", index, "Options for the explicit model builder")
        .def(py::init<>(), "Create default options")
        .def_readwrite("exploration_order", &Builder::Options::explorationOrder, "The order in which to explore the model")
        .def_readwrite("fix_deadlocks", &Builder::Options::fixDeadlocks, "If set, deadlocks states will be fixed by adding a self-loop with probability 1.")
        .def_readwrite("exploration_state_limit", &Builder::Options::explorationStateLimit,
                       "If set, no further states will be explored once the given number is exceeded.");

    stormpy::bindings::bindTemplateClass<Builder>(m, "ExplicitModelBuilder", index, "Model builder for sparse models")
        .def("build", &Builder::build, "Build the model", py::call_guard<py::gil_scoped_release>())
        .def("export_explicit_state_lookup", &Builder::exportExplicitStateLookup, "Export lookup of state ids");
}

template void define_builder_typed<double>(py::module&);
template void define_builder_typed<storm::RationalNumber>(py::module&);
template void define_builder_typed<storm::RationalFunction>(py::module&);
template void define_builder_typed<storm::Interval>(py::module&);
template void define_builder_typed<storm::RationalInterval>(py::module&);

}  // namespace stormpy
