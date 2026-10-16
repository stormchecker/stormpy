#include "pars.h"

#include <storm-pars/api/synthesis.h>
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

template<typename RegionOrBound>
void define_synthesis_functions(py::module& m, char const* regionArgument) {
    using Model = std::shared_ptr<storm::models::sparse::Model<storm::RationalFunction>>;
    using Formula = std::shared_ptr<storm::logic::Formula const>;
    using Engine = storm::modelchecker::RegionCheckEngine;
    m.def("verify", py::overload_cast<storm::Environment const&, Model const&, Formula const&, RegionOrBound const&, Engine>(&storm::api::verify),
          "Verify a bounded probability or reward formula for all well-defined valuations in the region", "environment"_a, "model"_a, "formula"_a,
          py::arg(regionArgument), "engine"_a = Engine::ParameterLifting);
    m.def("check_feasibility",
          py::overload_cast<storm::Environment const&, Model const&, Formula const&, RegionOrBound const&, storm::pars::FeasibilityMethod, Engine>(
              &storm::api::checkFeasibility),
          "Find a well-defined valuation satisfying a bounded probability or reward formula", "environment"_a, "model"_a, "formula"_a, py::arg(regionArgument),
          "method"_a = storm::pars::FeasibilityMethod::PLA, "region_engine"_a = Engine::ParameterLifting);
}

void define_synthesis(py::module& m) {
    using Method = storm::pars::FeasibilityMethod;
    py::native_enum<Method>(m, "FeasibilityMethod", "enum.Enum", "Methods for feasibility synthesis")
        .value("PLA", Method::PLA)
        .value("SCP", Method::SCP)
        .value("GD", Method::GD)
        .finalize();

    using Witness = storm::pars::FeasibilityResult<double>;
    py::classh<Witness>(m, "FeasibilityResult", "A satisfying parameter valuation and its value at the initial state")
        .def_readonly("value", &Witness::value, "Value at the initial state, including infinite rewards")
        .def_readonly("valuation", &Witness::valuation, "Mapping of parameters to their values");

    using Result = storm::pars::FeasibilitySynthesisResult<double>;
    py::classh<Result>(m, "FeasibilitySynthesisResult", "Feasibility decision: EXISTS_SAT, ALL_VIOLATED, or UNKNOWN, with an optional witness")
        .def_readonly("status", &Result::status, "Feasibility decision as a RegionResult")
        .def_readonly("witness", &Result::witness, "Satisfying valuation and value, or None unless the status is EXISTS_SAT");

    define_synthesis_functions<storm::storage::ParameterRegion<storm::RationalFunction>>(m, "region");
    define_synthesis_functions<storm::RationalFunctionCoefficient>(m, "region_bound");
}
