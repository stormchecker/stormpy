#include "common.h"

#include "core/core.h"
#include "core/result.h"
#include "core/modelchecking.h"
#include "core/bisimulation.h"
#include "core/input.h"
#include "core/analysis.h"
#include "core/counterexample.h"
#include "core/environment.h"
#include "core/transformation.h"
#include "core/simulator.h"

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
    define_modelchecking(m);
    define_counterexamples(m);
    define_bisimulation(m);
    define_input(m);
    define_graph_constraints(m);
    define_transformation(m);
    define_transformation_typed<double>(m, "Double");
    define_transformation_typed<storm::RationalNumber>(m, "Exact");
    define_transformation_typed<storm::RationalFunction>(m, "RatFunc");
    define_sparse_model_simulator<double>(m, "Double");
    define_sparse_model_simulator<storm::RationalNumber>(m, "Exact");
    define_prism_program_simulator<double>(m, "Double");

}
