#include "pars.h"

#include <storm-pars/transformer/SparseParametricModelSimplifier.h>

#include "src/binding_type_index.h"

template<storm::models::ModelType ModelKind, typename SparseModel>
void define_simplifier(py::module& m, std::string const& modelName) {
    using Simplifier = storm::transformer::SparseParametricModelSimplifier<SparseModel>;
    stormpy::bindings::bindTemplateClass<Simplifier>(m, "SparseParametricModelSimplifier", stormpy::bindings::typeIndex<ModelKind>(),
                                                     "Model simplifier for parametric " + modelName)
        .def(py::init<SparseModel const&>(), "model"_a)
        .def(
            "simplify", [](Simplifier& simplifier, storm::logic::Formula const& formula) -> bool { return simplifier.simplify(formula); }, "Simplify model",
            "formula"_a)
        .def_property_readonly("simplified_model", &Simplifier::getSimplifiedModel, "Return simplified model")
        .def_property_readonly("simplified_formula", &Simplifier::getSimplifiedFormula, "Return simplified formula");
}

void define_pars(py::module& m) {
    define_simplifier<storm::models::ModelType::Dtmc, storm::models::sparse::Dtmc<storm::RationalFunction>>(m, "DTMCs");
    define_simplifier<storm::models::ModelType::Mdp, storm::models::sparse::Mdp<storm::RationalFunction>>(m, "MDPs");
}
