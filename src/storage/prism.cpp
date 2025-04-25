#include "prism.h"
#include <storm/storage/prism/Program.h>
#include <boost/variant.hpp>
#include <boost/algorithm/string/join.hpp>
#include <random>
#include <optional>
#include "src/helpers.h"
#include <storm/storage/expressions/ExpressionManager.h>
#include <storm/storage/expressions/ExpressionEvaluator.h>
#include <storm/storage/jani/Model.h>
#include <storm/storage/jani/Property.h>
#include <storm/storage/prism/OverlappingGuardAnalyser.h>
#include <storm/generator/NextStateGenerator.h>
#include <storm/generator/Choice.h>
#include <storm/generator/StateBehavior.h>
#include <storm/generator/PrismNextStateGenerator.h>
#include "storm/exceptions/NotSupportedException.h"
#include "storm/exceptions/NotImplementedException.h"
#include <storm/storage/expressions/SimpleValuation.h>
#include "storm/exceptions/InvalidTypeException.h"
#include "storm/exceptions/InvalidStateException.h"
#include "storm/exceptions/InvalidAccessException.h"
#include <storm/utility/solver.h>
#include <storm/solver/SmtSolver.h>


using namespace storm::prism;

template <typename StateType, typename ValueType>
void define_stateGeneration(py::module& m);

void define_prism(py::module& m) {
    py::class_<storm::prism::Program, std::shared_ptr<storm::prism::Program>> program(m, "PrismProgram", "A Prism Program");
    program.def_property_readonly("constants", &Program::getConstants, "Get Program Constants")
            .def_property_readonly("global_boolean_variables", &Program::getGlobalBooleanVariables, "Retrieves the global boolean variables of the program")
            .def_property_readonly("global_integer_variables", &Program::getGlobalIntegerVariables, "Retrieves the global integer variables of the program")
            .def_property_readonly("variables", [](Program const& prog) {return prog.getAllExpressionVariables(true);}, "Retrieves all expression variables (including constants) of the program")
            .def("get_variables", &Program::getAllExpressionVariables, py::arg("include_constants") = true, "Get all expression variables (and constants) used by the program")
            .def_property_readonly("nr_modules", &storm::prism::Program::getNumberOfModules, "Number of modules")
            .def_property_readonly("modules", &storm::prism::Program::getModules, "Modules in the program")
            .def_property_readonly("model_type", &storm::prism::Program::getModelType, "Model type")
            .def_property_readonly("has_undefined_constants", &storm::prism::Program::hasUndefinedConstants, "Flag if program has undefined constants")
            .def_property_readonly("undefined_constants_are_graph_preserving", &storm::prism::Program::undefinedConstantsAreGraphPreserving, "Flag if the undefined constants do not change the graph structure")
            .def("get_undefined_constants", &Program::getUndefinedConstants, "Collect the undefined constants")
            .def("substitute_constants", &Program::substituteConstants, "Substitute constants within program")
            .def("substitute_formulas", &Program::substituteFormulas, "Substitute formulas within program")
            .def("define_constants", &Program::defineUndefinedConstants, "Define constants")
            .def("restrict_commands", &Program::restrictCommands, "Restrict commands")
            .def("simplify", &Program::simplify, "Simplify")
            .def("has_label", &Program::hasLabel, py::arg("name"))
            .def("substitute_nonstandard_predicates", &Program::substituteNonStandardPredicates, "Remove nonstandard predicates from the prism program")
            .def("used_constants",&Program::usedConstants, "Compute Used Constants")
            .def("label_unlabelled_commands", &Program::labelUnlabelledCommands, "Label unlabelled commands", py::arg("name_suggestions"))
            .def("replace_variable_initialization_by_init_expression", &Program::replaceVariableInitializationByInitExpression, "Replaces initializations from the individual variables to a init expression.")
            .def("replace_constant_by_variable", &Program::replaceConstantByVariable, py::arg("constant"), py::arg("lower_bound"), py::arg("upper_bound"), py::arg("observable") = true, "Operation to take a constant and make it into a global variable (ranging from lower to upper bound).")
            .def_property_readonly("has_initial_states_expression", &Program::hasInitialConstruct, "Is an initial states expression given.")
            .def_property_readonly("initial_states_expression", [](Program const& p) {return p.hasInitialConstruct() ? std::make_optional(p.getInitialStatesExpression()) : std::nullopt;}, "Get the initial states expression, or none, if none exists")
            .def("update_initial_states_expression", &Program::updateInitialStatesExpression, py::arg("new_expression"), "Replace initial expression. Can only be called if initial expression exists.")
            .def("has_constant", &Program::hasConstant, py::arg("name"))
            .def("get_constant", &Program::getConstant, py::arg("name"), "Requires that the program has a constant with this name")
            .def("has_reward_model", [](Program const& p, std::string const& name) {return p.hasRewardModel(name);},  py::arg("name"), "Is a reward model with the specified name defined?")
            .def_property_readonly("reward_models", &Program::getRewardModels, "The defined reward models")
            .def("get_module", [](Program const& prog, std::string const& name) {return prog.getModule(name);}, py::arg("module_name"))
            // TODO the following is a duplicate and should be deprecated.
            .def_property_readonly("is_deterministic_model", &Program::isDeterministicModel, "Does the program describe a deterministic model?")
            .def_property_readonly("expression_manager", &Program::getManager, "Get the expression manager for expressions in this program")
            .def("get_synchronizing_action_indices", &Program::getSynchronizingActionIndices, "Get the synchronizing action indices")
            .def("get_action_name", &Program::getActionName, py::arg("action_index"), "Get the action name for a given action index")
            .def("get_module_indices_by_action_index", &Program::getModuleIndicesByActionIndex, py::arg("action_index"), "get all modules that have a particular action index")
            .def_property_readonly("number_of_unlabeled_commands", &Program::getNumberOfUnlabeledCommands, "Gets the number of commands that are not labelled")
            .def("flatten", &Program::flattenModules, "Put program into a single module", py::arg("smt_factory")=std::shared_ptr<storm::utility::solver::SmtSolverFactory>(new storm::utility::solver::SmtSolverFactory()))
            .def("to_jani", [](storm::prism::Program const& program, std::vector<storm::jani::Property> const& properties, bool allVariablesGlobal, std::string suffix) {
                    return program.toJani(properties, allVariablesGlobal, suffix);
                }, "Transform to Jani program", py::arg("properties"), py::arg("all_variables_global") = true, py::arg("suffix") = "")
            .def("__str__", &streamToString<storm::prism::Program>)
            .def("get_label_expression", [](storm::prism::Program const& program, std::string const& label){
                return program.getLabelExpression(label);
            }, "Get the expression of the given label.", py::arg("label"))
            .def_property_readonly("labels", &Program::getLabels, "Get all labels in the program")
            ;

    py::class_<Module> module(m, "PrismModule", "A module in a Prism program");
    module.def_property_readonly("commands", [](Module const& module) {return module.getCommands();}, "Commands in the module")
            .def_property_readonly("name", &Module::getName, "Name of the module")
            .def_property_readonly("integer_variables", &Module::getIntegerVariables, "All integer Variables of this module")
            .def_property_readonly("boolean_variables", &Module::getBooleanVariables, "All boolean Variables of this module")
            .def("get_integer_variable", &Module::getIntegerVariable, py::arg("variable_name"))
            .def("get_boolean_variable", &Module::getBooleanVariable, py::arg("variable_name"))
            .def("get_command_indices_by_action_index", &Module::getCommandIndicesByActionIndex, py::arg("action_index"))
            .def("__str__", &streamToString<Module>)
            ;

    py::class_<Command> command(m, "PrismCommand", "A command in a Prism program");
    command.def_property_readonly("global_index", &Command::getGlobalIndex, "Get global index")
            .def_property_readonly("labeled", &Command::isLabeled, "Is the command labeled")
            .def_property_readonly("action_index", &Command::getActionIndex, "What is the action index of the command")
            .def_property_readonly("guard_expression", &Command::getGuardExpression, "Get guard expression")
            .def_property_readonly("is_labeled", &Command::isLabeled, "Retrieves whether the command possesses a synchronization label")
            .def_property_readonly("action_name", &Command::getActionName, "Retrieves the action name of this command")
            .def_property_readonly("updates", [](Command const& command) {
                    return command.getUpdates();
                }, "Updates in the command")
            .def("__str__", &streamToString<Command>)
            ;

    py::class_<Update> update(m, "PrismUpdate", "An update in a Prism command");
    update.def(py::init<uint_fast64_t, storm::expressions::Expression const&, std::vector<storm::prism::Assignment> const&>())
           .def_property_readonly("assignments", [](Update const& update) {
                    return update.getAssignments();
                }, "Assignments in the update")
           .def_property_readonly("probability_expression", &Update::getLikelihoodExpression, "The probability expression for this update")
           .def_property_readonly("global_index", &Update::getGlobalIndex, "Retrieves the global index of the update, that is, a unique index over all modules")
           .def("substitute", &Update::substitute, "Substitutes all identifiers in the update according to the given map")
           .def("simplify", &Update::simplify, "Simplifies the update in various ways (also removes identity assignments)")
           .def("get_assignment", &Update::getAssignment, py::arg("variable_name"), "Retrieves a reference to the assignment for the variable with the given name")
           .def("get_as_variable_to_expression_map", &Update::getAsVariableToExpressionMap, "Creates a mapping representation of this update")
           .def("__str__", &streamToString<Update>)
           ;

    py::class_<Assignment> assignment(m, "PrismAssignment", "An assignment in prism");
    assignment.def(py::init<storm::expressions::Variable const&, storm::expressions::Expression const&>())
            .def_property_readonly("variable", &Assignment::getVariable, "Variable that is updated")
            .def_property_readonly("expression", &Assignment::getExpression, "Expression for the update")
            .def("__str__", &streamToString<Assignment>)
            ;

    py::class_<Label> label(m, "PrismLabel", "A label in prism");
    label.def_property_readonly("name", &Label::getName);
    label.def_property_readonly("expression", &Label::getStatePredicateExpression);

    // PrismType
    py::enum_<storm::prism::Program::ModelType>(m, "PrismModelType", "Type of the prism model")
            .value("DTMC", storm::prism::Program::ModelType::DTMC)
            .value("CTMC", storm::prism::Program::ModelType::CTMC)
            .value("MDP", storm::prism::Program::ModelType::MDP)
            .value("CTMDP", storm::prism::Program::ModelType::CTMDP)
            .value("MA", storm::prism::Program::ModelType::MA)
            .value("POMDP", storm::prism::Program::ModelType::POMDP)
            .value("UNDEFINED", storm::prism::Program::ModelType::UNDEFINED)
            ;

    py::class_<Constant, std::shared_ptr<Constant>> constant(m, "PrismConstant", "A constant in a Prism program");
    constant.def_property_readonly("name", &Constant::getName, "Constant name")
            .def_property_readonly("defined", &Constant::isDefined, "Is the constant defined?")
            .def_property_readonly("type", &Constant::getType, "The type of the constant")
            .def_property_readonly("expression_variable", &Constant::getExpressionVariable, "Expression variable")
            .def_property_readonly("definition", &Constant::getExpression, "Defining expression")
            ;

    py::class_<Variable, std::shared_ptr<Variable>> variable(m, "PrismVariable", "A program variable in a Prism program");
    variable.def_property_readonly("name", &Variable::getName, "Variable name")
            .def_property_readonly("initial_value_expression", &Variable::getInitialValueExpression, "The expression represented the initial value of the variable")
            .def_property_readonly("expression_variable", &Variable::getExpressionVariable, "The expression variable corresponding to the variable")
            ;

    py::class_<IntegerVariable, std::shared_ptr<IntegerVariable>> integer_variable(m, "PrismIntegerVariable", variable, "A program integer variable in a Prism program");
    integer_variable.def_property_readonly("lower_bound_expression", &IntegerVariable::getLowerBoundExpression, "The the lower bound expression of this integer variable")
                    .def_property_readonly("upper_bound_expression", &IntegerVariable::getUpperBoundExpression, "The the upper bound expression of this integer variable")
                    .def("__str__", &streamToString<IntegerVariable>)
                    ;

    py::class_<BooleanVariable, std::shared_ptr<BooleanVariable>> boolean_variable(m, "PrismBooleanVariable", variable, "A program boolean variable in a Prism program");
    boolean_variable.def("__str__", &streamToString<BooleanVariable>);

    py::class_<RewardModel, std::shared_ptr<RewardModel>> rewardModel(m, "PrismRewardModel", "Reward declaration in prism");
    rewardModel.def_property_readonly("name", &RewardModel::getName, "get name of the reward model");

    //define_stateGeneration<uint32_t, storm::RationalNumber>(m);

    py::class_<OverlappingGuardAnalyser> oga(m, "OverlappingGuardAnalyser", "An SMT driven analysis for overlapping guards");
    oga.def(py::init<Program const&, std::shared_ptr<storm::utility::solver::SmtSolverFactory>&>(), py::arg("program"), py::arg("smt solver factory"));
    oga.def("has_module_with_inner_action_overlapping_guard", &OverlappingGuardAnalyser::hasModuleWithInnerActionOverlap);
}

class ValuationMapping {
    public:
    std::map<storm::expressions::Variable, bool> booleanValues;
    std::map<storm::expressions::Variable, int_fast64_t> integerValues;
    std::map<storm::expressions::Variable, double> rationalValues;

    ValuationMapping(storm::prism::Program const& program,
                     storm::expressions::SimpleValuation valuation) {
        auto const& variables = program.getManager().getVariables();
        for (auto const& variable : variables) {
            if (variable.hasBooleanType()) {
                booleanValues[variable] = valuation.getBooleanValue(variable);
            } else if (variable.hasIntegerType()) {
                integerValues[variable] = valuation.getIntegerValue(variable);
            } else if (variable.hasRationalType()) {
                rationalValues[variable] = valuation.getRationalValue(variable);
            } else {
                STORM_LOG_THROW(false, storm::exceptions::InvalidTypeException,
                        "Unexpected variable type.");
            }
        }
    }

    std::string toString() const {
        std::vector<std::string> strs;
        for (auto const& value : booleanValues) {
            std::stringstream sstr;
            sstr << value.first.getName() + "=";
            sstr << value.second;
            strs.push_back(sstr.str());
        }
        for (auto const& value : integerValues) {
            std::stringstream sstr;
            sstr << value.first.getName() + "=";
            sstr << value.second;
            strs.push_back(sstr.str());
        }
        for (auto const& value : rationalValues) {
            std::stringstream sstr;
            sstr << value.first.getName() + "=";
            sstr << value.second;
            strs.push_back(sstr.str());
        }
        return "[" + boost::join(strs, ",") + "]";
    }
};

template <typename StateType, typename ValueType>
class GeneratorChoice {
    public:
    typedef std::vector<uint_fast64_t> origins_type;
    typedef std::vector<std::pair<StateType, ValueType>> distribution_type;

    origins_type origins;
    distribution_type distribution;

    private:
    static origins_type getOriginsVector(storm::generator::Choice<ValueType, StateType> &choice) {
        auto originsSet = boost::any_cast<storm::storage::FlatSet<uint_fast64_t>>(&choice.getOriginData());
        if (originsSet != nullptr) {
          return origins_type(originsSet->begin(), originsSet->end());
        } else {
          STORM_LOG_THROW(false, storm::exceptions::NotImplementedException,
                          "Type of choice origin data (aka "
                              << choice.getOriginData().type().name()
                              << ") is not implemented.");
        }
    }

    public:
    GeneratorChoice(storm::generator::Choice<ValueType, StateType> &choice) : origins(getOriginsVector(choice)), distribution(choice.begin(), choice.end()) {}
};

template <typename StateType, typename ValueType>
class StateGenerator {
    public:
    typedef std::unordered_map<StateType, storm::generator::CompressedState> IdToStateMap;
    typedef std::vector<GeneratorChoice<StateType, ValueType>> choice_list_type;

    private:
    storm::prism::Program const& program;
    storm::generator::PrismNextStateGenerator<ValueType, StateType> generator;
    std::function<StateType (storm::generator::CompressedState const&)> stateToIdCallback;
    // this needs to be below the generator attribute,
    // because its initialization depends on the generator being initialized.
    // #justcppthings
    storm::storage::sparse::StateStorage<StateType> stateStorage;
    bool hasComputedInitialStates = false;
    IdToStateMap stateMap;
    boost::optional<StateType> currentStateIndex;

    static storm::generator::NextStateGeneratorOptions makeNextStateGeneratorOptions() {
        storm::generator::NextStateGeneratorOptions options;
        options.setBuildChoiceOrigins(true);
        return options;
    }

    public:
        StateGenerator(storm::prism::Program const& program_) : program(program_), generator(program_, StateGenerator<StateType, ValueType>::makeNextStateGeneratorOptions()), stateStorage(generator.getStateSize()) {
            stateToIdCallback = [this] (storm::generator::CompressedState const& state) -> StateType {
                StateType newIndex = stateStorage.getNumberOfStates();
                std::pair<StateType, std::size_t> indexBucketPair = stateStorage.stateToId.findOrAddAndGetBucket(state, newIndex);
                StateType index = indexBucketPair.first;
                stateMap[index] = state;
                return index;
            };
        }

        StateType loadInitialState() {
            if (!hasComputedInitialStates) {
                stateStorage.initialStateIndices = generator.getInitialStates(stateToIdCallback);
                hasComputedInitialStates = true;
            }
            STORM_LOG_THROW(stateStorage.initialStateIndices.size() == 1, storm::exceptions::NotSupportedException, "Currently only models with one initial state are supported.");
            StateType initialStateIndex = stateStorage.initialStateIndices.front();
            load(initialStateIndex);
            return initialStateIndex;
        }

        void load(StateType stateIndex) {
            if (currentStateIndex && *currentStateIndex == stateIndex) {
                return;
            }
            auto search = stateMap.find(stateIndex);
            if (search == stateMap.end()) {
                STORM_LOG_THROW(false, storm::exceptions::InvalidAccessException,
                        "state id not found");
            }
            generator.load(search->second);
            currentStateIndex = stateIndex;
        }

        ValuationMapping currentStateToValuation() {
            if (!currentStateIndex) {
                STORM_LOG_THROW(false, storm::exceptions::InvalidStateException,
                        "Initial state not initialized");
            }
            auto valuation = generator.toValuation(stateMap[*currentStateIndex]);
            return ValuationMapping(program, valuation);
        }

        bool satisfies(storm::expressions::Expression const& expression) {
            return generator.satisfies(expression);
        }

        storm::generator::StateBehavior<ValueType, StateType> expandBehavior() {
            if (!hasComputedInitialStates) {
                STORM_LOG_THROW(false, storm::exceptions::InvalidStateException,
                        "Initial state not initialized");
            }
            return generator.expand(stateToIdCallback);
        }

        choice_list_type expand() {
            auto behavior = expandBehavior();
            choice_list_type choices_result;
            for (auto choice : behavior.getChoices()) {
                choices_result.push_back(GeneratorChoice<StateType, ValueType>(choice));
            }

            return choices_result;
        }

        bool isTerminal() {
            if (!hasComputedInitialStates) {
                STORM_LOG_THROW(false, storm::exceptions::InvalidStateException,
                        "Initial state not initialized");
            }
            choice_list_type choices_result;
            auto behavior = generator.expand(stateToIdCallback);
            return behavior.getChoices().empty();
        }

};

std::map<uint32_t, std::pair<storm::RationalNumber, storm::RationalNumber>> simulate(storm::prism::Program const& program, uint64_t totalSamples, uint64_t maxSteps) {
    using StateType = uint32_t;
    using ValueType = double;

    StateGenerator<StateType, ValueType> generator(program);
    std::map<StateType, std::pair<storm::RationalNumber, storm::RationalNumber>> result;
    std::set<StateType> visited;
    auto goal = program.getLabelExpression("goal");

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    const auto addSample = [&result](StateType state, bool isGoal) {
        auto hitsVisits = result.count(state) != 0 ? result[state] : std::make_pair(0, 0);
        if (isGoal) hitsVisits.first++;
        hitsVisits.second++;
        result[state] = hitsVisits;
    };

    const auto sampleBehavior = [&gen, &dis](std::vector<storm::generator::Choice<ValueType, StateType>> const& choices) -> StateType {
        ValueType rnd = dis(gen);
        STORM_LOG_THROW(choices.size() == 1, storm::exceptions::InvalidStateException, "nondeterminism");
        auto choice = choices[0];
        for (auto entry : choice) {
            if (rnd <= entry.second) {
                return entry.first;
            }
            rnd -= entry.second;
        }
        STORM_LOG_THROW(false, storm::exceptions::InvalidStateException, "unreachable");
    };

    for (unsigned int i = 0; i <= totalSamples; i++) {
        StateType state = generator.loadInitialState();
        uint64_t steps = 0;
        bool hitGoal = false;
        visited.clear();

        while (steps <= maxSteps) {
            steps++;
            visited.insert(state);

            if (generator.satisfies(goal)) {
                addSample(state, true);
                break;
            }

            auto behavior = generator.expandBehavior();
            auto choices = behavior.getChoices();
            if (choices.empty()) {
                addSample(state, false);
                break;
            }

            state = sampleBehavior(choices);
        }
    }

    return result;
}

template <typename StateType, typename ValueType>
void define_stateGeneration(py::module& m) {
//    py::class_<ValuationMapping, std::shared_ptr<ValuationMapping>> valuation_mapping(m, "ValuationMapping", "A valuation mapping for a state consists of a mapping from variable to value for each of the three types.");
//    valuation_mapping
//        .def_readonly("boolean_values", &ValuationMapping::booleanValues)
//        .def_readonly("integer_values", &ValuationMapping::integerValues)
//        .def_readonly("rational_values", &ValuationMapping::rationalValues)
//        .def("__str__", &ValuationMapping::toString);
//
//    py::class_<GeneratorChoice<StateType, ValueType>,
//              std::shared_ptr<GeneratorChoice<StateType, ValueType>>>
//        generator_choice(m, "GeneratorChoice", R"doc(
//            Representation of a choice taken by the generator.
//
//            :ivar origins: A list of command ids that generated this choice.
//            :vartype origins: List[int]
//            :ivar distribution: The probability distribution of this choice.
//            :vartype distribution: List[Pair[StateId, Probability]]
//    )doc");
//    generator_choice
//        .def_readonly("origins", &GeneratorChoice<StateType, ValueType>::origins)
//        .def_readonly("distribution", &GeneratorChoice<StateType, ValueType>::distribution);
//
//    py::class_<StateGenerator<StateType, ValueType>, std::shared_ptr<StateGenerator<StateType, ValueType>>> state_generator(m, "StateGenerator", R"doc(
//        Interactively explore states using Storm's PrismNextStateGenerator.
//
//        :ivar program: A PRISM program.
//    )doc");
//    state_generator
//        .def(py::init<storm::prism::Program const&>())
//        .def("load_initial_state", &StateGenerator<StateType, ValueType>::loadInitialState, R"doc(
//            Loads the (unique) initial state.
//            Multiple initial states are not supported.
//
//            :rtype: the ID of the initial state.
//        )doc")
//        .def("load", &StateGenerator<StateType, ValueType>::load, R"doc(
//            :param state_id: The ID of the state to load.
//        )doc")
//        .def("current_state_to_valuation", &StateGenerator<StateType, ValueType>::currentStateToValuation, R"doc(
//            Return a valuation for the currently loaded state.
//
//            :rtype: stormpy.ValuationMapping
//        )doc")
//        .def("current_state_satisfies", &StateGenerator<StateType, ValueType>::satisfies, R"doc(
//            Check if the currently loaded state satisfies the given expression.
//
//            :param stormpy.Expression expression: The expression to check against.
//            :rtype: bool
//        )doc")
//        .def("expand", &StateGenerator<StateType, ValueType>::expand, R"doc(
//            Expand the currently loaded state and return its successors.
//
//            :rtype: [GeneratorChoice]
//        )doc");
//
//    m.def("simulate", &simulate);
}
