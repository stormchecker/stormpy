#include "pars.h"
#include "storm-pars/settings/modules/ParametricSettings.h"
#include "storm-pars/settings/modules/RegionSettings.h"
#include "storm-pars/transformer/SparseParametricDtmcSimplifier.h"
#include "storm-pars/transformer/SparseParametricMdpSimplifier.h"
#include "storm/settings/SettingsManager.h"

typedef storm::models::sparse::Dtmc<storm::RationalFunction> Dtmc;
typedef storm::models::sparse::Mdp<storm::RationalFunction> Mdp;
typedef storm::transformer::SparseParametricDtmcSimplifier<Dtmc> SparseParametricDtmcSimplifier;
typedef storm::transformer::SparseParametricMdpSimplifier<Mdp> SparseParametricMdpSimplifier;

void define_pars(py::module& m) {
    m.def(
        "_set_up",
        []() {
            storm::settings::addModule<storm::settings::modules::ParametricSettings>();
            storm::settings::addModule<storm::settings::modules::RegionSettings>();
        },
        "Initialize Storm-pars");

    py::class_<SparseParametricDtmcSimplifier, std::shared_ptr<SparseParametricDtmcSimplifier>>(m, "_SparseParametricDtmcSimplifier",
                                                                                                "Model simplifier for parametric DTMCs")
        .def(py::init<Dtmc const&>(), py::arg("dtmc"))
        .def(
            "simplify", [](SparseParametricDtmcSimplifier& simplifier, storm::logic::Formula const& formula) -> bool { return simplifier.simplify(formula); },
            "Simplify model", py::arg("formula"))
        .def_property_readonly(
            "simplified_model", [](SparseParametricDtmcSimplifier const& simplifier) { return simplifier.getSimplifiedModel(); }, "Return simplified model")
        .def_property_readonly(
            "simplified_formula", [](SparseParametricDtmcSimplifier const& simplifier) { return simplifier.getSimplifiedFormula(); },
            "Return simplified formula");

    py::class_<SparseParametricMdpSimplifier, std::shared_ptr<SparseParametricMdpSimplifier>>(m, "_SparseParametricMdpSimplifier",
                                                                                              "Model simplifier for parametric MDPs")
        .def(py::init<Mdp const&>(), py::arg("mdp"))
        .def(
            "simplify", [](SparseParametricMdpSimplifier& simplifier, storm::logic::Formula const& formula) -> bool { return simplifier.simplify(formula); },
            "Simplify model", py::arg("formula"))
        .def_property_readonly(
            "simplified_model", [](SparseParametricMdpSimplifier const& simplifier) { return simplifier.getSimplifiedModel(); }, "Return simplified model")
        .def_property_readonly(
            "simplified_formula", [](SparseParametricMdpSimplifier const& simplifier) { return simplifier.getSimplifiedFormula(); },
            "Return simplified formula");
}
