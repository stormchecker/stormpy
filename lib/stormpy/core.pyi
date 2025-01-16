"""
core
"""
from __future__ import annotations
import stormpy.pycarl.cln
import stormpy.pycarl.gmp
import typing
__all__ = ['ActionMaskDouble', 'BisimulationType', 'BuilderOptions', 'CheckTask', 'ConstraintCollector', 'DirectEncodingOptions', 'DirectEncodingParserOptions', 'EliminationLabelBehavior', 'EndComponentEliminatorReturnTypeDouble', 'Environment', 'EquationSolverType', 'ExactCheckTask', 'ExplicitExactQuantitativeCheckResult', 'ExplicitModelBuilder', 'ExplicitModelCheckerHintDouble', 'ExplicitParametricModelBuilder', 'ExplicitParametricQuantitativeCheckResult', 'ExplicitParetoCurveCheckResultDouble', 'ExplicitQualitativeCheckResult', 'ExplicitQuantitativeCheckResult', 'ExplicitStateLookup', 'FlatSet', 'HybridExactQuantitativeCheckResult', 'HybridParametricQuantitativeCheckResult', 'HybridQuantitativeCheckResult', 'JaniModelType', 'MinMaxMethod', 'MinMaxSolverEnvironment', 'ModelCheckerHint', 'ModelFormulasPair', 'NativeLinearEquationSolverMethod', 'NativeSolverEnvironment', 'OptimizationDirection', 'ParametricCheckTask', 'ParetoCurveCheckResultDouble', 'Property', 'QuotientFormat', 'SMTCounterExampleGenerator', 'SMTCounterExampleGeneratorOptions', 'SMTCounterExampleGeneratorStats', 'SMTCounterExampleInput', 'SolverEnvironment', 'StateValuationFunctionActionMaskDouble', 'SubsystemBuilderOptions', 'SubsystemBuilderReturnTypeDouble', 'SubsystemBuilderReturnTypeExact', 'SubsystemBuilderReturnTypeRatFunc', 'SymbolicExactQuantitativeCheckResult', 'SymbolicModelDescription', 'SymbolicParametricQuantitativeCheckResult', 'SymbolicQualitativeCheckResult', 'SymbolicQuantitativeCheckResult', 'build_sparse_exact_model_with_options', 'build_sparse_model_from_explicit', 'build_sparse_model_with_options', 'build_sparse_parametric_model_with_options', 'check_interval_mdp', 'compute_all_until_probabilities', 'compute_transient_probabilities', 'create_filter_initial_states_sparse', 'create_filter_initial_states_symbolic', 'create_filter_symbolic', 'install_signal_handlers', 'make_sparse_model_builder', 'make_sparse_model_builder_exact', 'make_sparse_model_builder_parametric', 'parse_constants_string', 'parse_jani_model', 'parse_jani_model_from_string', 'parse_prism_program', 'parse_properties_for_jani_model', 'parse_properties_for_prism_program', 'parse_properties_without_context', 'preprocess_symbolic_input', 'reset_timeout', 'set_loglevel_debug', 'set_loglevel_error', 'set_loglevel_trace', 'set_settings', 'set_timeout']
class ActionMaskDouble:
    pass
class BisimulationType:
    """
    Types of bisimulation
    
    Members:
    
      STRONG
    
      WEAK
    """
    STRONG: typing.ClassVar[BisimulationType]  # value = <BisimulationType.STRONG: 0>
    WEAK: typing.ClassVar[BisimulationType]  # value = <BisimulationType.WEAK: 1>
    __members__: typing.ClassVar[dict[str, BisimulationType]]  # value = {'STRONG': <BisimulationType.STRONG: 0>, 'WEAK': <BisimulationType.WEAK: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BuilderOptions:
    """
    Options for building process
    """
    @typing.overload
    def __init__(self, formulae: list[...]) -> None:
        """
        Initialise with formulae to preserve
        """
    @typing.overload
    def __init__(self, build_all_reward_models: bool = True, build_all_labels: bool = True) -> None:
        """
        Initialise without formulae
        """
    def set_add_out_of_bounds_state(self, new_value: bool = True) -> BuilderOptions:
        """
        Build with out of bounds state
        """
    def set_add_overlapping_guards_label(self, new_value: bool = True) -> BuilderOptions:
        """
        Build with overlapping guards state labeled
        """
    def set_build_all_labels(self, new_value: bool = True) -> BuilderOptions:
        """
        Build with all state labels
        """
    def set_build_all_reward_models(self, new_value: bool = True) -> BuilderOptions:
        """
        Build with all reward models
        """
    def set_build_choice_labels(self, new_value: bool = True) -> BuilderOptions:
        """
        Build with choice labels
        """
    def set_build_observation_valuations(self, new_value: bool = True) -> BuilderOptions:
        """
        Build observation valuations
        """
    def set_build_state_valuations(self, new_value: bool = True) -> BuilderOptions:
        """
        Build state valuations
        """
    def set_build_with_choice_origins(self, new_value: bool = True) -> BuilderOptions:
        """
        Build choice origins
        """
    def set_exploration_checks(self, new_value: bool = True) -> BuilderOptions:
        """
        Perform extra checks during exploration
        """
    @property
    def preserved_label_names(self) -> set[str]:
        """
        Labels preserved
        """
class CheckTask:
    """
    Task for model checking
    """
    def __init__(self, formula: ..., only_initial_states: bool = False) -> None:
        ...
    def set_hint(self, arg0: ...) -> None:
        """
        Sets a hint that may speed up the solver
        """
    def set_produce_schedulers(self, produce_schedulers: bool = True) -> None:
        """
        Set whether schedulers should be produced (if possible)
        """
    def set_robust_uncertainty(self, arg0: bool) -> None:
        """
        Sets whether robust uncertainty should be considered
        """
class ConstraintCollector:
    """
    Collector for constraints on parametric Markov chains
    """
    @staticmethod
    def __init__(*args, **kwargs) -> None:
        ...
    @property
    def graph_preserving_constraints(self) -> set[..., ..., ...]:
        """
        Get the constraints ensuring the graph is preserved
        """
    @property
    def wellformed_constraints(self) -> set[..., ..., ...]:
        """
        Get the constraints ensuring a wellformed model
        """
class DirectEncodingOptions:
    allow_placeholders: bool
    def __init__(self) -> None:
        ...
class DirectEncodingParserOptions:
    """
    Options for the .drn parser
    """
    def __init__(self) -> None:
        """
        initialise
        """
    @property
    def build_choice_labels(self) -> bool:
        """
        Build with choice labels
        """
    @build_choice_labels.setter
    def build_choice_labels(self, arg0: bool) -> None:
        ...
class EliminationLabelBehavior:
    """
    Behavior of labels while eliminating non-Markovian chains
    
    Members:
    
      KEEP_LABELS
    
      MERGE_LABELS
    
      DELETE_LABELS
    """
    DELETE_LABELS: typing.ClassVar[EliminationLabelBehavior]  # value = <EliminationLabelBehavior.DELETE_LABELS: 3>
    KEEP_LABELS: typing.ClassVar[EliminationLabelBehavior]  # value = <EliminationLabelBehavior.KEEP_LABELS: 0>
    MERGE_LABELS: typing.ClassVar[EliminationLabelBehavior]  # value = <EliminationLabelBehavior.MERGE_LABELS: 2>
    __members__: typing.ClassVar[dict[str, EliminationLabelBehavior]]  # value = {'KEEP_LABELS': <EliminationLabelBehavior.KEEP_LABELS: 0>, 'MERGE_LABELS': <EliminationLabelBehavior.MERGE_LABELS: 2>, 'DELETE_LABELS': <EliminationLabelBehavior.DELETE_LABELS: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EndComponentEliminatorReturnTypeDouble:
    """
    Container for result of endcomponent elimination
    """
    @property
    def matrix(self) -> ...:
        """
        The resulting matrix
        """
    @property
    def new_to_old_row_mapping(self) -> list[int]:
        """
        Index mapping that gives for each row fo the new matrix the corresponding row in the original matrix
        """
    @property
    def old_to_new_state_mapping(self) -> list[int]:
        """
        For each state of the original matrix (and subsystem) the corresponding state in the result. Removed states are mapped to the EC.
        """
    @property
    def sink_rows(self) -> ...:
        """
        Rows that indicate staying in the EC forever
        """
class Environment:
    """
    Environment
    """
    def __init__(self) -> None:
        """
        Construct default environment
        """
    @property
    def solver_environment(self) -> ...:
        """
        solver part of environment
        """
class EquationSolverType:
    """
    Solver type for equation systems
    
    Members:
    
      native
    
      eigen
    
      elimination
    
      gmmxx
    
      topological
    """
    __members__: typing.ClassVar[dict[str, EquationSolverType]]  # value = {'native': <EquationSolverType.native: 0>, 'eigen': <EquationSolverType.eigen: 2>, 'elimination': <EquationSolverType.elimination: 3>, 'gmmxx': <EquationSolverType.gmmxx: 1>, 'topological': <EquationSolverType.topological: 4>}
    eigen: typing.ClassVar[EquationSolverType]  # value = <EquationSolverType.eigen: 2>
    elimination: typing.ClassVar[EquationSolverType]  # value = <EquationSolverType.elimination: 3>
    gmmxx: typing.ClassVar[EquationSolverType]  # value = <EquationSolverType.gmmxx: 1>
    native: typing.ClassVar[EquationSolverType]  # value = <EquationSolverType.native: 0>
    topological: typing.ClassVar[EquationSolverType]  # value = <EquationSolverType.topological: 4>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ExactCheckTask:
    """
    Task for model checking with exact numbers
    """
    def __init__(self, formula: ..., only_initial_states: bool = False) -> None:
        ...
    def set_produce_schedulers(self, produce_schedulers: bool = True) -> None:
        """
        Set whether schedulers should be produced (if possible)
        """
class ExplicitExactQuantitativeCheckResult(_ExactQuantitativeCheckResult):
    """
    Explicit exact quantitative model checking result
    """
    def __init__(self, values: list[stormpy.pycarl.gmp.Rational]) -> None:
        ...
    def at(self, state: int) -> stormpy.pycarl.gmp.Rational:
        """
        Get result for given state
        """
    def get_values(self) -> list[stormpy.pycarl.gmp.Rational]:
        """
        Get model checking result values for all states
        """
    @property
    def scheduler(self) -> ...:
        """
        get scheduler
        """
class ExplicitModelBuilder:
    """
    Model builder for sparse models
    """
    def build(self) -> ...:
        """
        Build the model
        """
    def export_lookup(self) -> ...:
        """
        Export a lookup model
        """
class ExplicitModelCheckerHintDouble(ModelCheckerHint):
    """
    Information that may accelerate an explicit state model checker
    """
    def __init__(self) -> None:
        ...
    def set_compute_only_maybe_states(self, arg0: bool) -> None:
        """
        value
        """
    def set_maybe_states(self, arg0: ...) -> None:
        """
        sets the maybe states. This is assumed to be correct.
        """
    def set_result_hint(self, result_hint: list[float] | None) -> None:
        ...
    def set_scheduler_hint(self, scheduler_hint: ... | None) -> None:
        """
        Set a scheduler that is close to the optimal scheduler
        """
class ExplicitParametricModelBuilder:
    """
    Model builder for sparse models
    """
    def build(self) -> ...:
        """
        Build the model
        """
    def export_lookup(self) -> ...:
        """
        Export a lookup model
        """
class ExplicitParametricQuantitativeCheckResult(_ParametricQuantitativeCheckResult):
    """
    Explicit parametric quantitative model checking result
    """
    def at(self, state: int) -> stormpy.pycarl.cln.FactorizedRationalFunction:
        """
        Get result for given state
        """
    def get_values(self) -> list[stormpy.pycarl.cln.FactorizedRationalFunction]:
        """
        Get model checking result values for all states
        """
    @property
    def scheduler(self) -> ...:
        """
        get scheduler
        """
class ExplicitParetoCurveCheckResultDouble(ParetoCurveCheckResultDouble):
    """
    Result for explicit multiobjective model checking
    """
class ExplicitQualitativeCheckResult(_QualitativeCheckResult):
    """
    Explicit qualitative model checking result
    """
    def at(self, state: int) -> bool:
        """
        Get result for given state
        """
    def get_truth_values(self) -> ...:
        """
        Get BitVector representing the truth values
        """
class ExplicitQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Explicit quantitative model checking result
    """
    def __init__(self, values: list[float]) -> None:
        ...
    def at(self, state: int) -> float:
        """
        Get result for given state
        """
    def get_values(self) -> list[float]:
        """
        Get model checking result values for all states
        """
    @property
    def scheduler(self) -> ...:
        """
        get scheduler
        """
class ExplicitStateLookup:
    """
    Lookup model for states
    """
    def lookup(self, state_description: dict[..., ...]) -> typing.Any:
        ...
class FlatSet:
    """
    Container to pass to program
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, other: FlatSet) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def insert(self, arg0: int) -> None:
        ...
    def insert_set(self, arg0: FlatSet) -> None:
        ...
    def is_subset_of(self, arg0: FlatSet) -> bool:
        ...
class HybridExactQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Symbolic exact hybrid quantitative model checking result
    """
    def get_values(self) -> list[stormpy.pycarl.gmp.Rational]:
        """
        Get model checking result values for all states
        """
class HybridParametricQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Symbolic parametric hybrid quantitative model checking result
    """
    def get_values(self) -> list[stormpy.pycarl.cln.FactorizedRationalFunction]:
        """
        Get model checking result values for all states
        """
class HybridQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Hybrid quantitative model checking result
    """
    def get_values(self) -> list[float]:
        """
        Get model checking result values for all states
        """
class JaniModelType:
    """
    Type of the Jani model
    
    Members:
    
      DTMC
    
      CTMC
    
      MDP
    
      CTMDP
    
      MA
    
      LTS
    
      TA
    
      PTA
    
      STA
    
      HA
    
      PHA
    
      SHA
    
      UNDEFINED
    """
    CTMC: typing.ClassVar[JaniModelType]  # value = <JaniModelType.CTMC: 3>
    CTMDP: typing.ClassVar[JaniModelType]  # value = <JaniModelType.CTMDP: 5>
    DTMC: typing.ClassVar[JaniModelType]  # value = <JaniModelType.DTMC: 2>
    HA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.HA: 10>
    LTS: typing.ClassVar[JaniModelType]  # value = <JaniModelType.LTS: 1>
    MA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.MA: 6>
    MDP: typing.ClassVar[JaniModelType]  # value = <JaniModelType.MDP: 4>
    PHA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.PHA: 11>
    PTA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.PTA: 8>
    SHA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.SHA: 12>
    STA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.STA: 9>
    TA: typing.ClassVar[JaniModelType]  # value = <JaniModelType.TA: 7>
    UNDEFINED: typing.ClassVar[JaniModelType]  # value = <JaniModelType.UNDEFINED: 0>
    __members__: typing.ClassVar[dict[str, JaniModelType]]  # value = {'DTMC': <JaniModelType.DTMC: 2>, 'CTMC': <JaniModelType.CTMC: 3>, 'MDP': <JaniModelType.MDP: 4>, 'CTMDP': <JaniModelType.CTMDP: 5>, 'MA': <JaniModelType.MA: 6>, 'LTS': <JaniModelType.LTS: 1>, 'TA': <JaniModelType.TA: 7>, 'PTA': <JaniModelType.PTA: 8>, 'STA': <JaniModelType.STA: 9>, 'HA': <JaniModelType.HA: 10>, 'PHA': <JaniModelType.PHA: 11>, 'SHA': <JaniModelType.SHA: 12>, 'UNDEFINED': <JaniModelType.UNDEFINED: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MinMaxMethod:
    """
    Method for min-max equation systems
    
    Members:
    
      policy_iteration
    
      value_iteration
    
      linear_programming
    
      topological
    
      rational_search
    
      interval_iteration
    
      sound_value_iteration
    
      optimistic_value_iteration
    """
    __members__: typing.ClassVar[dict[str, MinMaxMethod]]  # value = {'policy_iteration': <MinMaxMethod.policy_iteration: 1>, 'value_iteration': <MinMaxMethod.value_iteration: 0>, 'linear_programming': <MinMaxMethod.linear_programming: 2>, 'topological': <MinMaxMethod.topological: 3>, 'rational_search': <MinMaxMethod.rational_search: 4>, 'interval_iteration': <MinMaxMethod.interval_iteration: 5>, 'sound_value_iteration': <MinMaxMethod.sound_value_iteration: 6>, 'optimistic_value_iteration': <MinMaxMethod.optimistic_value_iteration: 7>}
    interval_iteration: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.interval_iteration: 5>
    linear_programming: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.linear_programming: 2>
    optimistic_value_iteration: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.optimistic_value_iteration: 7>
    policy_iteration: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.policy_iteration: 1>
    rational_search: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.rational_search: 4>
    sound_value_iteration: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.sound_value_iteration: 6>
    topological: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.topological: 3>
    value_iteration: typing.ClassVar[MinMaxMethod]  # value = <MinMaxMethod.value_iteration: 0>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MinMaxSolverEnvironment:
    """
    Environment for Min-Max-Solvers
    """
    method: MinMaxMethod
    precision: stormpy.pycarl.gmp.Rational
class ModelCheckerHint:
    """
    Information that may accelerate the model checking process
    """
class ModelFormulasPair:
    """
    Pair of model and formulas
    """
    @property
    def formulas(self) -> list[...]:
        """
        The formulas
        """
    @property
    def model(self) -> ...:
        """
        The model
        """
class NativeLinearEquationSolverMethod:
    """
    Method for linear equation systems with the native solver
    
    Members:
    
      power_iteration
    
      sound_value_iteration
    
      optimistic_value_iteration
    
      interval_iteration
    
      rational_search
    
      jacobi
    
      SOR
    
      gauss_seidel
    
      walker_chae
    """
    SOR: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.SOR: 2>
    __members__: typing.ClassVar[dict[str, NativeLinearEquationSolverMethod]]  # value = {'power_iteration': <NativeLinearEquationSolverMethod.power_iteration: 4>, 'sound_value_iteration': <NativeLinearEquationSolverMethod.sound_value_iteration: 5>, 'optimistic_value_iteration': <NativeLinearEquationSolverMethod.optimistic_value_iteration: 6>, 'interval_iteration': <NativeLinearEquationSolverMethod.interval_iteration: 7>, 'rational_search': <NativeLinearEquationSolverMethod.rational_search: 8>, 'jacobi': <NativeLinearEquationSolverMethod.jacobi: 0>, 'SOR': <NativeLinearEquationSolverMethod.SOR: 2>, 'gauss_seidel': <NativeLinearEquationSolverMethod.gauss_seidel: 1>, 'walker_chae': <NativeLinearEquationSolverMethod.walker_chae: 3>}
    gauss_seidel: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.gauss_seidel: 1>
    interval_iteration: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.interval_iteration: 7>
    jacobi: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.jacobi: 0>
    optimistic_value_iteration: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.optimistic_value_iteration: 6>
    power_iteration: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.power_iteration: 4>
    rational_search: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.rational_search: 8>
    sound_value_iteration: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.sound_value_iteration: 5>
    walker_chae: typing.ClassVar[NativeLinearEquationSolverMethod]  # value = <NativeLinearEquationSolverMethod.walker_chae: 3>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class NativeSolverEnvironment:
    """
    Environment for Native solvers
    """
    maximum_iterations: int
    method: NativeLinearEquationSolverMethod
    precision: stormpy.pycarl.gmp.Rational
class OptimizationDirection:
    """
    Members:
    
      Minimize
    
      Maximize
    """
    Maximize: typing.ClassVar[OptimizationDirection]  # value = <OptimizationDirection.Maximize: 1>
    Minimize: typing.ClassVar[OptimizationDirection]  # value = <OptimizationDirection.Minimize: 0>
    __members__: typing.ClassVar[dict[str, OptimizationDirection]]  # value = {'Minimize': <OptimizationDirection.Minimize: 0>, 'Maximize': <OptimizationDirection.Maximize: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ParametricCheckTask:
    """
    Task for parametric model checking
    """
    def __init__(self, formula: ..., only_initial_states: bool = False) -> None:
        ...
    def set_produce_schedulers(self, produce_schedulers: bool = True) -> None:
        """
        Set whether schedulers should be produced (if possible)
        """
class ParetoCurveCheckResultDouble(_CheckResult):
    """
    Result for multiobjective model checking
    """
    def get_overapproximation(self) -> ...:
        ...
    def get_underapproximation(self) -> ...:
        ...
class Property:
    """
    Property
    """
    @typing.overload
    def __init__(self, name: str, formula: ..., undefined_constants: set[...] = set(), comment: str = '') -> None:
        """
        Construct property from formula
        """
    @typing.overload
    def __init__(self, arg0: Property) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        """
        Obtain the name of the property
        """
    @property
    def raw_formula(self) -> ...:
        """
        Obtain the formula directly
        """
class QuotientFormat:
    """
    Return format of bisimulation quotient
    
    Members:
    
      SPARSE
    
      DD
    """
    DD: typing.ClassVar[QuotientFormat]  # value = <QuotientFormat.DD: 1>
    SPARSE: typing.ClassVar[QuotientFormat]  # value = <QuotientFormat.SPARSE: 0>
    __members__: typing.ClassVar[dict[str, QuotientFormat]]  # value = {'SPARSE': <QuotientFormat.SPARSE: 0>, 'DD': <QuotientFormat.DD: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SMTCounterExampleGenerator:
    """
    Highlevel Counterexample Generator with SMT as backend
    """
    @staticmethod
    def build(env: Environment, stats: SMTCounterExampleGeneratorStats, symbolic_model: ..., model: ..., storm: ..., cex_input: ..., dontcare: FlatSet, options: SMTCounterExampleGeneratorOptions) -> list[FlatSet]:
        """
        Compute counterexample
        """
    @staticmethod
    def precompute(env: Environment, symbolic_model: ..., model: ..., storm: ..., formula: ...) -> ...:
        """
        Precompute input for counterexample generation
        """
class SMTCounterExampleGeneratorOptions:
    """
    Options for highlevel counterexample generation
    """
    add_backward_implication_cuts: bool
    check_threshold_feasible: bool
    continue_after_first_counterexample: int
    encode_reachability: bool
    maximum_counterexamples: int
    maximum_iterations_after_counterexample: int
    silent: bool
    use_dynamic_constraints: bool
    def __init__(self) -> None:
        ...
class SMTCounterExampleGeneratorStats:
    """
    Stats for highlevel counterexample generation
    """
    def __init__(self) -> None:
        ...
    @property
    def analysis_time(self) -> ...:
        ...
    @property
    def cut_time(self) -> ...:
        ...
    @property
    def iterations(self) -> int:
        ...
    @property
    def model_checking_time(self) -> ...:
        ...
    @property
    def setup_time(self) -> ...:
        ...
    @property
    def solver_time(self) -> ...:
        ...
class SMTCounterExampleInput:
    """
    Precomputed input for counterexample generation
    """
    def add_reward_and_threshold(self, reward_name: str, threshold: float) -> None:
        """
        add another reward structure and threshold
        """
class SolverEnvironment:
    """
    Environment for solvers
    """
    def set_force_sound(self, new_value: bool = True) -> None:
        """
        force soundness
        """
    def set_linear_equation_solver_type(self, new_value: EquationSolverType, set_from_default: bool = False) -> None:
        """
        set solver type to use
        """
    @property
    def minmax_solver_environment(self) -> ...:
        ...
    @property
    def native_solver_environment(self) -> ...:
        ...
class StateValuationFunctionActionMaskDouble(ActionMaskDouble):
    def __init__(self, f: typing.Callable[[..., int], bool]) -> None:
        ...
class SubsystemBuilderOptions:
    """
    Options for constructing the subsystem
    """
    build_action_mapping: bool
    build_kept_actions: bool
    build_state_mapping: bool
    check_transitions_outside: bool
    fix_deadlocks: bool
    def __init__(self) -> None:
        ...
class SubsystemBuilderReturnTypeDouble:
    """
    Result of the construction of a subsystem
    """
    @property
    def deadlock_label(self) -> str | None:
        """
        If set, deadlock states have been introduced and have been assigned this label
        """
    @property
    def kept_actions(self) -> ...:
        """
        Actions of the subsystem available in the original system
        """
    @property
    def model(self) -> ...:
        """
        the submodel
        """
    @property
    def new_to_old_action_mapping(self) -> list[int]:
        """
        for each action in result, the action index in the original model
        """
    @property
    def new_to_old_state_mapping(self) -> list[int]:
        """
        for each state in result, the state index in the original model
        """
class SubsystemBuilderReturnTypeExact:
    """
    Result of the construction of a subsystem
    """
    @property
    def deadlock_label(self) -> str | None:
        """
        If set, deadlock states have been introduced and have been assigned this label
        """
    @property
    def kept_actions(self) -> ...:
        """
        Actions of the subsystem available in the original system
        """
    @property
    def model(self) -> ...:
        """
        the submodel
        """
    @property
    def new_to_old_action_mapping(self) -> list[int]:
        """
        for each action in result, the action index in the original model
        """
    @property
    def new_to_old_state_mapping(self) -> list[int]:
        """
        for each state in result, the state index in the original model
        """
class SubsystemBuilderReturnTypeRatFunc:
    """
    Result of the construction of a subsystem
    """
    @property
    def deadlock_label(self) -> str | None:
        """
        If set, deadlock states have been introduced and have been assigned this label
        """
    @property
    def kept_actions(self) -> ...:
        """
        Actions of the subsystem available in the original system
        """
    @property
    def model(self) -> ...:
        """
        the submodel
        """
    @property
    def new_to_old_action_mapping(self) -> list[int]:
        """
        for each action in result, the action index in the original model
        """
    @property
    def new_to_old_state_mapping(self) -> list[int]:
        """
        for each state in result, the state index in the original model
        """
class SymbolicExactQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Symbolic exact quantitative model checking result
    """
    def clone(self) -> SymbolicExactQuantitativeCheckResult:
        ...
class SymbolicModelDescription:
    """
    Symbolic description of model
    """
    @staticmethod
    def parse_constant_definitions(*args, **kwargs) -> dict[..., ...]:
        """
        Parse given constant definitions
        """
    @typing.overload
    def __init__(self, prism_program: ...) -> None:
        """
        Construct from Prism program
        """
    @typing.overload
    def __init__(self, jani_model: ...) -> None:
        """
        Construct from Jani model
        """
    def as_jani_model(self) -> ...:
        """
        Return Jani model
        """
    def as_prism_program(self) -> ...:
        """
        Return Prism program
        """
    def instantiate_constants(self, constant_definitions: dict[..., ...]) -> SymbolicModelDescription:
        """
        Instantiate constants in symbolic model description
        """
    @property
    def is_jani_model(self) -> bool:
        """
        Flag if program is in Jani format
        """
    @property
    def is_prism_program(self) -> bool:
        """
        Flag if program is in Prism format
        """
class SymbolicParametricQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Symbolic parametric quantitative model checking result
    """
    def clone(self) -> SymbolicParametricQuantitativeCheckResult:
        ...
class SymbolicQualitativeCheckResult(_QualitativeCheckResult):
    """
    Symbolic qualitative model checking result
    """
    def get_truth_values(self) -> ...:
        """
        Get Dd representing the truth values
        """
class SymbolicQuantitativeCheckResult(_QuantitativeCheckResult):
    """
    Symbolic quantitative model checking result
    """
    def clone(self) -> SymbolicQuantitativeCheckResult:
        ...
    def get_values(self) -> ...:
        ...
class _CheckResult:
    """
    Base class for all modelchecking results
    """
    def __str__(self) -> str:
        ...
    def as_explicit_exact_quantitative(self) -> ...:
        """
        Convert into explicit quantitative result
        """
    def as_explicit_parametric_quantitative(self) -> ...:
        """
        Convert into explicit quantitative result
        """
    def as_explicit_qualitative(self) -> ...:
        """
        Convert into explicit qualitative result
        """
    def as_explicit_quantitative(self) -> ...:
        """
        Convert into explicit quantitative result
        """
    def filter(self, filter: ...) -> None:
        """
        Filter the result
        """
    @property
    def _explicit_qualitative(self) -> bool:
        """
        Flag if result is explicit qualitative
        """
    @property
    def _explicit_quantitative(self) -> bool:
        """
        Flag if result is explicit quantitative
        """
    @property
    def _hybrid(self) -> bool:
        """
        Flag if result is hybrid
        """
    @property
    def _hybrid_quantitative(self) -> bool:
        """
        Flag if result is hybrid quantitative
        """
    @property
    def _pareto_curve(self) -> bool:
        """
        Flag if result is a pareto curve
        """
    @property
    def _qualitative(self) -> bool:
        """
        Flag if result is qualitative
        """
    @property
    def _quantitative(self) -> bool:
        """
        Flag if result is quantitative
        """
    @property
    def _symbolic(self) -> bool:
        """
        Flag if result is symbolic
        """
    @property
    def _symbolic_qualitative(self) -> bool:
        """
        Flag if result is symbolic qualitative
        """
    @property
    def _symbolic_quantitative(self) -> bool:
        """
        Flag if result is symbolic quantitative
        """
    @property
    def has_scheduler(self) -> bool:
        """
        Flag if a scheduler is present
        """
    @property
    def result_for_all_states(self) -> bool:
        """
        Flag if result is for all states
        """
class _DiscreteTimePrismProgramSimulatorDouble:
    """
    Simulator for prism programs
    """
    def __init__(self, program: ..., options: BuilderOptions) -> None:
        ...
    def _reset_to_state_from_compressed_state(self, arg0: ...) -> None:
        ...
    def _reset_to_state_from_valuation(self, arg0: ...) -> None:
        ...
    def get_action_indices(self) -> list[int]:
        """
        A list of choices that encode the possibilities in the current state.
        """
    def get_current_labels(self) -> list[str]:
        """
        What are the state labels at the current state?
        """
    def get_current_observation_as_json(self) -> ...:
        ...
    def get_current_state(self) -> ...:
        """
        Get current state
        """
    def get_current_state_as_json(self) -> ...:
        ...
    def get_current_state_is_sink(self) -> bool:
        ...
    def get_last_reward(self) -> list[float]:
        ...
    def get_number_of_current_choices(self) -> int:
        ...
    def get_reward_names(self) -> list[str]:
        """
        Get names of the rewards provided by the simulator
        """
    def reset_to_initial_state(self) -> bool:
        """
        Reset to the initial state
        """
    def set_seed(self, seed: int) -> None:
        ...
    def step(self, action_index: int) -> bool:
        """
        Make a step and randomly select the successor. The action is given as an argument, the index reflects the index of the getChoices vector that can be accessed.
        """
class _DiscreteTimeSparseModelSimulatorDouble:
    """
    Simulator for sparse discrete-time models in memory (for ValueType)
    """
    def __init__(self, arg0: ..., storm: ...) -> None:
        ...
    def get_current_state(self) -> int:
        ...
    def get_last_reward(self) -> list[float]:
        ...
    def random_step(self) -> bool:
        ...
    def reset_to_initial_state(self) -> bool:
        ...
    def set_seed(self, seed: int) -> None:
        ...
    def step(self, action: int) -> bool:
        ...
class _DiscreteTimeSparseModelSimulatorExact:
    """
    Simulator for sparse discrete-time models in memory (for ValueType)
    """
    @staticmethod
    def __init__(*args, **kwargs) -> None:
        ...
    def get_current_state(self) -> int:
        ...
    def get_last_reward(self) -> list[stormpy.pycarl.gmp.Rational]:
        ...
    def random_step(self) -> bool:
        ...
    def reset_to_initial_state(self) -> bool:
        ...
    def set_seed(self, seed: int) -> None:
        ...
    def step(self, action: int) -> bool:
        ...
class _ExactQuantitativeCheckResult(_CheckResult):
    """
    Abstract class for exact quantitative model checking results
    """
class _ParametricQuantitativeCheckResult(_CheckResult):
    """
    Abstract class for parametric quantitative model checking results
    """
class _QualitativeCheckResult(_CheckResult):
    """
    Abstract class for qualitative model checking results
    """
class _QuantitativeCheckResult(_CheckResult):
    """
    Abstract class for quantitative model checking results
    """
    @property
    def max(self) -> float:
        """
        Maximal value
        """
    @property
    def min(self) -> float:
        """
        Minimal value
        """
def _build_sparse_exact_model_from_drn(file: str, options: DirectEncodingParserOptions = ...) -> ...:
    """
    Build the model from DRN
    """
def _build_sparse_exact_model_from_symbolic_description(model_description: ..., formulas: list[...] = []) -> ...:
    """
    Build the model in sparse representation with exact number representation
    """
def _build_sparse_interval_model_from_drn(file: str, options: DirectEncodingParserOptions = ...) -> ...:
    """
    Build the interval model from DRN
    """
def _build_sparse_model_from_drn(file: str, options: DirectEncodingParserOptions = ...) -> ...:
    """
    Build the model from DRN
    """
def _build_sparse_model_from_symbolic_description(model_description: ..., formulas: list[...] = []) -> ...:
    """
    Build the model in sparse representation
    """
def _build_sparse_parametric_model_from_drn(file: str, options: DirectEncodingParserOptions = ...) -> ...:
    """
    Build the parametric model from DRN
    """
def _build_sparse_parametric_model_from_symbolic_description(model_description: ..., formulas: list[...] = []) -> ...:
    """
    Build the parametric model in sparse representation
    """
def _build_symbolic_model_from_symbolic_description(model_description: ..., formulas: list[...] = []) -> ...:
    """
    Build the model in symbolic representation
    """
def _build_symbolic_parametric_model_from_symbolic_description(model_description: ..., formulas: list[...] = []) -> ...:
    """
    Build the parametric model in symbolic representation
    """
def _compute_expected_number_of_visits_double(env: Environment, model: ..., storm: ...) -> _CheckResult:
    ...
def _compute_expected_number_of_visits_exact(*args, **kwargs) -> _CheckResult:
    ...
def _compute_prob01states_double(model: ..., storm: ..., phi_states: ..., psi_states: ...) -> tuple[..., ...]:
    """
    Compute prob-0-1 states
    """
def _compute_prob01states_max_double(model: ..., storm: ..., phi_states: ..., psi_states: ...) -> tuple[..., ...]:
    """
    Compute prob-0-1 states (max)
    """
def _compute_prob01states_max_rationalfunc(*args, **kwargs) -> tuple[..., ...]:
    """
    Compute prob-0-1 states (max)
    """
def _compute_prob01states_min_double(model: ..., storm: ..., phi_states: ..., psi_states: ...) -> tuple[..., ...]:
    """
    Compute prob-0-1 states (min)
    """
def _compute_prob01states_min_rationalfunc(*args, **kwargs) -> tuple[..., ...]:
    """
    Compute prob-0-1 states (min)
    """
def _compute_prob01states_rationalfunc(*args, **kwargs) -> tuple[..., ...]:
    """
    Compute prob-0-1 states
    """
def _compute_steady_state_distribution_double(env: Environment, model: ..., storm: ...) -> _CheckResult:
    ...
def _compute_steady_state_distribution_exact(*args, **kwargs) -> _CheckResult:
    ...
def _construct_subsystem_Double(arg0: ..., storm: ..., arg1: ..., arg2: ..., arg3: bool, arg4: SubsystemBuilderOptions) -> SubsystemBuilderReturnTypeDouble:
    """
    build a subsystem of a sparse model
    """
def _construct_subsystem_Exact(*args, **kwargs) -> SubsystemBuilderReturnTypeExact:
    """
    build a subsystem of a sparse model
    """
def _construct_subsystem_RatFunc(*args, **kwargs) -> SubsystemBuilderReturnTypeRatFunc:
    """
    build a subsystem of a sparse model
    """
def _eliminate_end_components_double(matrix: ..., subsystem: ..., possible_ec_rows: ..., addSinkRowStates: ..., addSelfLoopAtSinkStates: bool) -> EndComponentEliminatorReturnTypeDouble:
    """
    Eliminate ECs in the subystem
    """
def _eliminate_non_markovian_chains(ma: ..., storm: ..., formulae: list[...], label_behavior: EliminationLabelBehavior) -> tuple[..., ..., list[...]]:
    """
    Eliminate chains of non-Markovian states in Markov automaton.
    """
def _eliminate_non_markovian_chains_parametric(*args, **kwargs) -> tuple[..., ..., ..., ..., ..., ..., ..., ..., list[...]]:
    """
    Eliminate chains of non-Markovian states in Markov automaton.
    """
def _exact_model_checking_fully_observable(*args, **kwargs) -> _CheckResult:
    ...
def _exact_model_checking_sparse_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform model checking using the sparse engine
    """
def _export_exact_to_drn(*args, **kwargs) -> None:
    """
    Export model in DRN format
    """
def _export_parametric_to_drn(*args, **kwargs) -> None:
    """
    Export parametric model in DRN format
    """
def _export_to_drn(model: ..., storm: ..., file: str, options: DirectEncodingOptions = ...) -> None:
    """
    Export model in DRN format
    """
def _export_to_drn_interval(model: ..., storm: ..., file: str, options: DirectEncodingOptions = ...) -> None:
    """
    Export model in DRN format
    """
def _get_reachable_states_double(model: ..., storm: ..., initial_states: ..., constraint_states: ..., target_states: ..., maximal_steps: int | None = None, choice_filter: ... | None = None) -> ...:
    ...
def _get_reachable_states_exact(*args, **kwargs) -> ...:
    ...
def _get_reachable_states_rf(*args, **kwargs) -> ...:
    ...
def _model_checking_dd_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform model checking using the dd engine
    """
def _model_checking_fully_observable(model: ..., storm: ..., task: CheckTask, environment: Environment = ...) -> _CheckResult:
    ...
def _model_checking_hybrid_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform model checking using the hybrid engine
    """
def _model_checking_sparse_engine(model: ..., storm: ..., task: CheckTask, environment: Environment = ...) -> _CheckResult:
    """
    Perform model checking using the sparse engine
    """
def _multi_objective_model_checking_double(model: ..., storm: ..., formula: ..., environment: Environment = ...) -> _CheckResult:
    """
    Run multi-objective model checking
    """
def _multi_objective_model_checking_exact(*args, **kwargs) -> _CheckResult:
    """
    Run multi-objective model checking
    """
def _parametric_model_checking_dd_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform parametric model checking using the dd engine
    """
def _parametric_model_checking_hybrid_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform parametric model checking using the hybrid engine
    """
def _parametric_model_checking_sparse_engine(*args, **kwargs) -> _CheckResult:
    """
    Perform parametric model checking using the sparse engine
    """
def _perform_bisimulation(model: ..., storm: ..., formulas: list[...], bisimulation_type: ...) -> ...:
    """
    Perform bisimulation
    """
def _perform_parametric_bisimulation(*args, **kwargs) -> ...:
    """
    Perform bisimulation on parametric model
    """
def _perform_symbolic_bisimulation(*args, **kwargs) -> ...:
    """
    Perform bisimulation
    """
def _perform_symbolic_parametric_bisimulation(*args, **kwargs) -> ...:
    """
    Perform bisimulation on parametric model
    """
def _set_up(arguments: str) -> None:
    """
    Initialize Storm
    """
def _transform_to_discrete_time_model(model: ..., storm: ..., formulae: list[...] = []) -> tuple[..., ..., list[...]]:
    """
    Transform continuous time model to discrete time model
    """
def _transform_to_discrete_time_parametric_model(*args, **kwargs) -> tuple[..., ..., ..., ..., ..., ..., ..., ..., list[...]]:
    """
    Transform parametric continuous time model to parametric discrete time model
    """
def _transform_to_sparse_model(*args, **kwargs) -> ...:
    """
    Transform symbolic model into sparse model
    """
def _transform_to_sparse_parametric_model(*args, **kwargs) -> ...:
    """
    Transform symbolic parametric model into sparse parametric model
    """
def build_sparse_exact_model_with_options(model_description: ..., options: ...) -> ...:
    """
    Build the model in sparse representation with exact number representation
    """
def build_sparse_model_from_explicit(transition_file: str, labeling_file: str, state_reward_file: str | None = '', transition_reward_file: str | None = '', choice_labeling_file: str | None = '') -> ...:
    """
    Build the model model from explicit input
    """
def build_sparse_model_with_options(model_description: ..., options: ...) -> ...:
    """
    Build the model in sparse representation
    """
def build_sparse_parametric_model_with_options(model_description: ..., options: ...) -> ...:
    """
    Build the model in sparse representation
    """
def check_interval_mdp(arg0: ..., storm: ..., arg1: CheckTask, arg2: Environment) -> _CheckResult:
    """
    Check interval MDP
    """
def compute_all_until_probabilities(arg0: Environment, arg1: CheckTask, arg2: ..., storm: ..., arg3: ..., arg4: ...) -> list[float]:
    """
    Compute forward until probabilities
    """
def compute_transient_probabilities(arg0: Environment, arg1: ..., storm: ..., arg2: ..., arg3: ..., arg4: float) -> list[float]:
    """
    Compute transient probabilities
    """
def create_filter_initial_states_sparse(model: ..., storm: ...) -> _QualitativeCheckResult:
    """
    Create a filter for the initial states on a sparse model
    """
def create_filter_initial_states_symbolic(*args, **kwargs) -> _QualitativeCheckResult:
    """
    Create a filter for the initial states on a symbolic model
    """
def create_filter_symbolic(*args, **kwargs) -> _QualitativeCheckResult:
    """
    Creates a filter for the given states and a symbolic model
    """
def install_signal_handlers(arg0: int) -> None:
    ...
def make_sparse_model_builder(*args, **kwargs) -> ...:
    """
    Construct a builder instance
    """
def make_sparse_model_builder_exact(*args, **kwargs) -> ...:
    """
    Construct a builder instance
    """
def make_sparse_model_builder_parametric(*args, **kwargs) -> ...:
    """
    Construct a builder instance
    """
def parse_constants_string(expression_manager: ..., definition_string: str) -> dict[..., ...]:
    """
    Parse constants definition
    """
def parse_jani_model(path: str) -> tuple[..., list[Property]]:
    """
    Parse Jani model
    """
def parse_jani_model_from_string(json_string: str) -> tuple[..., list[Property]]:
    """
    Parse Jani model from string
    """
def parse_prism_program(path: str, prism_compat: bool = False, simplify: bool = True) -> ...:
    """
    Parse Prism program
    """
def parse_properties_for_jani_model(formula_string: str, jani_model: ..., property_filter: set[str] | None = None) -> list[Property]:
    ...
def parse_properties_for_prism_program(formula_string: str, prism_program: ..., property_filter: set[str] | None = None) -> list[Property]:
    """
              Parses properties given in the prism format, allows references to variables in the prism program.
              
              :param str formula_str: A string of formulas
              :param PrismProgram prism_program: A prism program
              :param str property_filter: A filter
              :return: A list of properties
    """
def parse_properties_without_context(formula_string: str, property_filter: set[str] | None = None) -> list[Property]:
    """
              Parse properties given in the prism format.
              
              :param str formula_str: A string of formulas
              :param str property_filter: A filter
              :return: A list of properties
    """
def preprocess_symbolic_input(symbolic_model_description: ..., properties: list[Property], constant_definition_string: str) -> tuple[..., list[Property]]:
    """
    Preprocess symoblic input
    """
def reset_timeout() -> None:
    """
    Reset timeout
    """
def set_loglevel_debug() -> None:
    """
    set loglevel for storm to debug
    """
def set_loglevel_error() -> None:
    ...
def set_loglevel_trace() -> None:
    ...
def set_settings(arguments: list[str]) -> None:
    """
    Set settings
    """
def set_timeout(timeout: int) -> None:
    """
    Set timeout in seconds
    """
