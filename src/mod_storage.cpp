#include <storm/adapters/IntervalAdapter.h>
#include <storm/dd/DdType.h>

#include "src/common.h"
#include "src/storage/bitvector.h"
#include "src/storage/choiceorigins.h"
#include "src/storage/dd.h"
#include "src/storage/decomposition.h"
#include "src/storage/distribution.h"
#include "src/storage/expressions.h"
#include "src/storage/geometry.h"
#include "src/storage/jani.h"
#include "src/storage/json.h"
#include "src/storage/labeling.h"
#include "src/storage/matrix.h"
#include "src/storage/memorystructure.h"
#include "src/storage/model.h"
#include "src/storage/model_components.h"
#include "src/storage/prism.h"
#include "src/storage/scheduler.h"
#include "src/storage/state.h"
#include "src/storage/umb.h"
#include "src/storage/valuation.h"

PYBIND11_MODULE(_storage, m) {
    m.doc() = "Data structures in Storm";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_bitvector(m);
    define_json<double>(m);
    define_json<storm::RationalNumber>(m);
    define_dd_nt(m);
    auto ddSylvan = define_dd<storm::dd::DdType::Sylvan>(m);
    define_dd_typed<storm::dd::DdType::Sylvan, double>(m, ddSylvan);
    define_model(m);
    define_sparse_model<double>(m);
    define_sparse_model<storm::RationalNumber>(m);
    define_sparse_model<storm::Interval>(m);
    define_sparse_model<storm::RationalFunction>(m);
    define_sparse_model<storm::RationalInterval>(m);
    define_valuation(m);
    define_valuation_transformer(m);
    define_simplevaluation(m);
    define_sparse_matrix<double>(m);
    define_sparse_matrix<storm::RationalNumber>(m);
    define_sparse_matrix<storm::Interval>(m);
    define_sparse_matrix<storm::RationalInterval>(m);
    define_sparse_matrix<storm::RationalFunction>(m);
    define_symbolic_model<storm::dd::DdType::Sylvan, double>(m);
    define_symbolic_model<storm::dd::DdType::Sylvan, storm::RationalNumber>(m);
    define_symbolic_model<storm::dd::DdType::Sylvan, storm::RationalFunction>(m);
    define_state<double>(m);
    define_state<storm::RationalNumber>(m);
    define_state<storm::Interval>(m);
    define_state<storm::RationalInterval>(m);
    define_state<storm::RationalFunction>(m);
    define_memorystructure_typed<double>(m);
    define_memorystructure_typed<storm::RationalNumber>(m);
    define_memorystructure_typed<storm::Interval>(m);
    define_memorystructure_typed<storm::RationalInterval>(m);
    define_memorystructure_typed<storm::RationalFunction>(m);
    define_memorystructure_untyped(m);
    define_prism(m);
    define_jani(m);
    define_jani_transformers(m);
    define_labeling(m);
    define_origins(m);
    define_expressions(m);
    define_scheduler<double>(m);
    define_scheduler<storm::RationalNumber>(m);
    define_scheduler<storm::Interval>(m);
    define_scheduler<storm::RationalInterval>(m);
    define_scheduler<storm::RationalFunction>(m);
    define_distribution<double>(m);
    define_distribution<storm::RationalNumber>(m);
    define_distribution<storm::Interval>(m);
    define_distribution<storm::RationalInterval>(m);
    define_sparse_model_components<double>(m);
    define_sparse_model_components<storm::RationalNumber>(m);
    define_sparse_model_components<storm::Interval>(m);
    define_sparse_model_components<storm::RationalInterval>(m);
    define_sparse_model_components<storm::RationalFunction>(m);
    define_geometry<double>(m);
    define_geometry<storm::RationalNumber>(m);

    define_maximal_end_components(m);
    define_maximal_end_component_decomposition<double>(m);
    define_maximal_end_component_decomposition<storm::RationalNumber>(m);
    define_maximal_end_component_decomposition<storm::Interval>(m);
    define_maximal_end_component_decomposition<storm::RationalInterval>(m);
    define_maximal_end_component_decomposition<storm::RationalFunction>(m);
    define_umb(m);
    define_umb_typed<double>(m);
    define_umb_typed<storm::RationalNumber>(m);
    define_umb_typed<storm::Interval>(m);
    define_umb_typed<storm::RationalInterval>(m);
}
