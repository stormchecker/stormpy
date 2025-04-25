#include <pybind11/functional.h>

#include "core.h"
#include "storm/utility/initialize.h"
#include "storm/utility/SignalHandler.h"
#include "storm/io/file.h"
#include "storm/io/DirectEncodingExporter.h"
#include "storm/storage/ModelFormulasPair.h"
#include "storm/storage/dd/DdType.h"
#include "storm/storage/jani/Property.h"
#include "storm/solver/OptimizationDirection.h"
#include "storm/models/symbolic/StandardRewardModel.h"
#include "storm/generator/NextStateGenerator.h"
#include "storm-parsers/api/storm-parsers.h"
#include "storm-counterexamples/settings/modules/CounterexampleGeneratorSettings.h"

void define_core(py::module& m) {
    // Init
    m.def("_set_up", [](std::string const& args) {
            storm::utility::setUp();
            storm::settings::initializeAll("stormpy", "stormpy");
            storm::settings::addModule<storm::settings::modules::CounterexampleGeneratorSettings>();
            storm::settings::mutableManager().setFromString(args);
        }, "Initialize Storm", py::arg("arguments"));
    m.def("set_settings", [](std::vector<std::string> const& args) {
            storm::settings::mutableManager().setFromExplodedString(args);
        }, "Set settings", py::arg("arguments"));
    m.def("set_loglevel_debug", []() {
        storm::utility::setLogLevel(l3pp::LogLevel::DEBUG);
    }, "set loglevel for storm to debug");
    m.def("set_loglevel_trace", []() {
        storm::utility::setLogLevel(l3pp::LogLevel::TRACE);
    });
    m.def("set_loglevel_error", []() {
        storm::utility::setLogLevel(l3pp::LogLevel::ERR);
    });

    m.def("set_timeout", &storm::utility::resources::setTimeoutAlarm, py::arg("timeout"), "Set timeout in seconds");
    m.def("reset_timeout", &storm::utility::resources::resetTimeoutAlarm, "Reset timeout");
    m.def("install_signal_handlers", &storm::utility::resources::installSignalHandler);

}

void define_parse(py::module& m) {
    // Parse formulas
    m.def("parse_properties_without_context", [](std::string const& inputString, boost::optional<std::set<std::string>> const& propertyFilter = boost::none) {
                return storm::api::parseProperties(inputString, propertyFilter);
            }, R"dox(
          
          Parse properties given in the prism format.
          
          :param str formula_str: A string of formulas
          :param str property_filter: A filter
          :return: A list of properties
          )dox", py::arg("formula_string"), py::arg("property_filter") = boost::none);
    m.def("parse_properties_for_prism_program", &storm::api::parsePropertiesForPrismProgram,  R"dox(
          
          Parses properties given in the prism format, allows references to variables in the prism program.
          
          :param str formula_str: A string of formulas
          :param PrismProgram prism_program: A prism program
          :param str property_filter: A filter
          :return: A list of properties
          )dox", py::arg("formula_string"), py::arg("prism_program"), py::arg("property_filter") = boost::none);

    m.def("parse_properties_for_jani_model", &storm::api::parsePropertiesForJaniModel, py::arg("formula_string"), py::arg("jani_model"), py::arg("property_filter") = boost::none);

    // Pair <Model,Formulas>
    py::class_<storm::storage::ModelFormulasPair>(m, "ModelFormulasPair", "Pair of model and formulas")
        .def_property_readonly("model", [](storm::storage::ModelFormulasPair const& pair) {
                return pair.model;
            }, "The model")
        .def_property_readonly("formulas", [](storm::storage::ModelFormulasPair const& pair) {
                return pair.formulas;
            }, "The formulas")
    ;
}

// Thin wrapper for model building using sparse representation
template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<ValueType>> buildSparseModel(storm::storage::SymbolicModelDescription const& modelDescription, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas) {
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
std::shared_ptr<storm::models::ModelBase> buildSparseModelWithOptions(storm::storage::SymbolicModelDescription const& modelDescription, storm::builder::BuilderOptions const& options) {
    return storm::api::buildSparseModel<ValueType>(modelDescription, options);
}

template<typename ValueType>
storm::builder::ExplicitModelBuilder<double> makeExplicitModelBuilder(storm::storage::SymbolicModelDescription const& model, storm::builder::BuilderOptions const& options) {
    return storm::api::makeExplicitModelBuilder<double>(model, options, nullptr); // Do not set ActionMask
}

// Thin wrapper for model building using symbolic representation
template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> buildSymbolicModel(storm::storage::SymbolicModelDescription const& modelDescription, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas) {
    if (formulas.empty()) {
        // Build full model
        return storm::api::buildSymbolicModel<DdType, ValueType>(modelDescription, formulas, true);
    } else {
        // Only build labels necessary for formulas
        return storm::api::buildSymbolicModel<DdType, ValueType>(modelDescription, formulas, false);
    }
}

void define_build(py::module& m) {

    py::class_<storm::parser::DirectEncodingParserOptions>(m, "DirectEncodingParserOptions", "Options for the .drn parser")
            .def(py::init<>(), "initialise")
            .def_readwrite("build_choice_labels", &storm::parser::DirectEncodingParserOptions::buildChoiceLabeling, "Build with choice labels");

    // Build model
    m.def("_build_sparse_model_from_symbolic_description", &buildSparseModel<double>, "Build the model in sparse representation", py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_build_sparse_exact_model_from_symbolic_description", &buildSparseModel<storm::RationalNumber>, "Build the model in sparse representation with exact number representation", py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_build_sparse_parametric_model_from_symbolic_description", &buildSparseModel<storm::RationalFunction>, "Build the parametric model in sparse representation", py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("build_sparse_model_with_options", &buildSparseModelWithOptions<double>, "Build the model in sparse representation", py::arg("model_description"), py::arg("options"));
    m.def("build_sparse_exact_model_with_options", &buildSparseModelWithOptions<storm::RationalNumber>, "Build the model in sparse representation with exact number representation", py::arg("model_description"), py::arg("options"));
    m.def("build_sparse_parametric_model_with_options", &buildSparseModelWithOptions<storm::RationalFunction>, "Build the model in sparse representation", py::arg("model_description"), py::arg("options"));
    m.def("_build_symbolic_model_from_symbolic_description", &buildSymbolicModel<storm::dd::DdType::Sylvan, double>, "Build the model in symbolic representation", py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_build_symbolic_parametric_model_from_symbolic_description", &buildSymbolicModel<storm::dd::DdType::Sylvan, storm::RationalFunction>, "Build the parametric model in symbolic representation", py::arg("model_description"), py::arg("formulas") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_build_sparse_model_from_drn", &storm::api::buildExplicitDRNModel<double>, "Build the model from DRN", py::arg("file"), py::arg("options") = storm::parser::DirectEncodingParserOptions());
    m.def("_build_sparse_exact_model_from_drn", &storm::api::buildExplicitDRNModel<storm::RationalNumber>, "Build the model from DRN", py::arg("file"), py::arg("options") = storm::parser::DirectEncodingParserOptions());
    m.def("_build_sparse_parametric_model_from_drn", &storm::api::buildExplicitDRNModel<storm::RationalFunction>, "Build the parametric model from DRN", py::arg("file"), py::arg("options") = storm::parser::DirectEncodingParserOptions());
    m.def("_build_sparse_interval_model_from_drn", &storm::api::buildExplicitDRNModel<storm::Interval>, "Build the interval model from DRN", py::arg("file"), py::arg("options") = storm::parser::DirectEncodingParserOptions());
    m.def("build_sparse_model_from_explicit", &storm::api::buildExplicitModel<double>, "Build the model model from explicit input", py::arg("transition_file"), py::arg("labeling_file"), py::arg("state_reward_file") = "", py::arg("transition_reward_file") = "", py::arg("choice_labeling_file") = "");

    m.def("make_sparse_model_builder", &storm::api::makeExplicitModelBuilder<double>, "Construct a builder instance", py::arg("model_description"), py::arg("options"), py::arg("action_mask") = nullptr);
    m.def("make_sparse_model_builder_exact", &storm::api::makeExplicitModelBuilder<storm::RationalNumber>, "Construct a builder instance", py::arg("model_description"), py::arg("options"), py::arg("action_mask") = nullptr);
    m.def("make_sparse_model_builder_parametric", &storm::api::makeExplicitModelBuilder<storm::RationalFunction>, "Construct a builder instance", py::arg("model_description"), py::arg("options"), py::arg("action_mask") = nullptr);

    py::class_<storm::builder::ExplicitModelBuilder<double>>(m, "ExplicitModelBuilder", "Model builder for sparse models")
        .def("build", &storm::builder::ExplicitModelBuilder<double>::build, "Build the model",  py::call_guard<py::gil_scoped_release>())
        .def("export_lookup", &storm::builder::ExplicitModelBuilder<double>::exportExplicitStateLookup, "Export a lookup model")
    ;

    py::class_<storm::builder::ExplicitModelBuilder<storm::RationalFunction>>(m, "ExplicitParametricModelBuilder", "Model builder for sparse models")
        .def("build", &storm::builder::ExplicitModelBuilder<storm::RationalFunction>::build, "Build the model", py::call_guard<py::gil_scoped_release>())
        .def("export_lookup", &storm::builder::ExplicitModelBuilder<storm::RationalFunction>::exportExplicitStateLookup, "Export a lookup model")
    ;

    py::class_<storm::builder::ExplicitStateLookup<uint32_t>>(m, "ExplicitStateLookup", "Lookup model for states")
        .def("lookup", [](storm::builder::ExplicitStateLookup<uint32_t>const& lookup, std::map<storm::expressions::Variable, storm::expressions::Expression> const& stateDescription) -> py::object
        { auto res = lookup.lookup(stateDescription); if (res==lookup.size()) {return py::none();} else {return py::cast(res);}} , py::arg("state_description"))

    ;

    py::class_<storm::builder::BuilderOptions>(m, "BuilderOptions", "Options for building process")
            .def(py::init<std::vector<std::shared_ptr<storm::logic::Formula const>> const&>(), "Initialise with formulae to preserve", py::arg("formulae"))
            .def(py::init<bool, bool>(), "Initialise without formulae", py::arg("build_all_reward_models")=true, py::arg("build_all_labels")=true)
            .def_property_readonly("preserved_label_names", &storm::builder::BuilderOptions::getLabelNames, "Labels preserved")
            .def("set_build_state_valuations", &storm::builder::BuilderOptions::setBuildStateValuations, "Build state valuations", py::arg("new_value")=true)
            .def("set_build_observation_valuations", &storm::builder::BuilderOptions::setBuildObservationValuations, "Build observation valuations", py::arg("new_value")=true)
            .def("set_build_with_choice_origins", &storm::builder::BuilderOptions::setBuildChoiceOrigins, "Build choice origins", py::arg("new_value")=true)
            .def("set_add_out_of_bounds_state", &storm::builder::BuilderOptions::setAddOutOfBoundsState, "Build with out of bounds state", py::arg("new_value")=true)
            .def("set_add_overlapping_guards_label", &storm::builder::BuilderOptions::setAddOverlappingGuardsLabel, "Build with overlapping guards state labeled", py::arg("new_value")=true)
            .def("set_build_choice_labels", &storm::builder::BuilderOptions::setBuildChoiceLabels, "Build with choice labels", py::arg("new_value")=true)
            .def("set_exploration_checks", &storm::builder::BuilderOptions::setExplorationChecks, "Perform extra checks during exploration", py::arg("new_value")=true)
            .def("set_build_all_labels" , &storm::builder::BuilderOptions::setBuildAllLabels, "Build with all state labels", py::arg("new_value")=true)
            .def("set_build_all_reward_models", &storm::builder::BuilderOptions::setBuildAllRewardModels, "Build with all reward models", py::arg("new_value")=true);

    py::class_<storm::generator::ActionMask<double>, std::shared_ptr<storm::generator::ActionMask<double>>> actionmask(m, "ActionMaskDouble");
    py::class_<storm::generator::StateValuationFunctionMask<double>, std::shared_ptr<storm::generator::StateValuationFunctionMask<double>>> actfuncmask(m, "StateValuationFunctionActionMaskDouble", actionmask);
    actfuncmask.def(py::init<std::function<bool (storm::expressions::SimpleValuation const&, uint64_t)>>(), py::arg("f"));
}

void define_optimality_type(py::module& m) {
    py::enum_<storm::solver::OptimizationDirection>(m, "OptimizationDirection")
        .value("Minimize", storm::solver::OptimizationDirection::Minimize)
        .value("Maximize", storm::solver::OptimizationDirection::Maximize)
    ;
}

// Thin wrapper for exporting model
template<typename ValueType>
void exportDRN(std::shared_ptr<storm::models::sparse::Model<ValueType>> model, std::string const& file, storm::io::DirectEncodingOptions options) {
    std::ofstream stream;
    storm::io::openFile(file, stream);
    storm::io::explicitExportSparseModel(stream, model, {}, options);
    storm::io::closeFile(stream);
}

void define_export(py::module& m) {

    py::class_<storm::io::DirectEncodingOptions> opts(m, "DirectEncodingOptions");
    opts.def(py::init<>());
    opts.def_readwrite("allow_placeholders", &storm::io::DirectEncodingOptions::allowPlaceholders);
    // Export
    m.def("_export_to_drn", &exportDRN<double>, "Export model in DRN format", py::arg("model"), py::arg("file"), py::arg("options")=storm::io::DirectEncodingOptions());
    m.def("_export_to_drn_interval", &exportDRN<storm::Interval>, "Export model in DRN format", py::arg("model"), py::arg("file"), py::arg("options")=storm::io::DirectEncodingOptions());
    m.def("_export_exact_to_drn", &exportDRN<storm::RationalNumber>, "Export model in DRN format", py::arg("model"), py::arg("file"), py::arg("options")=storm::io::DirectEncodingOptions());
    m.def("_export_parametric_to_drn", &exportDRN<storm::RationalFunction>, "Export parametric model in DRN format", py::arg("model"), py::arg("file"), py::arg("options")=storm::io::DirectEncodingOptions());
}
