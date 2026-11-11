import math
import os
import signal
import threading
import time

import pytest
import stormpy
from helpers.helper import get_example_path

# Time after which SIGINT is sent to the running computation
INTERRUPT_DELAY = 0.5
# Upper bound on the time until the computation must have been aborted
ABORT_TIMEOUT = 5


def _random_walk(n):
    """Return model of random walk of the given size and the property to reach its upper end."""
    program = stormpy.parse_prism_program(get_example_path("dtmc", "random_walk.pm"))
    prop = stormpy.parse_property('P=? [F "goal"]', program)
    program, props = stormpy.instantiate_constants(program, {"N": n}, prop)
    return program, props[0]


def _interrupt_after(delay):
    """Send SIGINT to the process after the given delay (in seconds)."""
    timer = threading.Timer(delay, lambda: os.kill(os.getpid(), signal.SIGINT))
    timer.start()
    return timer


def _power_iteration_environment(model):
    """Environment using (slowly converging) power iteration with large iteration limit."""
    env = stormpy.environments.default(model)
    env.solver().set_linear_equation_solver_type(stormpy.environments.EquationSolverType.NATIVE)
    env.solver().native().method = stormpy.environments.NativeLinearEquationSolverMethod.POWER
    env.solver().native().maximal_number_of_iterations = 2**40
    return env


def _assert_small_model_checking_works():
    program, prop = _random_walk(10)
    model = stormpy.build_model(program, prop)
    result = stormpy.model_checking(model, prop)
    assert math.isclose(result[model.initial_states[0]], 0.5, rel_tol=1e-4)


@pytest.mark.skipif(threading.current_thread() is not threading.main_thread(), reason="Signals are only handled on the main thread")
class TestInterrupt:
    def test_interrupt_model_building(self):
        # Exploring this model takes a long time
        program, prop = _random_walk(100000000)
        timer = _interrupt_after(INTERRUPT_DELAY)
        start = time.monotonic()
        try:
            with pytest.raises(KeyboardInterrupt):
                stormpy.build_model(program, prop)
        finally:
            timer.cancel()
        assert time.monotonic() - start < ABORT_TIMEOUT
        _assert_small_model_checking_works()

    def test_interrupt_model_checking(self, capfd):
        # Power iteration converges very slowly on this model
        program, prop = _random_walk(20000)
        model = stormpy.build_model(program, prop)
        env = _power_iteration_environment(model)
        result = None
        # Warning about the aborted solver is needed below
        previous_log_level = stormpy.developer.get_log_level()
        stormpy.developer.set_log_level(stormpy.developer.LogLevel.WARN)
        capfd.readouterr()  # Discard previous output
        timer = _interrupt_after(INTERRUPT_DELAY)
        start = time.monotonic()
        try:
            with pytest.raises(KeyboardInterrupt):
                result = stormpy.model_checking(model, prop, environment=env)
        finally:
            timer.cancel()
            stormpy.developer.set_log_level(previous_log_level)
        assert time.monotonic() - start < ABORT_TIMEOUT
        out, err = capfd.readouterr()
        assert "Iterative solver was aborted" in out + err
        # The result is discarded instead of being returned
        assert result is None
        _assert_small_model_checking_works()

    def test_custom_signal_handler_does_not_abort(self):
        # A Python signal handler which does not raise must not abort the computation
        delay = 0.2
        program, prop = _random_walk(2000)
        model = stormpy.build_model(program, prop)
        env = _power_iteration_environment(model)

        # Times at which the handler was invoked
        handled = []
        previous = signal.signal(signal.SIGINT, lambda signum, frame: handled.append(time.monotonic()))
        try:
            timer = _interrupt_after(delay)
            start = time.monotonic()
            result = stormpy.model_checking(model, prop, environment=env)
            end = time.monotonic()
            timer.join()
        finally:
            signal.signal(signal.SIGINT, previous)

        assert end - start > delay, "Model checking finished before the signal was sent"
        assert len(handled) == 1
        # The handler was invoked during the computation, via the termination callback
        assert start < handled[0] < end
        assert math.isclose(result[model.initial_states[0]], 0.5, rel_tol=1e-3)
