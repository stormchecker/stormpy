from __future__ import annotations
from stormpy.core import ActionMaskDouble
from stormpy.core import BisimulationType
from stormpy.core import BuilderOptions
from stormpy.core import CheckTask
from stormpy.core import ConstraintCollector
from stormpy.core import DirectEncodingOptions
from stormpy.core import DirectEncodingParserOptions
from stormpy.core import EliminationLabelBehavior
from stormpy.core import EndComponentEliminatorReturnTypeDouble
from stormpy.core import Environment
from stormpy.core import EquationSolverType
from stormpy.core import ExactCheckTask
from stormpy.core import ExplicitExactQuantitativeCheckResult
from stormpy.core import ExplicitModelBuilder
from stormpy.core import ExplicitModelCheckerHintDouble
from stormpy.core import ExplicitParametricModelBuilder
from stormpy.core import ExplicitParametricQuantitativeCheckResult
from stormpy.core import ExplicitParetoCurveCheckResultDouble
from stormpy.core import ExplicitQualitativeCheckResult
from stormpy.core import ExplicitQuantitativeCheckResult
from stormpy.core import ExplicitStateLookup
from stormpy.core import FlatSet
from stormpy.core import HybridExactQuantitativeCheckResult
from stormpy.core import HybridParametricQuantitativeCheckResult
from stormpy.core import HybridQuantitativeCheckResult
from stormpy.core import JaniModelType
from stormpy.core import MinMaxMethod
from stormpy.core import MinMaxSolverEnvironment
from stormpy.core import ModelCheckerHint
from stormpy.core import ModelFormulasPair
from stormpy.core import NativeLinearEquationSolverMethod
from stormpy.core import NativeSolverEnvironment
from stormpy.core import OptimizationDirection
from stormpy.core import ParametricCheckTask
from stormpy.core import ParetoCurveCheckResultDouble
from stormpy.core import Property
from stormpy.core import QuotientFormat
from stormpy.core import SMTCounterExampleGenerator
from stormpy.core import SMTCounterExampleGeneratorOptions
from stormpy.core import SMTCounterExampleGeneratorStats
from stormpy.core import SMTCounterExampleInput
from stormpy.core import SolverEnvironment
from stormpy.core import StateValuationFunctionActionMaskDouble
from stormpy.core import SubsystemBuilderOptions
from stormpy.core import SubsystemBuilderReturnTypeDouble
from stormpy.core import SubsystemBuilderReturnTypeExact
from stormpy.core import SubsystemBuilderReturnTypeRatFunc
from stormpy.core import SymbolicExactQuantitativeCheckResult
from stormpy.core import SymbolicModelDescription
from stormpy.core import SymbolicParametricQuantitativeCheckResult
from stormpy.core import SymbolicQualitativeCheckResult
from stormpy.core import SymbolicQuantitativeCheckResult
from stormpy.core import build_sparse_exact_model_with_options
from stormpy.core import build_sparse_model_from_explicit
from stormpy.core import build_sparse_model_with_options
from stormpy.core import build_sparse_parametric_model_with_options
from stormpy.core import check_interval_mdp
from stormpy.core import compute_all_until_probabilities
from stormpy.core import compute_transient_probabilities
from stormpy.core import create_filter_initial_states_sparse
from stormpy.core import create_filter_initial_states_symbolic
from stormpy.core import create_filter_symbolic
from stormpy.core import install_signal_handlers
from stormpy.core import make_sparse_model_builder
from stormpy.core import make_sparse_model_builder_exact
from stormpy.core import make_sparse_model_builder_parametric
from stormpy.core import parse_constants_string
from stormpy.core import parse_jani_model
from stormpy.core import parse_jani_model_from_string
from stormpy.core import parse_prism_program
from stormpy.core import parse_properties_for_jani_model
from stormpy.core import parse_properties_for_prism_program
from stormpy.core import parse_properties_without_context
from stormpy.core import preprocess_symbolic_input
from stormpy.core import reset_timeout
from stormpy.core import set_loglevel_debug
from stormpy.core import set_loglevel_error
from stormpy.core import set_loglevel_trace
from stormpy.core import set_settings
from stormpy.core import set_timeout
from stormpy.exceptions import StormError
from stormpy.logic import logic
from stormpy.logic.logic import AtomicExpressionFormula
from stormpy.logic.logic import AtomicLabelFormula
from stormpy.logic.logic import BinaryBooleanOperatorType
from stormpy.logic.logic import BinaryPathFormula
from stormpy.logic.logic import BinaryStateFormula
from stormpy.logic.logic import BooleanBinaryStateFormula
from stormpy.logic.logic import BooleanLiteralFormula
from stormpy.logic.logic import BoundedUntilFormula
from stormpy.logic.logic import ComparisonType
from stormpy.logic.logic import ConditionalFormula
from stormpy.logic.logic import CumulativeRewardFormula
from stormpy.logic.logic import EventuallyFormula
from stormpy.logic.logic import Formula
from stormpy.logic.logic import GameFormula
from stormpy.logic.logic import GloballyFormula
from stormpy.logic.logic import InstantaneousRewardFormula
from stormpy.logic.logic import LongRunAvarageOperator
from stormpy.logic.logic import LongRunAverageRewardFormula
from stormpy.logic.logic import MultiObjectiveFormula
from stormpy.logic.logic import OperatorFormula
from stormpy.logic.logic import PathFormula
from stormpy.logic.logic import ProbabilityOperator
from stormpy.logic.logic import RewardOperator
from stormpy.logic.logic import StateFormula
from stormpy.logic.logic import TimeOperator
from stormpy.logic.logic import UnaryBooleanStateFormula
from stormpy.logic.logic import UnaryPathFormula
from stormpy.logic.logic import UnaryStateFormula
from stormpy.logic.logic import UntilFormula
from stormpy.pycarl import cln
from stormpy.pycarl.cln import FactorizedPolynomial
from stormpy.pycarl.cln import FactorizedRationalFunction
from stormpy.pycarl.cln import Polynomial
from stormpy.pycarl.cln import Rational as RationalRF
from stormpy.pycarl.cln import RationalFunction
from stormpy.pycarl import gmp
from stormpy.pycarl.gmp import Rational
from stormpy.storage import build_parametric_sparse_matrix
from stormpy.storage import build_sparse_matrix
from stormpy.storage import get_maximal_end_components
from stormpy.storage import storage
from stormpy.storage.storage import AddIterator_Sylvan_Double
from stormpy.storage.storage import Add_Sylvan_Double
from stormpy.storage.storage import Bdd_Sylvan
from stormpy.storage.storage import BitVector
from stormpy.storage.storage import ChoiceLabeling
from stormpy.storage.storage import ChoiceOrigins
from stormpy.storage.storage import DdManager_Sylvan
from stormpy.storage.storage import DdMetaVariableType
from stormpy.storage.storage import DdMetaVariable_Sylvan
from stormpy.storage.storage import Dd_Sylvan
from stormpy.storage.storage import DiceStringVisitor
from stormpy.storage.storage import Distribution
from stormpy.storage.storage import DistributionExact
from stormpy.storage.storage import DistributionInterval
from stormpy.storage.storage import ExactSparseMatrix
from stormpy.storage.storage import ExactSparseMatrixBuilder
from stormpy.storage.storage import ExactSparseMatrixEntry
from stormpy.storage.storage import ExactSparseMatrixRows
from stormpy.storage.storage import Expression
from stormpy.storage.storage import ExpressionManager
from stormpy.storage.storage import ExpressionParser
from stormpy.storage.storage import ExpressionType
from stormpy.storage.storage import IntervalSparseMatrix
from stormpy.storage.storage import IntervalSparseMatrixBuilder
from stormpy.storage.storage import IntervalSparseMatrixEntry
from stormpy.storage.storage import IntervalSparseMatrixRows
from stormpy.storage.storage import ItemLabeling
from stormpy.storage.storage import JaniAssignment
from stormpy.storage.storage import JaniAutomaton
from stormpy.storage.storage import JaniChoiceOrigins
from stormpy.storage.storage import JaniConstant
from stormpy.storage.storage import JaniEdge
from stormpy.storage.storage import JaniEdgeDestination
from stormpy.storage.storage import JaniInformationObject
from stormpy.storage.storage import JaniLocation
from stormpy.storage.storage import JaniLocationExpander
from stormpy.storage.storage import JaniModel
from stormpy.storage.storage import JaniOrderedAssignments
from stormpy.storage.storage import JaniScopeChanger
from stormpy.storage.storage import JaniTemplateEdge
from stormpy.storage.storage import JaniTemplateEdgeDestination
from stormpy.storage.storage import JaniVariable
from stormpy.storage.storage import JaniVariableSet
from stormpy.storage.storage import MaximalEndComponent
from stormpy.storage.storage import MaximalEndComponentDecomposition_double
from stormpy.storage.storage import MaximalEndComponentDecomposition_exact
from stormpy.storage.storage import MaximalEndComponentDecomposition_interval
from stormpy.storage.storage import MaximalEndComponentDecomposition_ratfunc
from stormpy.storage.storage import ModelType
from stormpy.storage.storage import OperatorType
from stormpy.storage.storage import OverlappingGuardAnalyser
from stormpy.storage.storage import ParametricSparseMatrix
from stormpy.storage.storage import ParametricSparseMatrixBuilder
from stormpy.storage.storage import ParametricSparseMatrixEntry
from stormpy.storage.storage import ParametricSparseMatrixRows
from stormpy.storage.storage import PolytopeDouble
from stormpy.storage.storage import PolytopeExact
from stormpy.storage.storage import PrismAssignment
from stormpy.storage.storage import PrismBooleanVariable
from stormpy.storage.storage import PrismChoiceOrigins
from stormpy.storage.storage import PrismCommand
from stormpy.storage.storage import PrismConstant
from stormpy.storage.storage import PrismIntegerVariable
from stormpy.storage.storage import PrismLabel
from stormpy.storage.storage import PrismModelType
from stormpy.storage.storage import PrismModule
from stormpy.storage.storage import PrismProgram
from stormpy.storage.storage import PrismRewardModel
from stormpy.storage.storage import PrismUpdate
from stormpy.storage.storage import PrismVariable
from stormpy.storage.storage import Scheduler
from stormpy.storage.storage import SchedulerChoice
from stormpy.storage.storage import SchedulerChoiceExact
from stormpy.storage.storage import SchedulerChoiceInterval
from stormpy.storage.storage import SchedulerChoiceParametric
from stormpy.storage.storage import SchedulerExact
from stormpy.storage.storage import SchedulerInterval
from stormpy.storage.storage import SchedulerParametric
from stormpy.storage.storage import SimpleValuation
from stormpy.storage.storage import SparseCtmc
from stormpy.storage.storage import SparseDtmc
from stormpy.storage.storage import SparseExactCtmc
from stormpy.storage.storage import SparseExactDtmc
from stormpy.storage.storage import SparseExactMA
from stormpy.storage.storage import SparseExactMdp
from stormpy.storage.storage import SparseExactModelAction
from stormpy.storage.storage import SparseExactModelActions
from stormpy.storage.storage import SparseExactModelComponents
from stormpy.storage.storage import SparseExactModelState
from stormpy.storage.storage import SparseExactModelStates
from stormpy.storage.storage import SparseExactPomdp
from stormpy.storage.storage import SparseExactRewardModel
from stormpy.storage.storage import SparseExactSmg
from stormpy.storage.storage import SparseIntervalCtmc
from stormpy.storage.storage import SparseIntervalDtmc
from stormpy.storage.storage import SparseIntervalMA
from stormpy.storage.storage import SparseIntervalMdp
from stormpy.storage.storage import SparseIntervalModelAction
from stormpy.storage.storage import SparseIntervalModelActions
from stormpy.storage.storage import SparseIntervalModelComponents
from stormpy.storage.storage import SparseIntervalModelState
from stormpy.storage.storage import SparseIntervalModelStates
from stormpy.storage.storage import SparseIntervalPomdp
from stormpy.storage.storage import SparseIntervalRewardModel
from stormpy.storage.storage import SparseIntervalSmg
from stormpy.storage.storage import SparseMA
from stormpy.storage.storage import SparseMatrix
from stormpy.storage.storage import SparseMatrixBuilder
from stormpy.storage.storage import SparseMatrixEntry
from stormpy.storage.storage import SparseMatrixRows
from stormpy.storage.storage import SparseMdp
from stormpy.storage.storage import SparseModelAction
from stormpy.storage.storage import SparseModelActions
from stormpy.storage.storage import SparseModelComponents
from stormpy.storage.storage import SparseModelState
from stormpy.storage.storage import SparseModelStates
from stormpy.storage.storage import SparseParametricCtmc
from stormpy.storage.storage import SparseParametricDtmc
from stormpy.storage.storage import SparseParametricMA
from stormpy.storage.storage import SparseParametricMdp
from stormpy.storage.storage import SparseParametricModelAction
from stormpy.storage.storage import SparseParametricModelActions
from stormpy.storage.storage import SparseParametricModelComponents
from stormpy.storage.storage import SparseParametricModelState
from stormpy.storage.storage import SparseParametricModelStates
from stormpy.storage.storage import SparseParametricPomdp
from stormpy.storage.storage import SparseParametricRewardModel
from stormpy.storage.storage import SparsePomdp
from stormpy.storage.storage import SparseRewardModel
from stormpy.storage.storage import SparseSmg
from stormpy.storage.storage import StateLabeling
from stormpy.storage.storage import StateValuation
from stormpy.storage.storage import StateValuationsBuilder
from stormpy.storage.storage import SymbolicSylvanCtmc
from stormpy.storage.storage import SymbolicSylvanDtmc
from stormpy.storage.storage import SymbolicSylvanMA
from stormpy.storage.storage import SymbolicSylvanMdp
from stormpy.storage.storage import SymbolicSylvanParametricCtmc
from stormpy.storage.storage import SymbolicSylvanParametricDtmc
from stormpy.storage.storage import SymbolicSylvanParametricMA
from stormpy.storage.storage import SymbolicSylvanParametricMdp
from stormpy.storage.storage import SymbolicSylvanParametricRewardModel
from stormpy.storage.storage import SymbolicSylvanRewardModel
from stormpy.storage.storage import Valuation
from stormpy.storage.storage import Variable
from stormpy.storage.storage import collect_information
from stormpy.storage.storage import eliminate_reward_accumulations
import sys as sys
from . import _config
from . import _version
from . import core
from . import exceptions
from . import pycarl
from . import utility
__all__ = ['ActionMaskDouble', 'AddIterator_Sylvan_Double', 'Add_Sylvan_Double', 'AtomicExpressionFormula', 'AtomicLabelFormula', 'Bdd_Sylvan', 'BinaryBooleanOperatorType', 'BinaryPathFormula', 'BinaryStateFormula', 'BisimulationType', 'BitVector', 'BooleanBinaryStateFormula', 'BooleanLiteralFormula', 'BoundedUntilFormula', 'BuilderOptions', 'CheckTask', 'ChoiceLabeling', 'ChoiceOrigins', 'ComparisonType', 'ConditionalFormula', 'ConstraintCollector', 'CumulativeRewardFormula', 'DdManager_Sylvan', 'DdMetaVariableType', 'DdMetaVariable_Sylvan', 'Dd_Sylvan', 'DiceStringVisitor', 'DirectEncodingOptions', 'DirectEncodingParserOptions', 'Distribution', 'DistributionExact', 'DistributionInterval', 'EliminationLabelBehavior', 'EndComponentEliminatorReturnTypeDouble', 'Environment', 'EquationSolverType', 'EventuallyFormula', 'ExactCheckTask', 'ExactSparseMatrix', 'ExactSparseMatrixBuilder', 'ExactSparseMatrixEntry', 'ExactSparseMatrixRows', 'ExplicitExactQuantitativeCheckResult', 'ExplicitModelBuilder', 'ExplicitModelCheckerHintDouble', 'ExplicitParametricModelBuilder', 'ExplicitParametricQuantitativeCheckResult', 'ExplicitParetoCurveCheckResultDouble', 'ExplicitQualitativeCheckResult', 'ExplicitQuantitativeCheckResult', 'ExplicitStateLookup', 'Expression', 'ExpressionManager', 'ExpressionParser', 'ExpressionType', 'FactorizedPolynomial', 'FactorizedRationalFunction', 'FlatSet', 'Formula', 'GameFormula', 'GloballyFormula', 'HybridExactQuantitativeCheckResult', 'HybridParametricQuantitativeCheckResult', 'HybridQuantitativeCheckResult', 'InstantaneousRewardFormula', 'IntervalSparseMatrix', 'IntervalSparseMatrixBuilder', 'IntervalSparseMatrixEntry', 'IntervalSparseMatrixRows', 'ItemLabeling', 'JaniAssignment', 'JaniAutomaton', 'JaniChoiceOrigins', 'JaniConstant', 'JaniEdge', 'JaniEdgeDestination', 'JaniInformationObject', 'JaniLocation', 'JaniLocationExpander', 'JaniModel', 'JaniModelType', 'JaniOrderedAssignments', 'JaniScopeChanger', 'JaniTemplateEdge', 'JaniTemplateEdgeDestination', 'JaniVariable', 'JaniVariableSet', 'LongRunAvarageOperator', 'LongRunAverageRewardFormula', 'MaximalEndComponent', 'MaximalEndComponentDecomposition_double', 'MaximalEndComponentDecomposition_exact', 'MaximalEndComponentDecomposition_interval', 'MaximalEndComponentDecomposition_ratfunc', 'MinMaxMethod', 'MinMaxSolverEnvironment', 'ModelCheckerHint', 'ModelFormulasPair', 'ModelType', 'MultiObjectiveFormula', 'NativeLinearEquationSolverMethod', 'NativeSolverEnvironment', 'OperatorFormula', 'OperatorType', 'OptimizationDirection', 'OverlappingGuardAnalyser', 'ParametricCheckTask', 'ParametricSparseMatrix', 'ParametricSparseMatrixBuilder', 'ParametricSparseMatrixEntry', 'ParametricSparseMatrixRows', 'ParetoCurveCheckResultDouble', 'PathFormula', 'Polynomial', 'PolytopeDouble', 'PolytopeExact', 'PrismAssignment', 'PrismBooleanVariable', 'PrismChoiceOrigins', 'PrismCommand', 'PrismConstant', 'PrismIntegerVariable', 'PrismLabel', 'PrismModelType', 'PrismModule', 'PrismProgram', 'PrismRewardModel', 'PrismUpdate', 'PrismVariable', 'ProbabilityOperator', 'Property', 'QuotientFormat', 'Rational', 'RationalFunction', 'RationalRF', 'RewardOperator', 'SMTCounterExampleGenerator', 'SMTCounterExampleGeneratorOptions', 'SMTCounterExampleGeneratorStats', 'SMTCounterExampleInput', 'Scheduler', 'SchedulerChoice', 'SchedulerChoiceExact', 'SchedulerChoiceInterval', 'SchedulerChoiceParametric', 'SchedulerExact', 'SchedulerInterval', 'SchedulerParametric', 'SimpleValuation', 'SolverEnvironment', 'SparseCtmc', 'SparseDtmc', 'SparseExactCtmc', 'SparseExactDtmc', 'SparseExactMA', 'SparseExactMdp', 'SparseExactModelAction', 'SparseExactModelActions', 'SparseExactModelComponents', 'SparseExactModelState', 'SparseExactModelStates', 'SparseExactPomdp', 'SparseExactRewardModel', 'SparseExactSmg', 'SparseIntervalCtmc', 'SparseIntervalDtmc', 'SparseIntervalMA', 'SparseIntervalMdp', 'SparseIntervalModelAction', 'SparseIntervalModelActions', 'SparseIntervalModelComponents', 'SparseIntervalModelState', 'SparseIntervalModelStates', 'SparseIntervalPomdp', 'SparseIntervalRewardModel', 'SparseIntervalSmg', 'SparseMA', 'SparseMatrix', 'SparseMatrixBuilder', 'SparseMatrixEntry', 'SparseMatrixRows', 'SparseMdp', 'SparseModelAction', 'SparseModelActions', 'SparseModelComponents', 'SparseModelState', 'SparseModelStates', 'SparseParametricCtmc', 'SparseParametricDtmc', 'SparseParametricMA', 'SparseParametricMdp', 'SparseParametricModelAction', 'SparseParametricModelActions', 'SparseParametricModelComponents', 'SparseParametricModelState', 'SparseParametricModelStates', 'SparseParametricPomdp', 'SparseParametricRewardModel', 'SparsePomdp', 'SparseRewardModel', 'SparseSmg', 'StateFormula', 'StateLabeling', 'StateValuation', 'StateValuationFunctionActionMaskDouble', 'StateValuationsBuilder', 'StormError', 'SubsystemBuilderOptions', 'SubsystemBuilderReturnTypeDouble', 'SubsystemBuilderReturnTypeExact', 'SubsystemBuilderReturnTypeRatFunc', 'SymbolicExactQuantitativeCheckResult', 'SymbolicModelDescription', 'SymbolicParametricQuantitativeCheckResult', 'SymbolicQualitativeCheckResult', 'SymbolicQuantitativeCheckResult', 'SymbolicSylvanCtmc', 'SymbolicSylvanDtmc', 'SymbolicSylvanMA', 'SymbolicSylvanMdp', 'SymbolicSylvanParametricCtmc', 'SymbolicSylvanParametricDtmc', 'SymbolicSylvanParametricMA', 'SymbolicSylvanParametricMdp', 'SymbolicSylvanParametricRewardModel', 'SymbolicSylvanRewardModel', 'TimeOperator', 'UnaryBooleanStateFormula', 'UnaryPathFormula', 'UnaryStateFormula', 'UntilFormula', 'Valuation', 'Variable', 'build_interval_model_from_drn', 'build_model', 'build_model_from_drn', 'build_parametric_model', 'build_parametric_model_from_drn', 'build_parametric_sparse_matrix', 'build_sparse_exact_model_with_options', 'build_sparse_matrix', 'build_sparse_model', 'build_sparse_model_from_explicit', 'build_sparse_model_with_options', 'build_sparse_parametric_model', 'build_sparse_parametric_model_with_options', 'build_symbolic_model', 'build_symbolic_parametric_model', 'check_interval_mdp', 'check_model_dd', 'check_model_hybrid', 'check_model_sparse', 'cln', 'collect_information', 'compute_all_until_probabilities', 'compute_expected_number_of_visits', 'compute_prob01_states', 'compute_prob01max_states', 'compute_prob01min_states', 'compute_steady_state_distribution', 'compute_transient_probabilities', 'construct_submodel', 'core', 'create_filter_initial_states_sparse', 'create_filter_initial_states_symbolic', 'create_filter_symbolic', 'eliminate_ECs', 'eliminate_non_markovian_chains', 'eliminate_reward_accumulations', 'exceptions', 'export_to_drn', 'get_maximal_end_components', 'get_reachable_states', 'gmp', 'install_signal_handlers', 'logic', 'make_sparse_model_builder', 'make_sparse_model_builder_exact', 'make_sparse_model_builder_parametric', 'model_checking', 'parse_constants_string', 'parse_jani_model', 'parse_jani_model_from_string', 'parse_prism_program', 'parse_properties', 'parse_properties_for_jani_model', 'parse_properties_for_prism_program', 'parse_properties_without_context', 'perform_bisimulation', 'perform_sparse_bisimulation', 'perform_symbolic_bisimulation', 'preprocess_symbolic_input', 'prob01max_states', 'prob01min_states', 'pycarl', 'reset_timeout', 'set_loglevel_debug', 'set_loglevel_error', 'set_loglevel_trace', 'set_settings', 'set_timeout', 'storage', 'storm_with_dft', 'storm_with_gspn', 'storm_with_pars', 'storm_with_pomdp', 'storm_with_spot', 'storm_with_xerces', 'stormpy', 'sys', 'topological_sort', 'transform_to_discrete_time_model', 'transform_to_sparse_model', 'utility']
def _convert_sparse_model(model, parametric = False):
    """
    
        Convert (parametric) model in sparse representation into model corresponding to exact model type.
        :param model: Sparse model.
        :param parametric: Flag indicating if the model is parametric.
        :return: Model corresponding to exact model type.
        
    """
def _convert_symbolic_model(model, parametric = False):
    """
    
        Convert (parametric) model in symbolic representation into model corresponding to exact model type.
        :param model: Symbolic model.
        :param parametric: Flag indicating if the model is parametric.
        :return: Model corresponding to exact model type.
        
    """
def build_interval_model_from_drn(file, options = ...):
    """
    
        Build an interval model in sparse representation from the explicit DRN representation.
    
        :param String file: DRN file containing the model.
        :param DirectEncodingParserOptions: Options for the parser.
        :return: Interval model in sparse representation.
        
    """
def build_model(symbolic_description, properties = None):
    """
    
        Build a model in sparse representation from a symbolic description.
    
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Model in sparse representation.
        
    """
def build_model_from_drn(file, options = ...):
    """
    
        Build a model in sparse representation from the explicit DRN representation.
    
        :param String file: DRN file containing the model.
        :param DirectEncodingParserOptions: Options for the parser.
        :return: Model in sparse representation.
        
    """
def build_parametric_model(symbolic_description, properties = None):
    """
    
        Build a parametric model in sparse representation from a symbolic description.
    
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Parametric model in sparse representation.
        
    """
def build_parametric_model_from_drn(file, options = ...):
    """
    
        Build a parametric model in sparse representation from the explicit DRN representation.
    
        :param String file: DRN file containing the model.
        :param DirectEncodingParserOptions: Options for the parser.
        :return: Parametric model in sparse representation.
        
    """
def build_sparse_model(symbolic_description, properties = None):
    """
    
        Build a model in sparse representation from a symbolic description.
    
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Model in sparse representation.
        
    """
def build_sparse_parametric_model(symbolic_description, properties = None):
    """
    
        Build a parametric model in sparse representation from a symbolic description.
        
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Parametric model in sparse representation.
        
    """
def build_symbolic_model(symbolic_description, properties = None):
    """
    
        Build a model in symbolic representation from a symbolic description.
    
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Model in symbolic representation.
        
    """
def build_symbolic_parametric_model(symbolic_description, properties = None):
    """
    
        Build a parametric model in symbolic representation from a symbolic description.
    
        :param symbolic_description: Symbolic model description to translate into a model.
        :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
        :return: Parametric model in symbolic representation.
        
    """
def check_model_dd(model, property, only_initial_states = False, environment = ...):
    """
    
        Perform model checking using dd engine.
        :param model: Model.
        :param property: Property to check for.
        :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
        :return: Model checking result.
        :rtype: CheckResult
        
    """
def check_model_hybrid(model, property, only_initial_states = False, environment = ...):
    """
    
        Perform model checking using hybrid engine.
        :param model: Model.
        :param property: Property to check for.
        :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
        :return: Model checking result.
        :rtype: CheckResult
        
    """
def check_model_sparse(model, property, only_initial_states = False, extract_scheduler = False, force_fully_observable = False, hint = None, environment = ...):
    """
    
        Perform model checking on model for property.
        :param model: Model.
        :param property: Property to check for.
        :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
        :param extract_scheduler: If True, try to extract a scheduler
        :param hint: If not None, this hint is used by the model checker
        :param force_fully_observable: If True, treat a POMDP as an MDP
        :return: Model checking result.
        :rtype: CheckResult
        
    """
def compute_expected_number_of_visits(environment, model):
    """
    
        Compute the number of expected visits. Model must be deterministic.
    
        :param environment: An model checking environment
        :param model: A DTMC or CTMC
        :return: A vector with the expected number of visits
        
    """
def compute_prob01_states(model, phi_states, psi_states):
    """
    
        Compute prob01 states for properties of the form phi_states until psi_states
    
        :param SparseDTMC model:
        :param BitVector phi_states:
        :param BitVector psi_states: Target states
        
    """
def compute_prob01max_states(model, phi_states, psi_states):
    ...
def compute_prob01min_states(model, phi_states, psi_states):
    ...
def compute_steady_state_distribution(environment, model):
    """
    
        Compute the steady-state (aka stationary) distribution. Model must be deterministic.
    
        :param environment: A model checking environment
        :param model: A DTMC or CTMC
        :return: A vector with the steady-state distribution
        
    """
def construct_submodel(model, states, actions, keep_unreachable_states = True, options = ...):
    """
    
    
        :param model: The model
        :param states: Which states should be preserved
        :param actions: Which actions should be preserved
        :param keep_unreachable_states: If False, run a reachability analysis.
        :param options: An options object of type SubsystemBuilderOptions
        :return: A model with fewer states/actions
        
    """
def eliminate_ECs(matrix, subsystem, possible_ecs, add_sink_row_states, add_self_loop_at_sink_states = False):
    """
    
        For each such EC (that is not contained in another EC), we add a new state and redirect all incoming and outgoing
                 transitions of the EC to (and from) this state.
    
        :param matrix:
        :param subsystem: BitVector with states many entries. Only states in the given subsystem are kept. Transitions leading to a state outside of the subsystem will be
                 removed (but the corresponding row is kept, possibly yielding empty rows).
                 The ECs are then identified on the subsystem.
        :param possible_ecs: BitVector with rows many entries. Only ECs for which possible_ecs is true for all choices are considered.
                 Furthermore, the rows that contain a transition leading outside of the subsystem are not considered for an EC.
        :param add_sink_row_states: BitVector with states many entries. If add_sink_row_states is true for at least one state of an eliminated EC, a row is added to the new state (representing the choice to stay at the EC forever).
        :param add_self_loop_at_sink_states: if true, such rows get a selfloop (with value 1). Otherwise, the row remains empty.
        :return: A container with various information.
        
    """
def eliminate_non_markovian_chains(ma, properties, label_behavior):
    """
    
        Eliminate chains of non-Markovian states if possible.
        :param ma: Markov automaton.
        :param properties: List of properties to transform as well.
        :param label_behavior: Behavior of labels while elimination.
        :return: Tuple (converted MA, converted properties).
        
    """
def export_to_drn(model, file, options = ...):
    """
    
        Export a model to DRN format
        :param model: The model
        :param file: A path
        :param options: DirectEncodingOptions
        :return:
        
    """
def get_reachable_states(model, initial_states, constraint_states, target_states, maximal_steps = None, choice_filter = None):
    """
    
        Get the states that are reachable in a sparse model
    
        :param model: A model
        :param initial_states: Which states should be definitively reachable
        :param constraint_states:
        :param target_states: Which states should be considered absorbing
        :param maximal_steps: The maximal depth to explore
        :param choice_filter:
        :return:
        
    """
def model_checking(model, property, only_initial_states = False, extract_scheduler = False, force_fully_observable = False, environment = ...):
    """
    
        Perform model checking on model for property.
        :param model: Model.
        :param property: Property to check for.
        :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
        :param extract_scheduler: If True, try to extract a scheduler
        :return: Model checking result.
        :rtype: CheckResult
        
    """
def parse_properties(properties, context = None, filters = None):
    """
    
    
        :param properties: A string with the pctl properties
        :param context: A symbolic model that gives meaning to variables and constants.
        :param filters: filters, if applicable.
        :return: A list of properties
        
    """
def perform_bisimulation(model, properties, bisimulation_type):
    """
    
        Perform bisimulation on model.
        :param model: Model.
        :param properties: Properties to preserve during bisimulation.
        :param bisimulation_type: Type of bisimulation (weak or strong).
        :return: Model after bisimulation.
        
    """
def perform_sparse_bisimulation(model, properties, bisimulation_type):
    """
    
        Perform bisimulation on model in sparse representation.
        :param model: Model.
        :param properties: Properties to preserve during bisimulation.
        :param bisimulation_type: Type of bisimulation (weak or strong).
        :return: Model after bisimulation.
        
    """
def perform_symbolic_bisimulation(model, properties, quotient_format = ...):
    """
    
        Perform bisimulation on model in symbolic representation.
        :param model: Model.
        :param properties: Properties to preserve during bisimulation.
        :param quotient_format: Return format of quotient.
        :return: Model after bisimulation.
        
    """
def prob01max_states(model, eventually_formula):
    ...
def prob01min_states(model, eventually_formula):
    ...
def topological_sort(model, forward = True, initial = list()):
    """
    
    
        :param model: A sparse model
        :param forward: A flag whether the sorting should be forward or backwards
        :param initial: a list of states
        :return: A topological sort of the states
        
    """
def transform_to_discrete_time_model(model, properties):
    """
    
        Transform continuous-time model to discrete time model.
        :param model: Continuous-time model.
        :param properties: List of properties to transform as well.
        :return: Tuple (Discrete-time model, converted properties).
        
    """
def transform_to_sparse_model(model):
    """
    
        Transform model in symbolic representation into model in sparse representation.
        :param model: Symbolic model.
        :return: Sparse model.
        
    """
__version__: str = '1.9.0'
storm_with_dft: bool = True
storm_with_gspn: bool = True
storm_with_pars: bool = True
storm_with_pomdp: bool = True
storm_with_spot: bool = False
storm_with_xerces: bool = True
stormpy = 
