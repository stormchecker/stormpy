
#include "common.h"

#include "pomdp/generator.h"
#include "pomdp/memory.h"
#include "pomdp/qualitative_analysis.h"
#include "pomdp/quantitative_analysis.h"
#include "pomdp/tracker.h"
#include "pomdp/transformations.h"
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>

PYBIND11_MODULE(pomdp, m) {
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
  define_belief_exploration<double>(m, "Double");
  define_verimon_generator<double>(m, "Double");
  define_verimon_generator<storm::RationalNumber>(m, "Exact");

  define_transformations<storm::RationalFunction>(m, "Rf");
}
