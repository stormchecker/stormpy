#include "result.h"
#include "storm/analysis/GraphConditions.h"
#include "storm/modelchecker/results/SymbolicQualitativeCheckResult.h"
#include "storm/modelchecker/results/SymbolicQuantitativeCheckResult.h"
#include "storm/modelchecker/results/HybridQuantitativeCheckResult.h"
#include "storm/modelchecker/results/ExplicitQuantitativeCheckResult.h"
#include "storm/modelchecker/results/ExplicitQualitativeCheckResult.h"
#include "storm/modelchecker/results/ExplicitParetoCurveCheckResult.h"

#include "storm/models/symbolic/StandardRewardModel.h"

template<typename ValueType>
std::shared_ptr<storm::modelchecker::QualitativeCheckResult> createFilterInitialStatesSparse(std::shared_ptr<storm::models::sparse::Model<ValueType>> model) {
    return std::make_unique<storm::modelchecker::ExplicitQualitativeCheckResult<ValueType>>(model->getInitialStates());
}

template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::modelchecker::QualitativeCheckResult> createFilterInitialStatesSymbolic(std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> model) {
   return std::make_unique<storm::modelchecker::SymbolicQualitativeCheckResult<DdType>>(model->getReachableStates(), model->getInitialStates());
}

template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::modelchecker::QualitativeCheckResult> createFilterSymbolic(std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> model, storm::expressions::Expression const& expr) {
    return std::make_unique<storm::modelchecker::SymbolicQualitativeCheckResult<DdType>>(model->getReachableStates(), model->getStates(expr));
}

// Define python bindings
void define_result(py::module& m) {

    // CheckResult
    py::class_<storm::modelchecker::CheckResult, std::shared_ptr<storm::modelchecker::CheckResult>> checkResult(m, "_CheckResult", "Base class for all modelchecking results");
    checkResult.def_property_readonly("_symbolic", &storm::modelchecker::CheckResult::isSymbolic, "Flag if result is symbolic")
               .def_property_readonly("_hybrid", &storm::modelchecker::CheckResult::isHybrid, "Flag if result is hybrid")
               .def_property_readonly("_quantitative", &storm::modelchecker::CheckResult::isQuantitative, "Flag if result is quantitative")
               .def_property_readonly("_qualitative", &storm::modelchecker::CheckResult::isQualitative, "Flag if result is qualitative")
               .def_property_readonly("_explicit_qualitative", &storm::modelchecker::CheckResult::isExplicitQualitativeCheckResult, "Flag if result is explicit qualitative")
               .def_property_readonly("_explicit_quantitative", &storm::modelchecker::CheckResult::isExplicitQuantitativeCheckResult, "Flag if result is explicit quantitative")
               .def_property_readonly("_symbolic_qualitative", &storm::modelchecker::CheckResult::isSymbolicQualitativeCheckResult, "Flag if result is symbolic qualitative")
               .def_property_readonly("_symbolic_quantitative", &storm::modelchecker::CheckResult::isSymbolicQuantitativeCheckResult, "Flag if result is symbolic quantitative")
               .def_property_readonly("_hybrid_quantitative", &storm::modelchecker::CheckResult::isHybridQuantitativeCheckResult, "Flag if result is hybrid quantitative")
               .def_property_readonly("_pareto_curve", &storm::modelchecker::CheckResult::isParetoCurveCheckResult, "Flag if result is a pareto curve")
               .def_property_readonly("result_for_all_states", &storm::modelchecker::CheckResult::isResultForAllStates, "Flag if result is for all states")
               .def_property_readonly("has_scheduler", &storm::modelchecker::CheckResult::hasScheduler, "Flag if a scheduler is present")   
               .def("as_explicit_qualitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQualitativeCheckResult<double>();
                   }, "Convert into explicit qualitative result")
               .def("as_explicit_exact_qualitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQualitativeCheckResult<storm::RationalNumber>();
                   }, "Convert into explicit qualitative result")
               .def("as_explicit_parametric_qualitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQualitativeCheckResult<storm::RationalFunction>();
                   }, "Convert into explicit qualitative result")
               .def("as_explicit_quantitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQuantitativeCheckResult<double>();
                   }, "Convert into explicit quantitative result")
               .def("as_explicit_exact_quantitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQuantitativeCheckResult<storm::RationalNumber>();
                   }, "Convert into explicit quantitative result")
               .def("as_explicit_parametric_quantitative", [](storm::modelchecker::CheckResult const& result) {
                       return result.asExplicitQuantitativeCheckResult<storm::RationalFunction>();
                   }, "Convert into explicit quantitative result")
               .def("filter", &storm::modelchecker::CheckResult::filter, py::arg("filter"), "Filter the result")
               .def("__str__",  [](storm::modelchecker::CheckResult const& result) {
                       std::stringstream stream;
                       result.writeToStream(stream);
                       return stream.str();
                   })
    ;

    // QualitativeCheckResult
    py::class_<storm::modelchecker::QualitativeCheckResult, std::shared_ptr<storm::modelchecker::QualitativeCheckResult>> qualitativeCheckResult(m, "_QualitativeCheckResult", "Abstract class for qualitative model checking results", checkResult);

    py::class_<storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>, std::shared_ptr<storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>>>(m, "SymbolicQualitativeCheckResult", "Symbolic qualitative model checking result", qualitativeCheckResult)
            .def("get_truth_values", &storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>::getTruthValuesVector, "Get Dd representing the truth values")
    ;
}


template<typename ValueType>
void define_typed_result(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::modelchecker::ExplicitQualitativeCheckResult<ValueType>, std::shared_ptr<storm::modelchecker::ExplicitQualitativeCheckResult<ValueType>>, storm::modelchecker::QualitativeCheckResult>(m, ("Explicit" + vtSuffix + "QualitativeCheckResult").c_str(), "Explicit qualitative model checking result")
        .def("at", [](storm::modelchecker::ExplicitQualitativeCheckResult<ValueType> const& result, storm::storage::sparse::state_type state) {
                return result[state];
            }, py::arg("state"), "Get result for given state")
        .def("get_truth_values", &storm::modelchecker::ExplicitQualitativeCheckResult<ValueType>::getTruthValuesVector, "Get BitVector representing the truth values")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQualitativeCheckResult<ValueType> const& res) {return res.getScheduler();}, "Get scheduler")
    ;

    py::class_<storm::modelchecker::QuantitativeCheckResult<ValueType>, std::shared_ptr<storm::modelchecker::QuantitativeCheckResult<ValueType>>, storm::modelchecker::CheckResult> quantitativeCheckResult(m, ("_" + vtSuffix + "QuantitativeCheckResult").c_str(), "Abstract class for quantitative model checking results");
    quantitativeCheckResult.def_property_readonly("min", &storm::modelchecker::QuantitativeCheckResult<ValueType>::getMin, "Minimal value")
        .def_property_readonly("max", &storm::modelchecker::QuantitativeCheckResult<ValueType>::getMax, "Maximal value")
    ;

    py::class_<storm::modelchecker::ExplicitQuantitativeCheckResult<ValueType>, std::shared_ptr<storm::modelchecker::ExplicitQuantitativeCheckResult<ValueType>>>(m, ("Explicit" + vtSuffix + "QuantitativeCheckResult").c_str(), "Explicit quantitative model checking result", quantitativeCheckResult)
        .def(py::init<std::vector<ValueType>>(), py::arg("values"))
        .def("at", [](storm::modelchecker::ExplicitQuantitativeCheckResult<ValueType> const& result, storm::storage::sparse::state_type state) {
            return result[state];
        }, py::arg("state"), "Get result for given state")
        .def("get_values", [](storm::modelchecker::ExplicitQuantitativeCheckResult<ValueType> const& res) {return res.getValueVector();}, "Get model checking result values for all states")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQuantitativeCheckResult<ValueType> const& res) {return res.getScheduler();}, "get scheduler")
    ;

    py::class_<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>, std::shared_ptr<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>>>(m, ("Symbolic" + vtSuffix + "QuantitativeCheckResult").c_str(), "Symbolic quantitative model checking result", quantitativeCheckResult)
            .def("clone", [](storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType> const& dd)  {return dd.clone()->template asSymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>(); })
            .def("get_values", &storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>::getValueVector)
    ;

    py::class_<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>, std::shared_ptr<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>>>(m, ("Hybrid" + vtSuffix + "QuantitativeCheckResult").c_str(), "Hybrid quantitative model checking result", quantitativeCheckResult)
        .def("get_values", &storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, ValueType>::getExplicitValueVector, "Get model checking result values for all states")
    ;

    if constexpr (std::is_same_v<ValueType, double> || std::is_same_v<ValueType, storm::RationalNumber> ) {
        py::class_<storm::modelchecker::ParetoCurveCheckResult<ValueType>, std::shared_ptr<storm::modelchecker::ParetoCurveCheckResult<ValueType>>, storm::modelchecker::CheckResult> pccheckresult(m, (vtSuffix + "ParetoCurveCheckResult").c_str(), "Result for multiobjective model checking");
        pccheckresult.def("get_underapproximation", &storm::modelchecker::ParetoCurveCheckResult<ValueType>::getUnderApproximation)
            .def("get_overapproximation", &storm::modelchecker::ParetoCurveCheckResult<ValueType>::getOverApproximation)
        ;

        py::class_<storm::modelchecker::ExplicitParetoCurveCheckResult<ValueType>, std::shared_ptr<storm::modelchecker::ExplicitParetoCurveCheckResult<ValueType>>> epccheckresult(m, ("Explicit" + vtSuffix + "ParetoCurveCheckResult").c_str(), "Result for explicit multiobjective model checking", pccheckresult)
        ;

        m.def(("create_filter_symbolic" + vtSuffix).c_str(), &createFilterSymbolic<storm::dd::DdType::Sylvan, ValueType>, "Creates a filter for the given states and a symbolic model", py::arg("model"), py::arg("states"));
        m.def(("create_filter_initial_states_sparse" + vtSuffix).c_str(), &createFilterInitialStatesSparse<ValueType>, "Create a filter for the initial states on a sparse model", py::arg("model"));
        m.def(("create_filter_initial_states_symbolic" + vtSuffix).c_str(), &createFilterInitialStatesSymbolic<storm::dd::DdType::Sylvan, ValueType>, "Create a filter for the initial states on a symbolic model", py::arg("model"));
    }
}

template void define_typed_result<double>(py::module& m, std::string const& vtSuffix);
template void define_typed_result<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
template void define_typed_result<storm::RationalFunction>(py::module& m, std::string const& vtSuffix);
