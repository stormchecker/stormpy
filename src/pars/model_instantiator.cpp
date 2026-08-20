#include "model_instantiator.h"

#include <storm-pars/modelchecker/instantiation/SparseCtmcInstantiationModelChecker.h>
#include <storm-pars/modelchecker/instantiation/SparseDtmcInstantiationModelChecker.h>
#include <storm-pars/modelchecker/instantiation/SparseMdpInstantiationModelChecker.h>
#include <storm-pars/transformer/SparseParametricDtmcSimplifier.h>
#include <storm/adapters/RationalFunctionAdapter.h>
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
template<typename ParametricModel, typename InstantiatedModel>
void define_typed_instantiator(py::module& m, const char* pyName, const char* pyDesc) {
    py::classh<storm::utility::ModelInstantiator<ParametricModel, InstantiatedModel>>(m, pyName, pyDesc)
        .def(py::init<ParametricModel>(), "parametric model"_a)
        .def("instantiate", &storm::utility::ModelInstantiator<ParametricModel, InstantiatedModel>::instantiate,
             "Instantiate model with given parameter values");
}

template<typename ValueType>
void define_model_instantiator(py::module& m) {
    std::string prefix;
    if constexpr (std::is_same_v<ValueType, double>) {
        prefix = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalFunction>) {
        prefix = "Partial";
    }

    define_typed_instantiator<Dtmc<storm::RationalFunction>, Dtmc<ValueType>>(m, (prefix + "PDtmcInstantiator").c_str(), "Instantiate PDTMCs to DTMCs");
    define_typed_instantiator<Mdp<storm::RationalFunction>, Mdp<ValueType>>(m, (prefix + "PMdpInstantiator").c_str(), "Instantiate PMDPs to MDPs");
    define_typed_instantiator<Ctmc<storm::RationalFunction>, Ctmc<ValueType>>(m, (prefix + "PCtmcInstantiator").c_str(), "Instantiate PCTMCs to CTMCs");
    define_typed_instantiator<MarkovAutomaton<storm::RationalFunction>, MarkovAutomaton<ValueType>>(m, (prefix + "PMaInstantiator").c_str(),
                                                                                                    "Instantiate PMAs to MAs");
}

// Trait: maps (ModelType, ResultType) to the specific checker class
template<typename, typename>
struct instantiation_checker;

template<typename ResultType>
struct instantiation_checker<Dtmc<storm::RationalFunction>, ResultType> {
    using type = SparseDtmcInstantiationModelChecker<Dtmc<storm::RationalFunction>, ResultType>;
};

template<typename ResultType>
struct instantiation_checker<Mdp<storm::RationalFunction>, ResultType> {
    using type = SparseMdpInstantiationModelChecker<Mdp<storm::RationalFunction>, ResultType>;
};

template<typename ResultType>
struct instantiation_checker<Ctmc<storm::RationalFunction>, ResultType> {
    using type = SparseCtmcInstantiationModelChecker<Ctmc<storm::RationalFunction>, ResultType>;
};

// Helper: define typed base + derived instantiation checker pair
template<typename ModelType, typename ResultType>
void define_typed_checker(py::module& m, const char* baseName, const char* baseDesc, const char* derivedName, const char* derivedDesc) {
    using CheckerType = typename instantiation_checker<ModelType, ResultType>::type;
    using BaseChecker = SparseInstantiationModelChecker<ModelType, ResultType>;
    auto base = py::classh<BaseChecker>(m, baseName, baseDesc);
    base.def("specify_formula", &BaseChecker::specifyFormula, "check_task"_a);

    py::classh<CheckerType>(m, derivedName, derivedDesc, base)
        .def(py::init<ModelType>(), "parametric model"_a)
        .def(
            "check",
            [](CheckerType& c, storm::Environment const& env,
               storm::utility::parametric::Valuation<storm::RationalFunction> const& val) -> std::shared_ptr<CheckResult> { return c.check(env, val); },
            "env"_a, "instantiation"_a)
        .def("set_graph_preserving", &CheckerType::setInstantiationsAreGraphPreserving, "value"_a);
}

template<typename ValueType>
void define_model_instantiation_checker(py::module& m) {
    std::string exactStr, exactDesc;
    if constexpr (std::is_same_v<ValueType, double>) {
        exactStr = "";
        exactDesc = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalNumber>) {
        exactStr = "Exact";
        exactDesc = "exact ";
    }

    // Dtmc
    define_typed_checker<Dtmc<storm::RationalFunction>, ValueType>(
        m, ("_PDtmc" + exactStr + "InstantiationCheckerBase").c_str(), ("Instantiate pDTMCs to " + exactDesc + "DTMCs and immediately check (base)").c_str(),
        ("PDtmc" + exactStr + "InstantiationChecker").c_str(), ("Instantiate pDTMCs to " + exactDesc + "DTMCs and immediately check").c_str());

    // Mdp
    define_typed_checker<Mdp<storm::RationalFunction>, ValueType>(
        m, ("_PMdp" + exactStr + "InstantiationCheckerBase").c_str(), ("Instantiate pMDPs to " + exactDesc + "MDPs and immediately check (base)").c_str(),
        ("PMdp" + exactStr + "InstantiationChecker").c_str(), ("Instantiate PMDP to " + exactDesc + "MDPs and immediately check").c_str());

    // Ctmc
    define_typed_checker<Ctmc<storm::RationalFunction>, ValueType>(
        m, ("_PCtmc" + exactStr + "InstantiationCheckerBase").c_str(), ("Instantiate pCTMCs to " + exactDesc + "CTMCs and immediately check (base)").c_str(),
        ("PCtmc" + exactStr + "InstantiationChecker").c_str(), ("Instantiate pCTMCs to " + exactDesc + "CTMCs and immediately check").c_str());
}

template void define_model_instantiator<double>(py::module&);
template void define_model_instantiator<storm::RationalFunction>(py::module&);
template void define_model_instantiation_checker<double>(py::module&);
template void define_model_instantiation_checker<storm::RationalNumber>(py::module&);
