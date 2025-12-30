#include <vector>
#include "expressions.h"
#include "src/helpers.h"

#include "storm/adapters/IntervalAdapter.h"
#include "storm/storage/expressions/ExpressionManager.h"
#include "storm/storage/expressions/Expression.h"
#include "storm/storage/expressions/Valuation.h"
#include "storm/storage/expressions/OperatorType.h"
#include "storm-parsers/parser/ExpressionParser.h"
#include "storm/storage/expressions/ToDiceStringVisitor.h"

//Define python bindings
void define_expressions(py::module& m) {
    using Expression = storm::expressions::Expression;
    using Variable = storm::expressions::Variable;
    using Valuation = storm::expressions::Valuation;

    // ExpressionManager
    py::class_<storm::expressions::ExpressionManager, std::shared_ptr<storm::expressions::ExpressionManager>>(m, "ExpressionManager", "Manages variables for expressions")
        .def(py::init(), "Constructor")
        .def("create_boolean", &storm::expressions::ExpressionManager::boolean, py::arg("boolean"), "Create expression from boolean")
        .def("create_integer", &storm::expressions::ExpressionManager::integer, py::arg("integer"), "Create expression from integer number")
        .def("create_rational", [](storm::expressions::ExpressionManager const& manager, storm::RationalNumber number) {
                return manager.rational(number);
            }, py::arg("rational"), "Create expression from rational number")
        .def("create_boolean_variable", &storm::expressions::ExpressionManager::declareBooleanVariable, "create Boolean variable", py::arg("name"), py::arg("auxiliary") = false)
        .def("create_integer_variable", &storm::expressions::ExpressionManager::declareIntegerVariable, "create Integer variable", py::arg("name"), py::arg("auxiliary") = false)
        .def("create_rational_variable", &storm::expressions::ExpressionManager::declareRationalVariable, "create Rational variable", py::arg("name"), py::arg("auxiliary") = false)
        .def("get_variable", &storm::expressions::ExpressionManager::getVariable, "get variably by name", py::arg("name"))
        .def("get_variables", &storm::expressions::ExpressionManager::getVariables, "Retrieves the set of all variables known to this manager.")
            ;

    // Variable
    py::class_<storm::expressions::Variable, std::shared_ptr<storm::expressions::Variable>>(m, "Variable", "Represents a variable")
        .def_property_readonly("name", &storm::expressions::Variable::getName, "Variable name")
        .def_property_readonly("manager", &storm::expressions::Variable::getManager, "Variable manager")
        .def_property_readonly("index", &storm::expressions::Variable::getIndex, "Variable index")
        .def_property_readonly("offset", &storm::expressions::Variable::getOffset, "Variable offset (used e.g., in dds)")
        .def("has_boolean_type", &storm::expressions::Variable::hasBooleanType, "Check if the variable is of boolean type")
        .def("has_integer_type", &storm::expressions::Variable::hasIntegerType, "Check if the variable is of integer type")
        .def("has_rational_type", &storm::expressions::Variable::hasRationalType, "Check if the variable is of rational type")
        .def("has_numerical_type", &storm::expressions::Variable::hasNumericalType, "Check if the variable is of numerical type")
        .def("has_bitvector_type", &storm::expressions::Variable::hasBitVectorType, "Check if the variable is of bitvector type")
        .def("get_expression", &storm::expressions::Variable::getExpression, "Get expression from variable")
        .def("__eq__", &storm::expressions::Variable::operator==)
        .def("__hash__", &storm::expressions::Variable::getIndex)
    ;




    py::enum_<storm::expressions::OperatorType>(m, "OperatorType", "Type of an operator (of any sort)")
            .value("And", storm::expressions::OperatorType::And)
            .value("Or", storm::expressions::OperatorType::Or)
            .value("Xor", storm::expressions::OperatorType::Xor)
            .value("Implies", storm::expressions::OperatorType::Implies)
            .value("Iff", storm::expressions::OperatorType::Iff)
            .value("Plus", storm::expressions::OperatorType::Plus)
            .value("Minus", storm::expressions::OperatorType::Minus)
            .value("Times", storm::expressions::OperatorType::Times)
            .value("Divide", storm::expressions::OperatorType::Divide)
            .value("Min", storm::expressions::OperatorType::Min)
            .value("Max", storm::expressions::OperatorType::Max)
            .value("Power", storm::expressions::OperatorType::Power)
            .value("Modulo", storm::expressions::OperatorType::Modulo)
            .value("Equal", storm::expressions::OperatorType::Equal)
            .value("NotEqual", storm::expressions::OperatorType::NotEqual)
            .value("Less", storm::expressions::OperatorType::Less)
            .value("LessOrEqual", storm::expressions::OperatorType::LessOrEqual)
            .value("Greater", storm::expressions::OperatorType::Greater)
            .value("GreaterOrEqual", storm::expressions::OperatorType::GreaterOrEqual)
            .value("Not", storm::expressions::OperatorType::Not)
            .value("Floor", storm::expressions::OperatorType::Floor)
            .value("Ceil", storm::expressions::OperatorType::Ceil)
            .value("Ite", storm::expressions::OperatorType::Ite)
            ;


    // Expression
    py::class_<storm::expressions::Expression, std::shared_ptr<storm::expressions::Expression>> expression(m, "Expression", "Holds an expression");
    expression.def(py::init<Expression>(), "other_expression"_a)
        .def("contains_variables", &storm::expressions::Expression::containsVariables, "Check if the expression contains variables.")
        .def("contains_variable", &storm::expressions::Expression::containsVariable, "Check if the expression contains any of the given variables.", py::arg("variables"))
        .def("get_variables" , &storm::expressions::Expression::getVariables, "Get the variables")
            .def("is_literal", &storm::expressions::Expression::isLiteral, "Check if the expression is a literal")
            .def("is_variable", &storm::expressions::Expression::isVariable, "Check if the expression is a variable")
            .def("identifier", &storm::expressions::Expression::getIdentifier, "Retrieves the identifier associated with this expression if this expression is a variable")
        .def("has_boolean_type", &storm::expressions::Expression::hasBooleanType, "Check if the expression is a boolean")
        .def("has_integer_type", &storm::expressions::Expression::hasIntegerType, "Check if the expression is an integer")
        .def("has_rational_type", &storm::expressions::Expression::hasRationalType, "Check if the expression is a rational")
        .def_property_readonly("type", &storm::expressions::Expression::getType, "Get the Type")
        .def_property_readonly("manager", &storm::expressions::Expression::getManager, "Get the manager")
        .def("simplify", &storm::expressions::Expression::simplify, "Simplify expression")
        .def("substitute", [](Expression const& expr, std::map<Variable, Expression> const& map) { return expr.substitute(map);}, "substitution_map"_a)
        .def("evaluate_as_int", [](Expression const& expr)
                                {return expr.evaluateAsInt();}, "Get the integer value this expression evaluates to")
        .def("evaluate_as_bool", [](Expression const& expr)
            {return expr.evaluateAsBool();}, "Get the boolean value this expression evaluates to")
        .def("evaluate_as_double", [](Expression const& expr)
            {return expr.evaluateAsDouble();}, "Get the double value this expression evaluates to")
            .def("evaluate_as_rational", [](Expression const& expr)
            {return expr.evaluateAsRational();}, "Get the rational number this expression evaluates to")
        .def("__str__", &storm::expressions::Expression::toString, "To string")
        .def_property_readonly("is_function_application", &storm::expressions::Expression::isFunctionApplication, "True iff the expression is a function application (of any sort")
        .def_property_readonly("operator", &storm::expressions::Expression::getOperator, "The operator of the expression (if it is a function application)")
        .def_property_readonly("arity", &storm::expressions::Expression::getArity, "The arity of the expression")
        .def("get_operand", &storm::expressions::Expression::getOperand
                , "Get the operand at the given index", py::arg("operandIndex"))

        .def_static("Plus", [](Expression const& lhs, Expression const& rhs) {return lhs + rhs;})
        .def_static("Minus", [](Expression const& lhs, Expression const& rhs) {return lhs - rhs;})
        .def_static("Multiply", [](Expression const& lhs, Expression const& rhs) {return lhs * rhs;})
        .def_static("Divide", [](Expression const& lhs, Expression const& rhs) {return lhs / rhs;})
        .def_static("And", [](Expression const& lhs, Expression const& rhs) {return lhs && rhs;})
        .def_static("Or", [](Expression const& lhs, Expression const& rhs) {return lhs || rhs;})
        .def_static("Geq", [](Expression const& lhs, Expression const& rhs) {return lhs >= rhs;})
        .def_static("Eq", [](Expression const& lhs, Expression const& rhs) {return lhs == rhs;})
        .def_static("Neq", [](Expression const& lhs, Expression const& rhs) {return lhs != rhs;})
        .def_static("Greater", [](Expression const& lhs, Expression const& rhs) {return lhs > rhs;})
        .def_static("Less", [](Expression const& lhs, Expression const& rhs) {return lhs < rhs;})
        .def_static("Leq", [](Expression const& lhs, Expression const& rhs) {return lhs <= rhs;})
        .def_static("Modulo", [](Expression const& lhs, Expression const& rhs) {return storm::expressions::modulo(lhs, rhs);})
        .def_static("Implies", [](Expression const& lhs, Expression const& rhs) {return storm::expressions::implies(lhs, rhs);})
        .def_static("Iff", [](Expression const& lhs, Expression const& rhs) {return storm::expressions::iff(lhs, rhs);})
        .def_static("Conjunction", [](std::vector<Expression> const& expr) {return storm::expressions::conjunction(expr); })
        .def_static("Disjunction", [](std::vector<Expression> const& expr) {return storm::expressions::disjunction(expr); })
            ;


    py::class_<storm::parser::ExpressionParser>(m, "ExpressionParser", "Parser for storm-expressions")
            .def(py::init<storm::expressions::ExpressionManager const&>(), "Expression Manager to use", py::arg("expression_manager"))
            .def("set_identifier_mapping", [](storm::parser::ExpressionParser& p, std::unordered_map<std::string, storm::expressions::Expression> const& identifierMapping) {p.setIdentifierMapping(identifierMapping);}, "sets identifiers")
            .def("parse", &storm::parser::ExpressionParser::parseFromString, py::arg("string"), py::arg("ignore_error") = false, "parse")
            ;

    py::class_<storm::expressions::Type>(m, "ExpressionType", "The type of an expression")
            .def_property_readonly("is_boolean", &storm::expressions::Type::isBooleanType)
            .def_property_readonly("is_integer", &storm::expressions::Type::isIntegerType)
            .def_property_readonly("is_rational", &storm::expressions::Type::isRationalType)
            .def("__str__", &storm::expressions::Type::getStringRepresentation);

    py::class_<storm::expressions::ToDiceStringVisitor>(m, "DiceStringVisitor", "Translate expressions to dice")
            .def(py::init<uint64_t>(), py::arg("nr_bits"))
            .def("to_string", [](storm::expressions::ToDiceStringVisitor& visitor, storm::expressions::Expression const& expr) { return visitor.toString(expr);});

}
