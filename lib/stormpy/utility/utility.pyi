"""
Utilities for Storm
"""
from __future__ import annotations
import stormpy.pycarl.gmp
import typing
__all__ = ['JsonContainerDouble', 'JsonContainerRational', 'MatrixFormat', 'ModelReference', 'Path', 'ShortestPathsGenerator', 'SmtCheckResult', 'SmtSolver', 'SmtSolverFactory', 'Z3SmtSolver', 'Z3SmtSolverFactory', 'milliseconds', 'sharpen']
class JsonContainerDouble:
    """
    Storm-internal container for JSON structures
    """
    @staticmethod
    def __eq__(s, o):
        ...
    @staticmethod
    def __hash__(s):
        ...
    @staticmethod
    def __int__(s):
        ...
    def __getitem__(self, arg0: str) -> JsonContainerDouble:
        ...
    def __str__(self) -> str:
        ...
class JsonContainerRational:
    """
    Storm-internal container for JSON structures
    """
    @staticmethod
    def __eq__(s, o):
        ...
    @staticmethod
    def __hash__(s):
        ...
    @staticmethod
    def __int__(s):
        ...
    def __getitem__(self, arg0: str) -> JsonContainerRational:
        ...
    def __str__(self) -> str:
        ...
class MatrixFormat:
    """
    Members:
    
      Straight
    
      I_Minus_P
    """
    I_Minus_P: typing.ClassVar[MatrixFormat]  # value = <MatrixFormat.I_Minus_P: 1>
    Straight: typing.ClassVar[MatrixFormat]  # value = <MatrixFormat.Straight: 0>
    __members__: typing.ClassVar[dict[str, MatrixFormat]]  # value = {'Straight': <MatrixFormat.Straight: 0>, 'I_Minus_P': <MatrixFormat.I_Minus_P: 1>}
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
class ModelReference:
    """
    Lightweight Wrapper around results
    """
    def get_boolean_value(self, variable: ...) -> bool:
        """
        get a value for a boolean variable
        """
    def get_integer_value(self, variable: ...) -> int:
        """
        get a value for an integer variable
        """
    def get_rational_value(self, variable: ...) -> float:
        """
        get a value (as double) for an rational variable
        """
class Path:
    __hash__: typing.ClassVar[None] = None
    distance: float
    predecessorK: int
    predecessorNode: int | None
    def __eq__(self, arg0: Path) -> bool:
        """
        Compares predecessor node and index, ignoring distance
        """
    @typing.overload
    def __init__(self, predecessorNode: int, predecessorK: int, distance: float) -> None:
        ...
    @typing.overload
    def __init__(self, predecessorK: int, distance: float) -> None:
        ...
class ShortestPathsGenerator:
    @typing.overload
    def __init__(self, model: ..., storm: ..., target_bitvector: ...) -> None:
        ...
    @typing.overload
    def __init__(self, model: ..., storm: ..., target_state: int) -> None:
        ...
    @typing.overload
    def __init__(self, model: ..., storm: ..., target_state_list: list[int]) -> None:
        ...
    @typing.overload
    def __init__(self, model: ..., storm: ..., target_label: str) -> None:
        ...
    @typing.overload
    def __init__(self, transition_matrix: ..., target_prob_vector: list[float], initial_states: ..., matrix_format: MatrixFormat) -> None:
        ...
    @typing.overload
    def __init__(self, transition_matrix: ..., target_prob_map: dict[int, float], initial_states: ..., matrix_format: MatrixFormat) -> None:
        ...
    def get_distance(self, k: int) -> float:
        ...
    def get_path_as_list(self, k: int) -> list[int]:
        ...
    def get_states(self, k: int) -> ...:
        ...
class SmtCheckResult:
    """
    Result type
    
    Members:
    
      Sat
    
      Unsat
    
      Unknown
    """
    Sat: typing.ClassVar[SmtCheckResult]  # value = <SmtCheckResult.Sat: 0>
    Unknown: typing.ClassVar[SmtCheckResult]  # value = <SmtCheckResult.Unknown: 2>
    Unsat: typing.ClassVar[SmtCheckResult]  # value = <SmtCheckResult.Unsat: 1>
    __members__: typing.ClassVar[dict[str, SmtCheckResult]]  # value = {'Sat': <SmtCheckResult.Sat: 0>, 'Unsat': <SmtCheckResult.Unsat: 1>, 'Unknown': <SmtCheckResult.Unknown: 2>}
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
class SmtSolver:
    """
    Generic Storm SmtSolver Wrapper
    """
    def add(self, arg0: ...) -> None:
        """
        addconstraint
        """
    def check(self) -> SmtCheckResult:
        """
        check
        """
    def pop(self, levels: int) -> None:
        """
        pop
        """
    def push(self) -> None:
        """
        push
        """
    def reset(self) -> None:
        """
        reset
        """
    @property
    def model(self) -> ModelReference:
        """
        get the model
        """
class SmtSolverFactory:
    """
    Factory for creating SMT Solvers
    """
class Z3SmtSolver(SmtSolver):
    """
    z3 API for storm smtsolver wrapper
    """
    def __init__(self, arg0: ...) -> None:
        ...
class Z3SmtSolverFactory(SmtSolverFactory):
    """
    Factory for creating z3 based SMT solvers
    """
    def __init__(self) -> None:
        ...
class milliseconds:
    def __str__(self) -> str:
        ...
    def count(self) -> int:
        ...
def sharpen(precision: int, value: float) -> stormpy.pycarl.gmp.Rational:
    """
    Convert a float to the nearest rational within precision using Kwek Mehlhorn
    """
