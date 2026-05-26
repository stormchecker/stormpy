#include "src/common.h"
#include "src/core/analysis.h"
#include "src/core/bisimulation.h"
#include "src/core/core.h"
#include "src/core/counterexample.h"
#include "src/core/environment.h"
#include "src/core/input.h"
#include "src/core/modelchecking.h"
#include "src/core/multiobjective.h"
#include "src/core/result.h"
#include "src/core/simulator.h"
#include "src/core/transformation.h"

PYBIND11_MODULE(_core, m) {
    m.doc() = "core";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_environment(m);
    define_core(m);

    define_property(m);
    define_parse(m);
    define_build(m);
    define_optimality_type(m);
    define_export(m);
    define_result(m);
    define_typed_result<double>(m, "");
    define_typed_result<storm::RationalNumber>(m, "Exact");
    define_typed_result<storm::RationalFunction>(m, "Parametric");
    define_check_task<double>(m, "CheckTask");
    define_check_task<storm::RationalNumber>(m, "ExactCheckTask");
    define_check_task<storm::RationalFunction>(m, "ParametricCheckTask");
    define_modelchecking(m);
    define_multiobjective<double>(m, "Double");
    define_multiobjective<storm::RationalNumber>(m, "Exact");
    define_counterexamples(m);
    define_bisimulation(m);
    define_input(m);
    define_graph_constraints(m);
    define_transformation(m);
    define_transformation_typed<double>(m, "Double");
    define_transformation_typed<storm::RationalNumber>(m, "Exact");
    define_transformation_typed<storm::RationalFunction>(m, "RatFunc");
    define_transformation_typed_only_numbers<double>(m, "Double");
    define_transformation_typed_only_numbers<storm::RationalNumber>(m, "Exact");
    define_sparse_model_simulator<double>(m, "Double");
    define_sparse_model_simulator<storm::RationalNumber>(m, "Exact");
    define_prism_program_simulator<double>(m, "Double");
}
