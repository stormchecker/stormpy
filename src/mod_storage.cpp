#include "common.h"

#include "storage/bitvector.h"
#include "storage/dd.h"
#include "storage/model.h"
#include "storage/decomposition.h"
#include "storage/matrix.h"
#include "storage/model_components.h"
#include "storage/distribution.h"
#include "storage/scheduler.h"
#include "storage/prism.h"
#include "storage/jani.h"
#include "storage/state.h"
#include "src/storage/valuation.h"
#include "storage/choiceorigins.h"
#include "storage/labeling.h"
#include "storage/expressions.h"
#include "storage/geometry.h"

#include "storm/storage/dd/DdType.h"

PYBIND11_MODULE(_storage, m) {
    m.doc() = "Data structures in Storm";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_bitvector(m);
    define_dd<storm::dd::DdType::Sylvan>(m, "Sylvan");
    define_dd_nt(m);

    define_model(m);
    define_sparse_model<double>(m, "");
    define_sparse_model<storm::RationalNumber>(m, "Exact");
    define_sparse_model<storm::Interval>(m, "Interval");
    define_sparse_parametric_model(m);
    define_statevaluation(m);
    define_simplevaluation(m);
    define_sparse_matrix<double>(m, "");
    define_sparse_matrix<storm::RationalNumber>(m, "Exact");
    define_sparse_matrix<storm::Interval>(m, "Interval");
    define_sparse_matrix<storm::RationalFunction>(m, "Parametric");
    define_sparse_matrix_nt(m);
    define_symbolic_model<storm::dd::DdType::Sylvan>(m, "Sylvan");
    define_state<double>(m, "");
    define_state<storm::RationalNumber>(m, "Exact");
    define_state<storm::Interval>(m, "Interval");
    define_state<storm::RationalFunction>(m, "Parametric");
    define_prism(m);
    define_jani(m);
    define_jani_transformers(m);
    define_labeling(m);
    define_origins(m);
    define_expressions(m);
    define_scheduler<double>(m, "");
    define_scheduler<storm::RationalNumber>(m, "Exact");
    define_scheduler<storm::Interval>(m, "Interval");
    define_scheduler<storm::RationalFunction>(m, "Parametric");
    define_distribution<double>(m, "");
    define_distribution<storm::RationalNumber>(m, "Exact");
    define_distribution<storm::Interval>(m, "Interval");
    define_sparse_model_components<double>(m, "");
    define_sparse_model_components<storm::RationalNumber>(m, "Exact");
    define_sparse_model_components<storm::Interval>(m, "Interval");
    define_sparse_model_components<storm::RationalFunction>(m, "Parametric");
    define_geometry<double>(m, "Double");
    define_geometry<storm::RationalNumber>(m, "Exact");

    define_maximal_end_components(m);
    define_maximal_end_component_decomposition<double>(m, "_double");
    define_maximal_end_component_decomposition<storm::RationalNumber>(m, "_exact");
    define_maximal_end_component_decomposition<storm::Interval>(m, "_interval");
    define_maximal_end_component_decomposition<storm::RationalFunction>(m, "_ratfunc");

}
