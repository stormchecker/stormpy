#include "core.h"

#include <pybind11/functional.h>
#include <storm-parsers/api/storm-parsers.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/generator/NextStateGenerator.h>
#include <storm/io/DirectEncodingExporter.h>
#include <storm/io/file.h>
#include <storm/models/symbolic/StandardRewardModel.h>
#include <storm/settings/modules/CounterexampleGeneratorSettings.h>
#include <storm/solver/OptimizationDirection.h>
#include <storm/solver/UncertaintyResolutionMode.h>
#include <storm/storage/dd/DdType.h>
#include <storm/storage/jani/Property.h>
#include <storm/utility/SignalHandler.h>
#include <storm/utility/initialize.h>

void define_core(py::module& m) {
    // Init
    m.def(
        "_set_up",
        [](std::string const& args) {
            storm::utility::setUp();
            storm::settings::initializeAll("stormpy", "stormpy");
            storm::settings::addModule<storm::settings::modules::CounterexampleGeneratorSettings>();
            storm::settings::mutableManager().setFromString(args);
        },
        "Initialize Storm", py::arg("arguments"));
    m.def(
        "set_settings", [](std::vector<std::string> const& args) { storm::settings::mutableManager().setFromExplodedString(args); }, "Set settings",
        py::arg("arguments"));
    m.def("set_loglevel_debug", []() { storm::utility::setLogLevel(l3pp::LogLevel::DEBUG); }, "set loglevel for storm to debug");
    m.def("set_loglevel_trace", []() { storm::utility::setLogLevel(l3pp::LogLevel::TRACE); });
    m.def("set_loglevel_error", []() { storm::utility::setLogLevel(l3pp::LogLevel::ERR); });

    m.def("set_timeout", &storm::utility::resources::setTimeoutAlarm, py::arg("timeout"), "Set timeout in seconds");
    m.def("reset_timeout", &storm::utility::resources::resetTimeoutAlarm, "Reset timeout");
    m.def("install_signal_handlers", &storm::utility::resources::installSignalHandler);
}

void define_parse(py::module& m) {
    // Parse formulas
    m.def(
        "parse_properties_without_context",
        [](std::string const& inputString, boost::optional<std::set<std::string>> const& propertyFilter = boost::none) {
            return storm::api::parseProperties(inputString, propertyFilter);
        },
        R"dox(
          
          Parse properties given in the prism format.
          
          :param str formula_str: A string of formulas
          :param str property_filter: A filter
          :return: A list of properties
          )dox",
        py::arg("formula_string"), py::arg("property_filter") = boost::none);
    m.def("parse_properties_for_prism_program", &storm::api::parsePropertiesForPrismProgram, R"dox(
          
          Parses properties given in the prism format, allows references to variables in the prism program.
          
          :param str formula_str: A string of formulas
          :param PrismProgram prism_program: A prism program
          :param str property_filter: A filter
          :return: A list of properties
          )dox",
          py::arg("formula_string"), py::arg("prism_program"), py::arg("property_filter") = boost::none);

    m.def("parse_properties_for_jani_model", &storm::api::parsePropertiesForJaniModel, py::arg("formula_string"), py::arg("jani_model"),
          py::arg("property_filter") = boost::none);
}

// Thin wrapper for model building using sparse representation
template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<ValueType>> buildSparseModel(storm::storage::SymbolicModelDescription const& modelDescription,
                                                                          std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas) {
    if (formulas.empty()) {
        // Build all labels and rewards
        storm::builder::BuilderOptions options(true, true);
        return storm::api::buildSparseModel<ValueType>(modelDescription, options);
    } else {
        // Only build labels necessary for formulas
        return storm::api::buildSparseModel<ValueType>(modelDescription, formulas);
    }
}

template<typename ValueType>
std::shared_ptr<storm::models::ModelBase> buildSparseModelWithOptions(storm::storage::SymbolicModelDescription const& modelDescription,
                                                                      storm::builder::BuilderOptions const& options) {
    return storm::api::buildSparseModel<ValueType>(modelDescription, options);
}

// Thin wrapper for model building using symbolic representation
template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> buildSymbolicModel(storm::storage::SymbolicModelDescription const& modelDescription,
                                                                                      std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas,
                                                                                      storm::Environment const& env) {
    if (formulas.empty()) {
        // Build full model
        return storm::api::buildSymbolicModel<DdType, ValueType>(env, modelDescription, formulas, true);
    } else {
        // Only build labels necessary for formulas
        return storm::api::buildSymbolicModel<DdType, ValueType>(env, modelDescription, formulas, false);
    }
}

template<typename ValueType>
void define_build_sparse_model_defs(py::module& m) {
    std::string type;
    std::string classType;
    std::string desc;
    if constexpr (std::is_same_v<ValueType, double>) {
        type = "";
        classType = "";
        desc = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalNumber>) {
        type = "exact_";
        classType = "Exact";
        desc = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalFunction>) {
        type = "parametric_";
        classType = "Parametric";
        desc = "parametric ";
    } else if constexpr (std::is_same_v<ValueType, storm::Interval>) {
        type = "interval_";
        classType = "Interval";
        desc = "interval ";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalInterval>) {
        type = "exact_interval_";
        classType = "ExactInterval";
        desc = "exact interval ";
    }

    m.def(
        ("_build_sparse_" + type + "model_from_symbolic_description").c_str(), &buildSparseModel<ValueType>,
        ("Build the " + desc + "model in sparse representation" + (std::is_same_v<ValueType, storm::RationalNumber> ? " with exact number representation" : ""))
            .c_str(),
        py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def(
        ("build_sparse_" + type + "model_with_options").c_str(), &buildSparseModelWithOptions<ValueType>,
        ("Build the " + desc + "model in sparse representation" + (std::is_same_v<ValueType, storm::RationalNumber> ? " with exact number representation" : ""))
            .c_str(),
        py::arg("model_description"), py::arg("options"));
    m.def(("_build_sparse_" + type + "model_from_drn").c_str(), &storm::api::buildExplicitDRNModel<ValueType>,
          ("Build the " + desc + "model from DRN" + (std::is_same_v<ValueType, storm::RationalFunction> ? " (parametric)" : "")).c_str(), py::arg("file"),
          py::arg("options") = storm::parser::DirectEncodingParserOptions());

    py::classh<typename storm::builder::ExplicitModelBuilder<ValueType>::Options>(m, ("Explicit" + classType + "ModelBuilderOptions").c_str(),
                                                                                  "Options for the explicit model builder")
        .def(py::init<>(), "Create")
        .def_readwrite("exploration_order", &storm::builder::ExplicitModelBuilder<ValueType>::Options::explorationOrder,
                       "The order in which to explore the model")
        .def_readwrite("fix_deadlocks", &storm::builder::ExplicitModelBuilder<ValueType>::Options::fixDeadlocks,
                       "If set, deadlocks states will be fixed by adding a self-loop with probability 1.")
        .def_readwrite("exploration_state_limit", &storm::builder::ExplicitModelBuilder<ValueType>::Options::explorationStateLimit,
                       "If set, no further states will be explored once the given number is exceeded.");

    if constexpr (std::is_same_v<ValueType, double>) {
        m.def("_build_symbolic_model_from_symbolic_description", &buildSymbolicModel<storm::dd::DdType::Sylvan, double>,
              "Build the model in symbolic representation", py::arg("model_description"),
              py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>(), py::arg("environment") = storm::Environment());
        m.def("build_sparse_model_from_explicit", &storm::api::buildExplicitModel<double>, "Build the model model from explicit input",
              py::arg("transition_file"), py::arg("labeling_file"), py::arg("state_reward_file") = "", py::arg("transition_reward_file") = "",
              py::arg("choice_labeling_file") = "", py::arg("options") = storm::parser::ExplicitModelParserOptions());
        m.def("make_sparse_model_builder", &storm::api::makeExplicitModelBuilder<double>, "Construct a builder instance", py::arg("model_description"),
              py::arg("options"), py::arg("action_mask") = nullptr,
              py::arg("exploration_options") = typename storm::builder::ExplicitModelBuilder<ValueType>::Options());
        py::classh<storm::builder::ExplicitModelBuilder<double>>(m, "ExplicitModelBuilder", "Model builder for sparse models")
            .def("build", &storm::builder::ExplicitModelBuilder<double>::build, "Build the model", py::call_guard<py::gil_scoped_release>())
            .def("export_lookup", &storm::builder::ExplicitModelBuilder<double>::exportExplicitStateLookup, "Export a lookup model");
    } else if constexpr (std::is_same_v<ValueType, storm::RationalFunction>) {
        m.def("_build_symbolic_parametric_model_from_symbolic_description", &buildSymbolicModel<storm::dd::DdType::Sylvan, storm::RationalFunction>,
              "Build the parametric model in symbolic representation", py::arg("model_description"),
              py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>(), py::arg("environment") = storm::Environment());
        m.def("make_sparse_model_builder_parametric", &storm::api::makeExplicitModelBuilder<storm::RationalFunction>, "Construct a builder instance",
              py::arg("model_description"), py::arg("options"), py::arg("action_mask") = nullptr,
              py::arg("exploration_options") = typename storm::builder::ExplicitModelBuilder<ValueType>::Options());
        py::classh<storm::builder::ExplicitModelBuilder<storm::RationalFunction>>(m, "ExplicitParametricModelBuilder", "Model builder for sparse models")
            .def("build", &storm::builder::ExplicitModelBuilder<storm::RationalFunction>::build, "Build the model", py::call_guard<py::gil_scoped_release>())
            .def("export_lookup", &storm::builder::ExplicitModelBuilder<storm::RationalFunction>::exportExplicitStateLookup, "Export a lookup model");
    } else if constexpr (std::is_same_v<ValueType, storm::RationalNumber>) {
        m.def("make_sparse_model_builder_exact", &storm::api::makeExplicitModelBuilder<storm::RationalNumber>, "Construct a builder instance",
              py::arg("model_description"), py::arg("options"), py::arg("action_mask") = nullptr,
              py::arg("exploration_options") = typename storm::builder::ExplicitModelBuilder<ValueType>::Options());
    }
}

void define_build(py::module& m) {
    py::classh<storm::parser::DirectEncodingParserOptions>(m, "DirectEncodingParserOptions", "Options for the .drn parser")
        .def(py::init<>(), "initialise")
        .def_readwrite("build_choice_labels", &storm::parser::DirectEncodingParserOptions::buildChoiceLabeling, "Build with choice labels");

    py::native_enum<storm::builder::ExplorationOrder>(m, "ExplorationOrder", "enum.Enum")
        .value("DFS", storm::builder::ExplorationOrder::Dfs)
        .value("BFS", storm::builder::ExplorationOrder::Bfs)
        .finalize();

    py::classh<typename storm::parser::ExplicitModelParserOptions>(m, "ExplicitModelParserOptions", "Options for the explicit model parser")
        .def(py::init<>(), "Create")
        .def_readwrite("fix_deadlocks", &storm::parser::ExplicitModelParserOptions::fixDeadlocks,
                       "If set, deadlocks states will be fixed by adding a self-loop with probability 1.")
        .def_readwrite("build_choice_labels", &storm::parser::ExplicitModelParserOptions::buildChoiceLabels, "Whether to build choice labels.");

    // Build model
    define_build_sparse_model_defs<double>(m);
    define_build_sparse_model_defs<storm::RationalNumber>(m);
    define_build_sparse_model_defs<storm::RationalFunction>(m);
    define_build_sparse_model_defs<storm::Interval>(m);
    define_build_sparse_model_defs<storm::RationalInterval>(m);

    py::classh<storm::builder::ExplicitStateLookup<uint32_t>>(m, "ExplicitStateLookup", "Lookup model for states")
        .def(
            "lookup",
            [](storm::builder::ExplicitStateLookup<uint32_t> const& lookup,
               std::map<storm::expressions::Variable, storm::expressions::Expression> const& stateDescription) -> py::object {
                auto res = lookup.lookup(stateDescription);
                if (res == lookup.size()) {
                    return py::none();
                } else {
                    return py::cast(res);
                }
            },
            py::arg("state_description"))

        ;

    py::classh<storm::builder::BuilderOptions>(m, "BuilderOptions", "Options for building process")
        .def(py::init<std::vector<std::shared_ptr<storm::logic::Formula const>> const&>(), "Initialise with formulae to preserve", py::arg("formulae"))
        .def(py::init<bool, bool>(), "Initialise without formulae", py::arg("build_all_reward_models") = true, py::arg("build_all_labels") = true)
        .def_property_readonly("preserved_label_names", &storm::builder::BuilderOptions::getLabelNames, "Labels preserved")
        .def("set_build_state_valuations", &storm::builder::BuilderOptions::setBuildStateValuations, "Build state valuations", py::arg("new_value") = true)
        .def("set_build_observation_valuations", &storm::builder::BuilderOptions::setBuildObservationValuations, "Build observation valuations",
             py::arg("new_value") = true)
        .def("set_build_with_choice_origins", &storm::builder::BuilderOptions::setBuildChoiceOrigins, "Build choice origins", py::arg("new_value") = true)
        .def("set_add_out_of_bounds_state", &storm::builder::BuilderOptions::setAddOutOfBoundsState, "Build with out of bounds state",
             py::arg("new_value") = true)
        .def("set_add_overlapping_guards_label", &storm::builder::BuilderOptions::setAddOverlappingGuardsLabel, "Build with overlapping guards state labeled",
             py::arg("new_value") = true)
        .def("set_build_choice_labels", &storm::builder::BuilderOptions::setBuildChoiceLabels, "Build with choice labels", py::arg("new_value") = true)
        .def("set_exploration_checks", &storm::builder::BuilderOptions::setExplorationChecks, "Perform extra checks during exploration",
             py::arg("new_value") = true)
        .def("set_build_all_labels", &storm::builder::BuilderOptions::setBuildAllLabels, "Build with all state labels", py::arg("new_value") = true)
        .def("set_build_all_reward_models", &storm::builder::BuilderOptions::setBuildAllRewardModels, "Build with all reward models",
             py::arg("new_value") = true);

    py::classh<storm::generator::ActionMask<double>> actionmask(m, "ActionMaskDouble");
    py::classh<storm::generator::StateValuationFunctionMask<double>> actfuncmask(m, "StateValuationFunctionActionMaskDouble", actionmask);
    actfuncmask.def(py::init<std::function<bool(storm::expressions::SimpleValuation const&, uint64_t)>>(), py::arg("f"));
}

void define_optimality_type(py::module& m) {
    py::native_enum<storm::solver::OptimizationDirection>(m, "OptimizationDirection", "enum.Enum")
        .value("MINIMIZE", storm::solver::OptimizationDirection::Minimize)
        .value("MAXIMIZE", storm::solver::OptimizationDirection::Maximize)
        .finalize();

    py::native_enum<storm::solver::UncertaintyResolutionMode>(m, "UncertaintyResolutionMode", "enum.Enum")
        .value("MINIMIZE", storm::solver::UncertaintyResolutionMode::Minimize)
        .value("MAXIMIZE", storm::solver::UncertaintyResolutionMode::Maximize)
        .value("ROBUST", storm::solver::UncertaintyResolutionMode::Robust)
        .value("COOPERATIVE", storm::solver::UncertaintyResolutionMode::Cooperative)
        .value("UNSET", storm::solver::UncertaintyResolutionMode::Unset)
        .finalize();
}

// Thin wrapper for exporting model
template<typename ValueType>
void exportDRN(std::shared_ptr<storm::models::sparse::Model<ValueType>> model, std::string const& file, storm::io::DirectEncodingExporterOptions options) {
    storm::api::exportSparseModelAsDrn<ValueType>(model, file, options);
}

template<typename ValueType>
void define_export_drn(py::module& m) {
    std::string prefix;
    std::string suffix;
    if constexpr (std::is_same_v<ValueType, double>) {
        prefix = "";
        suffix = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalNumber>) {
        prefix = "_exact";
        suffix = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalFunction>) {
        prefix = "_parametric";
        suffix = "";
    } else if constexpr (std::is_same_v<ValueType, storm::Interval>) {
        prefix = "";
        suffix = "_interval";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalInterval>) {
        prefix = "_exact";
        suffix = "_interval";
    }

    m.def(("_export" + prefix + "_to_drn" + suffix).c_str(), &exportDRN<ValueType>,
          ("Export " + (std::is_same_v<ValueType, storm::RationalFunction> ? std::string("parametric ") : std::string()) + "model in DRN format").c_str(),
          py::arg("model"), py::arg("file"), py::arg("options") = storm::io::DirectEncodingExporterOptions());
}

void define_export(py::module& m) {
    py::classh<storm::io::DirectEncodingExporterOptions>(m, "DirectEncodingExporterOptions")
        .def(py::init<>())
        .def_readwrite("allow_placeholders", &storm::io::DirectEncodingExporterOptions::allowPlaceholders)
        .def_readwrite("outputPrecision", &storm::io::DirectEncodingExporterOptions::outputPrecision);

    // Export
    define_export_drn<double>(m);
    define_export_drn<storm::Interval>(m);
    define_export_drn<storm::RationalInterval>(m);
    define_export_drn<storm::RationalNumber>(m);
    define_export_drn<storm::RationalFunction>(m);
}
