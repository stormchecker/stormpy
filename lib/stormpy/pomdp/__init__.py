from stormpy import _config

if not _config.storm_with_pomdp:
    raise ImportError("No support for POMDPs was built in Storm.")

from . import pomdp
from .pomdp import *


def make_canonic(model):
    """
    Make the POMDP canonic
    :param model:
    :return:
    """

    if model.supports_parameters:
        return pomdp._make_canonic_Rf(model)
    else:
        return pomdp._make_canonic_Double(model)


def make_simple(model, keep_state_valuations=False):
    """
    Make the POMDP simple (aka alternating), i.e., each state has at most two actions, and if there is nondeterminism, then there is no probabilistic branching,

    :param model:
    :return:
    """
    if model.supports_parameters:
        return pomdp._make_simple_Rf(model, keep_state_valuations)
    else:
        return pomdp._make_simple_Double(model, keep_state_valuations)


def unfold_memory(model, memory, add_memory_labels=False, keep_state_valuations=False):
    """
    Unfold the memory for an FSC into the POMDP

    :param model: A pomdp
    :param memory: A memory structure
    :return: A pomdp that contains states from the product of the original POMDP and the FSC Memory
    """
    if model.supports_parameters:
        return pomdp._unfold_memory_Rf(model, memory, add_memory_labels, keep_state_valuations)
    else:
        return pomdp._unfold_memory_Double(model, memory, add_memory_labels, keep_state_valuations)


def apply_unknown_fsc(model, mode):
    if model.supports_parameters:
        return pomdp._apply_unknown_fsc_Rf(model, mode)
    else:
        return pomdp._apply_unknown_fsc_Double(model, mode)


def create_nondeterminstic_belief_tracker(model, reduction_timeout, track_timeout):
    """

    :param model: A POMDP
    :param reduction_timeout: timeout in milliseconds for the reduction algorithm, 0 for no timeout.
    :return:
    """
    if model.is_exact:
        opts = NondeterministicBeliefTrackerExactSparseOptions()
        opts.reduction_timeout = reduction_timeout
        opts.track_timeout = track_timeout
        return pomdp.NondeterministicBeliefTrackerExactSparse(model, opts)
    else:
        opts = NondeterministicBeliefTrackerDoubleSparseOptions()
        opts.reduction_timeout = reduction_timeout
        opts.track_timeout = track_timeout
        return pomdp.NondeterministicBeliefTrackerDoubleSparse(model, opts)


def create_observation_trace_unfolder(model, risk_assessment, expr_manager, rejection_sampling=True):
    """

    :param model:
    :param risk_assessment:
    :param expr_manager:
    :param rejection_sampling:
    :return:
    """
    options = pomdp.ObservationTraceUnfolderOptions()
    options.rejection_sampling = rejection_sampling
    if model.is_exact:
        return pomdp.ObservationTraceUnfolderExact(model, risk_assessment, expr_manager, options)
    else:
        return pomdp.ObservationTraceUnfolderDouble(model, risk_assessment, expr_manager, options)
