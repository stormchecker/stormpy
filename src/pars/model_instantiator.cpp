#include "model_instantiator.h"

#include <storm-pars/modelchecker/instantiation/SparseCtmcInstantiationModelChecker.h>
#include <storm-pars/modelchecker/instantiation/SparseDtmcInstantiationModelChecker.h>
#include <storm-pars/modelchecker/instantiation/SparseMdpInstantiationModelChecker.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/environment/Environment.h>
#include <storm/modelchecker/prctl/helper/BaierUpperRewardBoundsComputer.h>
#include <storm/modelchecker/prctl/helper/DsMpiUpperRewardBoundsComputer.h>
#include <storm/modelchecker/propositional/SparsePropositionalModelChecker.h>
#include <storm/modelchecker/results/ExplicitQualitativeCheckResult.h>
#include <storm/modelchecker/results/ExplicitQuantitativeCheckResult.h>
#include <storm/models/sparse/Dtmc.h>
#include <storm/models/sparse/Model.h>
#include <storm/models/sparse/StandardRewardModel.h>
#include <storm/solver/MinMaxLinearEquationSolver.h>
#include <storm/utility/NumberTraits.h>
#include <storm/utility/graph.h>
#include <storm/utility/vector.h>

#include "src/binding_type_index.h"

template<typename ValueType>
using Model = storm::models::sparse::Model<ValueType>;
template<typename ValueType>
using Dtmc = storm::models::sparse::Dtmc<ValueType>;
template<typename ValueType>
using Mdp = storm::models::sparse::Mdp<ValueType>;
template<typename ValueType>
using Ctmc = storm::models::sparse::Ctmc<ValueType>;
template<typename ValueType>
using MarkovAutomaton = storm::models::sparse::MarkovAutomaton<ValueType>;

using namespace storm::modelchecker;

// Helper: define typed ModelInstantiator class
template<storm::models::ModelType ModelKind, template<typename> class SparseModel, typename ValueType>
void define_typed_instantiator(py::module& m) {
    using ParametricModel = SparseModel<storm::RationalFunction>;
    using InstantiatedModel = SparseModel<ValueType>;
    using Instantiator = storm::utility::ModelInstantiator<ParametricModel, InstantiatedModel>;

    auto implementation = stormpy::bindings::bindTemplateClass<Instantiator>(m, "ModelInstantiator", stormpy::bindings::typeIndex<ModelKind, ValueType>(),
                                                                             "Instantiate a parametric model");
    implementation.def(py::init<ParametricModel>(), "model"_a)
        .def("instantiate", &Instantiator::instantiate, "valuation"_a, "Instantiate model with given parameter values");
}

template<typename ValueType>
void define_model_instantiator(py::module& m) {
    define_typed_instantiator<storm::models::ModelType::Dtmc, Dtmc, ValueType>(m);
    define_typed_instantiator<storm::models::ModelType::Mdp, Mdp, ValueType>(m);
    define_typed_instantiator<storm::models::ModelType::Ctmc, Ctmc, ValueType>(m);
    define_typed_instantiator<storm::models::ModelType::MarkovAutomaton, MarkovAutomaton, ValueType>(m);
}

// Helper: define typed base + derived instantiation checker pair
template<storm::models::ModelType ModelKind, template<typename> class SparseModel, template<typename, typename> class InstantiationChecker, typename ResultType>
void define_typed_checker(py::module& m) {
    using ParametricModel = SparseModel<storm::RationalFunction>;
    using CheckerType = InstantiationChecker<ParametricModel, ResultType>;
    using BaseChecker = SparseInstantiationModelChecker<ParametricModel, ResultType>;
    auto const index = stormpy::bindings::typeIndex<ModelKind, ResultType>();

    auto base = stormpy::bindings::bindInternalClass<BaseChecker>(m, stormpy::bindings::templateClassName("SparseInstantiationModelCheckerBase", index),
                                                                  "Instantiation checker base");
    base.def("specify_formula", &BaseChecker::specifyFormula, "check_task"_a, "Specify the formula to check");

    auto implementation =
        stormpy::bindings::bindTemplateClass<CheckerType>(m, "SparseInstantiationModelChecker", index, "Instantiate and check a parametric model", base);
    implementation.def(py::init<storm::Environment, ParametricModel>(), "environment"_a, "model"_a)
        .def(
            "check",
            [](CheckerType& c, storm::Environment const& env,
               storm::utility::parametric::Valuation<storm::RationalFunction> const& val) -> std::shared_ptr<CheckResult> { return c.check(env, val); },
            "environment"_a, "valuation"_a, "Check the model instantiated with the given valuation")
        .def("set_instantiations_are_graph_preserving", &CheckerType::setInstantiationsAreGraphPreserving, "value"_a,
             "Set whether all instantiations preserve the graph structure");
}

template<typename ValueType>
void define_model_instantiation_checker(py::module& m) {
    define_typed_checker<storm::models::ModelType::Dtmc, Dtmc, SparseDtmcInstantiationModelChecker, ValueType>(m);
    define_typed_checker<storm::models::ModelType::Mdp, Mdp, SparseMdpInstantiationModelChecker, ValueType>(m);
    define_typed_checker<storm::models::ModelType::Ctmc, Ctmc, SparseCtmcInstantiationModelChecker, ValueType>(m);
}

template void define_model_instantiator<double>(py::module&);
template void define_model_instantiator<storm::RationalNumber>(py::module&);
template void define_model_instantiator<storm::RationalFunction>(py::module&);
template void define_model_instantiation_checker<double>(py::module&);
template void define_model_instantiation_checker<storm::RationalNumber>(py::module&);
