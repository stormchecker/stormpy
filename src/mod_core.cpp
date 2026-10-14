#include <storm/adapters/IntervalAdapter.h>

#include "src/common.h"
#include "src/core/analysis.h"
#include "src/core/api.h"
#include "src/core/builder.h"
#include "src/core/counterexamples.h"
#include "src/core/environment.h"
#include "src/core/generator.h"
#include "src/core/io.h"
#include "src/core/modelchecker.h"
#include "src/core/modelchecker_multiobjective.h"
#include "src/core/modelchecker_results.h"
#include "src/core/parser.h"
#include "src/core/settings.h"
#include "src/core/simulator.h"
#include "src/core/solver.h"
#include "src/core/storage.h"
#include "src/core/transformer.h"
#include "src/core/utility.h"

PYBIND11_MODULE(_core, m) {
    m.doc() = "Functionality of the core library of Storm";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    using namespace stormpy;

    // We need the `DdType` type registration from this module, so we have to import the entire module here.
    py::module::import("stormpy.developer.storage._storage");
    // Solver enums and storage classes are used as default arguments by other classes
    define_solver(m);
    define_smt_solver(m);
    define_storage(m);

    define_analysis(m);
    define_builder(m);
    define_builder_typed<double>(m);
    define_builder_typed<storm::RationalNumber>(m);
    define_builder_typed<storm::RationalFunction>(m);
    define_builder_typed<storm::Interval>(m);
    define_builder_typed<storm::RationalInterval>(m);
    define_counterexamples(m);
    define_environment(m);
    define_generator(m);
    define_io(m);
    define_modelchecker(m);
    define_modelchecker_typed<double>(m);
    define_modelchecker_typed<storm::RationalNumber>(m);
    define_modelchecker_typed<storm::RationalFunction>(m);
    define_modelchecker_multiobjective_typed<double>(m);
    define_modelchecker_multiobjective_typed<storm::RationalNumber>(m);
    define_modelchecker_results(m);
    define_modelchecker_results_typed<double>(m);
    define_modelchecker_results_typed<storm::RationalNumber>(m);
    define_modelchecker_results_typed<storm::RationalFunction>(m);
    define_parser(m);
    define_settings(m);
    define_simulator_sparse_typed<double>(m);
    define_simulator_sparse_typed<storm::RationalNumber>(m);
    define_simulator_prism_typed<double>(m);
    define_transformer(m);
    define_transformer_typed<double>(m);
    define_transformer_typed<storm::RationalNumber>(m);
    define_transformer_typed<storm::RationalFunction>(m);
    define_transformer_typed<storm::Interval>(m);
    define_transformer_typed<storm::RationalInterval>(m);
    define_transformer_add_uncertainty_typed<double>(m);
    define_transformer_add_uncertainty_typed<storm::RationalNumber>(m);
    define_utility(m);
    define_utility_graph_typed<double>(m);
    define_utility_graph_typed<storm::RationalNumber>(m);
    define_utility_graph_typed<storm::RationalFunction>(m);

    // storm-parsers/api/
    define_parsers_api_model_descriptions(m);
    define_parsers_api_properties(m);
    define_parsers_api_explicit_models_typed<double>(m);
    define_parsers_api_explicit_models_typed<storm::RationalNumber>(m);
    define_parsers_api_explicit_models_typed<storm::RationalFunction>(m);
    define_parsers_api_explicit_models_typed<storm::Interval>(m);
    define_parsers_api_explicit_models_typed<storm::RationalInterval>(m);

    // storm/api/
    define_api_properties(m);
    define_api_bisimulation_typed<double>(m);
    define_api_bisimulation_typed<storm::RationalFunction>(m);
    define_api_builder_typed<double>(m);
    define_api_builder_typed<storm::RationalNumber>(m);
    define_api_builder_typed<storm::RationalFunction>(m);
    define_api_builder_typed<storm::Interval>(m);
    define_api_builder_typed<storm::RationalInterval>(m);
    define_api_export_typed<double>(m);
    define_api_export_typed<storm::RationalNumber>(m);
    define_api_export_typed<storm::RationalFunction>(m);
    define_api_export_typed<storm::Interval>(m);
    define_api_export_typed<storm::RationalInterval>(m);
    define_api_transformation_typed<double>(m);
    define_api_transformation_typed<storm::RationalNumber>(m);
    define_api_transformation_typed<storm::RationalFunction>(m);
    define_api_verification_typed<double>(m);
    define_api_verification_typed<storm::RationalNumber>(m);
    define_api_verification_typed<storm::RationalFunction>(m);
    define_api_verification_typed<storm::Interval>(m);
    define_api_verification_typed<storm::RationalInterval>(m);
}
