
#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>

#include "src/common.h"
#include "src/pomdp/belief_verification.h"
#include "src/pomdp/generator.h"
#include "src/pomdp/memory.h"
#include "src/pomdp/qualitative_analysis.h"
#include "src/pomdp/tracker.h"
#include "src/pomdp/transformations.h"

PYBIND11_MODULE(_pomdp, m) {
    m.doc() = "Functionality for POMDP analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif
    define_tracker<double>(m);
    define_tracker<storm::RationalNumber>(m);
    define_qualitative_policy_search_nt(m);
    define_qualitative_policy_search<double>(m);
    define_belief_verification_nt(m);
    define_belief_verification<double>(m);
    define_belief_verification<storm::RationalNumber>(m);
    define_memory(m);
    define_transformations_nt(m);

    define_transformations<double>(m);
    define_transformations<storm::RationalNumber>(m);
    define_transformations<storm::RationalFunction>(m);

    define_observation_trace_unfolder<double>(m);
    define_observation_trace_unfolder<storm::RationalNumber>(m);
    define_observation_trace_unfolder<storm::RationalFunction>(m);
    define_observation_trace_unfolder<storm::Interval>(m);
    define_observation_trace_unfolder<storm::RationalInterval>(m);

    define_verimon_generator<double>(m);
    define_verimon_generator<storm::RationalNumber>(m);
}
