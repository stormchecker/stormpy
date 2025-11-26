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
    return std::make_unique<storm::modelchecker::ExplicitQualitativeCheckResult>(model->getInitialStates());
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
                return result.asExplicitQualitativeCheckResult();
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
    py::class_<storm::modelchecker::ExplicitQualitativeCheckResult, std::shared_ptr<storm::modelchecker::ExplicitQualitativeCheckResult>>(m, "ExplicitQualitativeCheckResult", "Explicit qualitative model checking result", qualitativeCheckResult)
        .def("at", [](storm::modelchecker::ExplicitQualitativeCheckResult const& result, storm::storage::sparse::state_type state) {
                return result[state];
            }, py::arg("state"), "Get result for given state")
        .def("get_truth_values", &storm::modelchecker::ExplicitQualitativeCheckResult::getTruthValuesVector, "Get BitVector representing the truth values")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQualitativeCheckResult const& res) {return res.getScheduler();}, "get scheduler")

    ;
    py::class_<storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>, std::shared_ptr<storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>>>(m, "SymbolicQualitativeCheckResult", "Symbolic qualitative model checking result", qualitativeCheckResult)
            .def("get_truth_values", &storm::modelchecker::SymbolicQualitativeCheckResult<storm::dd::DdType::Sylvan>::getTruthValuesVector, "Get Dd representing the truth values")
    ;

    // QuantitativeCheckResult
    py::class_<storm::modelchecker::QuantitativeCheckResult<double>, std::shared_ptr<storm::modelchecker::QuantitativeCheckResult<double>>> quantitativeCheckResult(m, "_QuantitativeCheckResult", "Abstract class for quantitative model checking results", checkResult);
    quantitativeCheckResult.def_property_readonly("min", &storm::modelchecker::QuantitativeCheckResult<double>::getMin, "Minimal value")
        .def_property_readonly("max", &storm::modelchecker::QuantitativeCheckResult<double>::getMax, "Maximal value")
    ;

    py::class_<storm::modelchecker::ExplicitQuantitativeCheckResult<double>, std::shared_ptr<storm::modelchecker::ExplicitQuantitativeCheckResult<double>>>(m, "ExplicitQuantitativeCheckResult", "Explicit quantitative model checking result", quantitativeCheckResult)
        .def(py::init<std::vector<double>>(), py::arg("values"))
        .def("at", [](storm::modelchecker::ExplicitQuantitativeCheckResult<double> const& result, storm::storage::sparse::state_type state) {
            return result[state];
        }, py::arg("state"), "Get result for given state")
        .def("get_values", [](storm::modelchecker::ExplicitQuantitativeCheckResult<double> const& res) {return res.getValueVector();}, "Get model checking result values for all states")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQuantitativeCheckResult<double> const& res) {return res.getScheduler();}, "get scheduler")
    ;
    py::class_<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>, std::shared_ptr<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>>>(m, "SymbolicQuantitativeCheckResult", "Symbolic quantitative model checking result", quantitativeCheckResult)
            .def("clone", [](storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, double> const& dd)  {return dd.clone()->asSymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>(); })
            .def("get_values", &storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>::getValueVector);
            ;
    py::class_<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>, std::shared_ptr<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>>>(m, "HybridQuantitativeCheckResult", "Hybrid quantitative model checking result", quantitativeCheckResult)
        .def("get_values", &storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, double>::getExplicitValueVector, "Get model checking result values for all states")
    ;

    py::class_<storm::modelchecker::QuantitativeCheckResult<storm::RationalNumber>, std::shared_ptr<storm::modelchecker::QuantitativeCheckResult<storm::RationalNumber>>> exactQuantitativeCheckResult(m, "_ExactQuantitativeCheckResult", "Abstract class for exact quantitative model checking results", checkResult);
    py::class_<storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalNumber>, std::shared_ptr<storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalNumber>>>(m, "ExplicitExactQuantitativeCheckResult", "Explicit exact quantitative model checking result", exactQuantitativeCheckResult)
        .def(py::init<std::vector<storm::RationalNumber>>(), py::arg("values"))
        .def("at", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalNumber> const& result, storm::storage::sparse::state_type state) {
            return result[state];
        }, py::arg("state"), "Get result for given state")
        .def("get_values", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalNumber> const& res) { return res.getValueVector();}, "Get model checking result values for all states")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalNumber> const& res) {return res.getScheduler();}, "get scheduler")
    ;
    py::class_<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>, std::shared_ptr<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>>>(m, "SymbolicExactQuantitativeCheckResult", "Symbolic exact quantitative model checking result", quantitativeCheckResult)
       .def("clone", [](storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber> const& dd)  {return dd.clone()->asSymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>(); })
   ;
    py::class_<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>, std::shared_ptr<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>>>(m, "HybridExactQuantitativeCheckResult", "Symbolic exact hybrid quantitative model checking result", quantitativeCheckResult)
        .def("get_values", &storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalNumber>::getExplicitValueVector, "Get model checking result values for all states")
    ;

    py::class_<storm::modelchecker::QuantitativeCheckResult<storm::RationalFunction>, std::shared_ptr<storm::modelchecker::QuantitativeCheckResult<storm::RationalFunction>>> parametricQuantitativeCheckResult(m, "_ParametricQuantitativeCheckResult", "Abstract class for parametric quantitative model checking results", checkResult);
    py::class_<storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalFunction>, std::shared_ptr<storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalFunction>>>(m, "ExplicitParametricQuantitativeCheckResult", "Explicit parametric quantitative model checking result", parametricQuantitativeCheckResult)
        .def("at", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalFunction> const& result, storm::storage::sparse::state_type state) {
            return result[state];
        }, py::arg("state"), "Get result for given state")
        .def("get_values", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalFunction> const& res) { return res.getValueVector();}, "Get model checking result values for all states")
        .def_property_readonly("scheduler", [](storm::modelchecker::ExplicitQuantitativeCheckResult<storm::RationalFunction> const& res) {return res.getScheduler();}, "get scheduler")
    ;
    py::class_<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>, std::shared_ptr<storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>>>(m, "SymbolicParametricQuantitativeCheckResult", "Symbolic parametric quantitative model checking result", quantitativeCheckResult)
         .def("clone", [](storm::modelchecker::SymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction> const& dd)  {return dd.clone()->asSymbolicQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>(); })
    ;
    py::class_<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>, std::shared_ptr<storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>>>(m, "HybridParametricQuantitativeCheckResult", "Symbolic parametric hybrid quantitative model checking result", quantitativeCheckResult)
        .def("get_values", &storm::modelchecker::HybridQuantitativeCheckResult<storm::dd::DdType::Sylvan, storm::RationalFunction>::getExplicitValueVector, "Get model checking result values for all states")
    ;

    py::class_<storm::modelchecker::ParetoCurveCheckResult<double>, std::shared_ptr<storm::modelchecker::ParetoCurveCheckResult<double>>> pccheckresult(m, "ParetoCurveCheckResultDouble", "Result for multiobjective model checking", checkResult);
    pccheckresult.def("get_underapproximation", &storm::modelchecker::ParetoCurveCheckResult<double>::getUnderApproximation);
    pccheckresult.def("get_overapproximation", &storm::modelchecker::ParetoCurveCheckResult<double>::getOverApproximation);

    py::class_<storm::modelchecker::ExplicitParetoCurveCheckResult<double>, std::shared_ptr<storm::modelchecker::ExplicitParetoCurveCheckResult<double>>> epccheckresult(m, "ExplicitParetoCurveCheckResultDouble", "Result for explicit multiobjective model checking", pccheckresult);


    m.def("create_filter_symbolic", &createFilterSymbolic<storm::dd::DdType::Sylvan, double>, "Creates a filter for the given states and a symbolic model", py::arg("model"), py::arg("states"));
    m.def("create_filter_initial_states_sparse", &createFilterInitialStatesSparse<double>, "Create a filter for the initial states on a sparse model", py::arg("model"));
    m.def("create_filter_initial_states_symbolic", &createFilterInitialStatesSymbolic<storm::dd::DdType::Sylvan, double>, "Create a filter for the initial states on a symbolic model", py::arg("model"));


}

