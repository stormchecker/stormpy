
#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>

#include "src/common.h"
#include "src/pomdp/generator.h"
#include "src/pomdp/memory.h"
#include "src/pomdp/qualitative_analysis.h"
#include "src/pomdp/quantitative_analysis.h"
#include "src/pomdp/tracker.h"
#include "src/pomdp/transformations.h"

PYBIND11_MODULE(_pomdp, m) {
    m.doc() = "Functionality for POMDP analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif
    define_tracker<double>(m, "Double");
    define_tracker<storm::RationalNumber>(m, "Exact");
    define_qualitative_policy_search<double>(m, "Double");
    define_qualitative_policy_search_nt(m);
    define_memory(m);
    define_transformations_nt(m);

    define_transformations<double>(m, "Double");
    define_transformations<storm::RationalNumber>(m, "Exact");
    define_transformations<storm::RationalFunction>(m, "Rf");

    define_transformations_int<double>(m, "Double");
    define_transformations_int<storm::RationalNumber>(m, "Exact");
    define_transformations_int<storm::RationalFunction>(m, "Parametric");
    define_transformations_int<storm::Interval>(m, "Interval");
    define_transformations_int<storm::RationalInterval>(m, "RationalInterval");

    define_belief_exploration<double>(m, "Double");
    define_verimon_generator<double>(m, "Double");
    define_verimon_generator<storm::RationalNumber>(m, "Exact");
}
