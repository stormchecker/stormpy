from stormpy.info import _config

if not _config.STORM_WITH_DFT:
    raise ImportError("No support for DFTs was built in Storm.")

from . import _dft
from ._dft import *
from .modules import modules_json

_dft._set_up()


def analyze_dft(ft, properties, symred=True, allow_modularisation=False, relevant_events=RelevantEvents(), allow_dc_for_relevant=False):
    if isinstance(ft, DFT_double):
        return _dft._analyze_dft_double(ft, properties, symred, allow_modularisation, relevant_events, allow_dc_for_relevant)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._analyze_dft_ratfunc(ft, properties, symred, allow_modularisation, relevant_events, allow_dc_for_relevant)


def build_model(ft, symmetries=DftSymmetries(), relevant_events=RelevantEvents(), allow_dc_for_relevant=False):
    if isinstance(ft, DFT_double):
        return _dft._build_model_double(ft, symmetries, relevant_events, allow_dc_for_relevant)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._build_model_ratfunc(ft, symmetries, relevant_events, allow_dc_for_relevant)


def transform_dft(ft, unique_constant_be, binary_fdeps, exponential_distributions):
    if isinstance(ft, DFT_double):
        return _dft._transform_dft_double(ft, unique_constant_be, binary_fdeps, exponential_distributions)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._transform_dft_ratfunc(ft, unique_constant_be, binary_fdeps, exponential_distributions)


def compute_dependency_conflicts(ft, use_smt=False, solver_timeout=0):
    if isinstance(ft, DFT_double):
        return _dft._compute_dependency_conflicts_double(ft, use_smt, solver_timeout)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._compute_dependency_conflicts_ratfunc(ft, use_smt, solver_timeout)


def prepare_for_analysis(ft):
    compute_dependency_conflicts(ft, use_smt=False)
    return transform_dft(ft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)


def is_well_formed(ft, check_valid_for_analysis=True):
    if isinstance(ft, DFT_double):
        return _dft._is_well_formed_double(ft, check_valid_for_analysis)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._is_well_formed_ratfunc(ft, check_valid_for_analysis)


def has_potential_modeling_issues(ft):
    if isinstance(ft, DFT_double):
        return _dft._has_potential_modeling_issues_double(ft)
    else:
        assert isinstance(ft, DFT_ratfunc)
        return _dft._has_potential_modeling_issues_ratfunc(ft)
