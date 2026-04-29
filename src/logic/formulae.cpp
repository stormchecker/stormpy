#include "formulae.h"
#include "storm/logic/Formulas.h"
#include "storm/logic/CloneVisitor.h"
#include "storm/logic/LabelSubstitutionVisitor.h"
#include "storm/storage/expressions/Variable.h"
#include "storm/adapters/RationalNumberAdapter.h"


void define_formulae(py::module& m) {

    py::enum_<storm::logic::ComparisonType>(m, "ComparisonType")
        .value("LESS", storm::logic::ComparisonType::Less)
        .value("LEQ", storm::logic::ComparisonType::LessEqual)
        .value("GREATER", storm::logic::ComparisonType::Greater)
        .value("GEQ", storm::logic::ComparisonType::GreaterEqual)
    ;


    py::enum_<storm::logic::BinaryBooleanOperatorType>(m, "BinaryBooleanOperatorType")
            .value("AND", storm::logic::BinaryBooleanOperatorType::And)
            .value("OR", storm::logic::BinaryBooleanOperatorType::Or);


    py::class_<storm::logic::Formula, std::shared_ptr<storm::logic::Formula>> formula(m, "Formula", "Generic Storm Formula");
    formula.def("__str__", &storm::logic::Formula::toString)
        .def("clone", [](storm::logic::Formula const& f) { storm::logic::CloneVisitor cv; return cv.clone(f);})
        .def("substitute", [](storm::logic::Formula const& f, std::map<storm::expressions::Variable, storm::expressions::Expression> const& map) { return f.substitute(map); }, "Substitute variables", py::arg("constants_map"))
        .def("substitute_labels_by_labels", [](storm::logic::Formula const& f, std::map<std::string, std::string> const& labelSubs) {storm::logic::LabelSubstitutionVisitor lsv(labelSubs); return lsv.substitute(f);}, "substitute label occurences", py::arg("replacements"))
        .def_property_readonly("is_probability_operator", &storm::logic::Formula::isProbabilityOperatorFormula, "is it a probability operator")
        .def_property_readonly("is_reward_operator", &storm::logic::Formula::isRewardOperatorFormula, "is it a reward operator")
        .def_property_readonly("is_eventually_formula", &storm::logic::Formula::isEventuallyFormula)
        .def_property_readonly("is_bounded_until_formula", &storm::logic::Formula::isBoundedUntilFormula)
        .def_property_readonly("is_until_formula", &storm::logic::Formula::isUntilFormula)
        .def_property_readonly("is_multi_objective_formula", &storm::logic::Formula::isMultiObjectiveFormula)
            ;

    // Path Formulae
    py::class_<storm::logic::PathFormula, std::shared_ptr<storm::logic::PathFormula>> pathFormula(m, "PathFormula", "Formula about the probability of a set of paths in an automaton", formula);
    py::class_<storm::logic::UnaryPathFormula, std::shared_ptr<storm::logic::UnaryPathFormula>> unaryPathFormula(m, "UnaryPathFormula", "Path formula with one operand", pathFormula);
    unaryPathFormula.def_property_readonly("subformula", &storm::logic::UnaryPathFormula::getSubformula, "the subformula");
    py::class_<storm::logic::EventuallyFormula, std::shared_ptr<storm::logic::EventuallyFormula>>(m, "EventuallyFormula", "Formula for eventually", unaryPathFormula)
    .def_property_readonly("subformula", &storm::logic::EventuallyFormula::getSubformula, "the subformula");
    py::class_<storm::logic::GloballyFormula, std::shared_ptr<storm::logic::GloballyFormula>>(m, "GloballyFormula", "Formula for globally", unaryPathFormula);
    py::class_<storm::logic::BinaryPathFormula, std::shared_ptr<storm::logic::BinaryPathFormula>> binaryPathFormula(m, "BinaryPathFormula", "Path formula with two operands", pathFormula);
    binaryPathFormula.def_property_readonly("left_subformula", &storm::logic::BinaryPathFormula::getLeftSubformula);
    binaryPathFormula.def_property_readonly("right_subformula", &storm::logic::BinaryPathFormula::getRightSubformula);
    py::class_<storm::logic::BoundedUntilFormula, std::shared_ptr<storm::logic::BoundedUntilFormula>>(m, "BoundedUntilFormula", "Until Formula with either a step or a time bound.", binaryPathFormula)
    .def_property_readonly("is_multidimensional", &storm::logic::BoundedUntilFormula::isMultiDimensional, "Is the bound multi-dimensional")
    .def_property_readonly("has_lower_bound", [](storm::logic::BoundedUntilFormula const& form) { return form.hasLowerBound(); })
    .def_property_readonly("upper_bound_expression", [](storm::logic::BoundedUntilFormula const& form) { return form.getUpperBound(); } )
    .def_property_readonly("left_subformula", [](storm::logic::BoundedUntilFormula const& form) -> storm::logic::Formula const& { return form.getLeftSubformula(); }, py::return_value_policy::reference_internal)
    .def_property_readonly("right_subformula", [](storm::logic::BoundedUntilFormula const& form)-> storm::logic::Formula const& { return form.getRightSubformula(); }, py::return_value_policy::reference_internal);
    py::class_<storm::logic::ConditionalFormula, std::shared_ptr<storm::logic::ConditionalFormula>>(m, "ConditionalFormula", "Formula with the right hand side being a condition.", formula)
    .def_property_readonly("main_subformula", &storm::logic::ConditionalFormula::getSubformula, "the subformula")
    .def_property_readonly("conditional_subformula", &storm::logic::ConditionalFormula::getConditionFormula, "the conditional subformula");
    py::class_<storm::logic::UntilFormula, std::shared_ptr<storm::logic::UntilFormula>>(m, "UntilFormula", "Path Formula for unbounded until", binaryPathFormula);

    // Reward Path Formulae
    //py::class_<storm::logic::RewardPathFormula, std::shared_ptr<storm::logic::RewardPathFormula>(m, "RewardPathFormula", "Formula about the rewards of a set of paths in an automaton", py::base<storm::logic::Formula>());
    py::class_<storm::logic::CumulativeRewardFormula, std::shared_ptr<storm::logic::CumulativeRewardFormula>>(m, "CumulativeRewardFormula", "Summed rewards over a the paths", pathFormula);
    py::class_<storm::logic::InstantaneousRewardFormula, std::shared_ptr<storm::logic::InstantaneousRewardFormula>>(m ,"InstantaneousRewardFormula", "Instantaneous reward", pathFormula);
    py::class_<storm::logic::LongRunAverageRewardFormula, std::shared_ptr<storm::logic::LongRunAverageRewardFormula>>(m, "LongRunAverageRewardFormula", "Long run average reward", pathFormula);
    //py::class_<storm::logic::ReachabilityRewardFormula, std::shared_ptr<storm::logic::ReachabilityRewardFormula>>(m, "ReachabilityRewardFormula", "Reachability reward", py::base<storm::logic::RewardPathFormula>());


    // State Formulae
    py::class_<storm::logic::StateFormula, std::shared_ptr<storm::logic::StateFormula>> stateFormula(m, "StateFormula", "Formula about a state of an automaton", formula);
    py::class_<storm::logic::AtomicExpressionFormula, std::shared_ptr<storm::logic::AtomicExpressionFormula>>(m, "AtomicExpressionFormula", "Formula with an atomic expression", stateFormula)
        .def("get_expression", &storm::logic::AtomicExpressionFormula::getExpression);
    py::class_<storm::logic::AtomicLabelFormula, std::shared_ptr<storm::logic::AtomicLabelFormula>>(m, "AtomicLabelFormula", "Formula with an atomic label", stateFormula)
        .def_property_readonly("label", &storm::logic::AtomicLabelFormula::getLabel, "label in the formula");
    py::class_<storm::logic::BooleanLiteralFormula, std::shared_ptr<storm::logic::BooleanLiteralFormula>>(m, "BooleanLiteralFormula", "Formula with a boolean literal", stateFormula)
            .def(py::init<bool>(),"truth value"_a);
    py::class_<storm::logic::UnaryStateFormula, std::shared_ptr<storm::logic::UnaryStateFormula>> unaryStateFormula(m, "UnaryStateFormula", "State formula with one operand", stateFormula);
    unaryStateFormula.def_property_readonly("subformula", &storm::logic::UnaryStateFormula::getSubformula, "the subformula");
    py::class_<storm::logic::UnaryBooleanStateFormula, std::shared_ptr<storm::logic::UnaryBooleanStateFormula>>(m, "UnaryBooleanStateFormula", "Unary boolean state formula", unaryStateFormula);
    py::class_<storm::logic::OperatorFormula, std::shared_ptr<storm::logic::OperatorFormula>> operatorFormula(m, "OperatorFormula", "Operator formula", unaryStateFormula);
    operatorFormula.def_property_readonly("has_bound", &storm::logic::OperatorFormula::hasBound, "Flag if formula is bounded")
        .def_property("comparison_type", &storm::logic::OperatorFormula::getComparisonType, &storm::logic::OperatorFormula::setComparisonType, "Comparison type of bound")
        .def_property_readonly("threshold", [](storm::logic::OperatorFormula const& f) {
            if (f.getThreshold().containsVariables()) {
                throw std::runtime_error("To obtain the threshold as an expression, use threshold_expr");
            }
            if (f.getThreshold().hasRationalType()) {
                return f.getThresholdAs<storm::RationalNumber>();
            } else if (f.getThreshold().hasIntegerType()) {
                return storm::utility::convertNumber<storm::RationalNumber>(f.getThreshold().evaluateAsInt());
            } else {
                throw std::runtime_error("Can't get non-rational threshold (not implemented)");
            }
        }, "Threshold of bound (currently only applicable to rational expressions)")
        .def_property_readonly("threshold_expr", [](storm::logic::OperatorFormula const& f) {
            return f.getThreshold();
        })
        .def("set_bound", [](storm::logic::OperatorFormula& f, storm::logic::ComparisonType comparisonType, storm::expressions::Expression const& bound) {
            f.setBound(storm::logic::Bound(comparisonType, bound));
        }, "Set bound", py::arg("comparison_type"), py::arg("bound"))
        .def("remove_bound", &storm::logic::OperatorFormula::removeBound)
        .def_property_readonly("has_optimality_type",  &storm::logic::OperatorFormula::hasOptimalityType, "Flag if an optimality type is present")
        .def_property_readonly("optimality_type", &storm::logic::OperatorFormula::getOptimalityType, "Flag for the optimality type")
        .def("set_optimality_type", &storm::logic::OperatorFormula::setOptimalityType, "set the optimality type (use remove optimiality type for clearing)", "new_optimality_type"_a)
        .def("remove_optimality_type", &storm::logic::OperatorFormula::removeOptimalityType, "remove the optimality type")

            ;
    py::class_<storm::logic::TimeOperatorFormula, std::shared_ptr<storm::logic::TimeOperatorFormula>>(m, "TimeOperator", "The time operator", operatorFormula);
    py::class_<storm::logic::LongRunAverageOperatorFormula, std::shared_ptr<storm::logic::LongRunAverageOperatorFormula>>(m, "LongRunAvarageOperator", "Long run average operator", operatorFormula);
    py::class_<storm::logic::ProbabilityOperatorFormula, std::shared_ptr<storm::logic::ProbabilityOperatorFormula>>(m, "ProbabilityOperator", "Probability operator", operatorFormula)
            .def(py::init<std::shared_ptr<storm::logic::Formula>>(), "construct probability operator formula", py::arg("subformula"))
    ;

    py::class_<storm::logic::RewardOperatorFormula, std::shared_ptr<storm::logic::RewardOperatorFormula>>(m, "RewardOperator", "Reward operator", operatorFormula)
            .def("has_reward_name", &storm::logic::RewardOperatorFormula::hasRewardModelName)
            .def_property_readonly("reward_name", &storm::logic::RewardOperatorFormula::getRewardModelName);
    py::class_<storm::logic::BinaryStateFormula, std::shared_ptr<storm::logic::BinaryStateFormula>> binaryStateFormula(m, "BinaryStateFormula", "State formula with two operands", stateFormula);
    py::class_<storm::logic::BinaryBooleanStateFormula, std::shared_ptr<storm::logic::BinaryBooleanStateFormula>>(m, "BooleanBinaryStateFormula", "Boolean binary state formula", binaryStateFormula);

    py::class_<storm::logic::MultiObjectiveFormula, std::shared_ptr<storm::logic::MultiObjectiveFormula>>(m, "MultiObjectiveFormula", "Multi objective formula", formula)
            .def_property_readonly("subformulas", &storm::logic::MultiObjectiveFormula::getSubformulas, "Get vector of subformulas")
            .def_property_readonly("nr_subformulas", &storm::logic::MultiObjectiveFormula::getNumberOfSubformulas, "Get number of subformulas");

    py::class_<storm::logic::GameFormula, std::shared_ptr<storm::logic::GameFormula>>(m, "GameFormula", "Game formula", unaryStateFormula)
            .def_property_readonly("is_game_formula", &storm::logic::GameFormula::isGameFormula, "is it a game formula");
}
