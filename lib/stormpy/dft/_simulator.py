"""Simulator for Dynamic Fault Trees."""

from collections.abc import Iterable

from . import developer
from . import DFT, DFTElement

# Import classes from developer
SimulationStepResult = developer.SimulationStepResult
SimulationTraceResult = developer.SimulationTraceResult


class DFTSimulator:
    """
    High-level simulator for Dynamic Fault Trees.

    Wraps :class:`stormpy.dft.developer.DFTTraceSimulator`: builds the random
    number generator and state-generation information automatically, and
    resolves failable elements to their BE/dependency names.
    """

    def __init__(self, dft: DFT, seed: int = 42, relevant_events: Iterable[str] | None = None) -> None:
        """
        Create simulator.

        :param dft: DFT to simulate.
        :param seed: Seed for the pseudo-random number generator.
        :param relevant_events: Additional names to mark as relevant events (beyond the top-level event),
            or ``None``.
        """
        self._dft = dft
        # Set only top event as relevant (plus any additionally requested events)
        relevant_events = developer.compute_relevant_events([], additional_relevant_names=relevant_events or [])
        self._dft.set_relevant_events(relevant_events, False)
        # Create information for state space generation
        info = self._dft.build_state_generation_info(developer.DftSymmetries())
        # Initialize random generator
        generator = developer.RandomGenerator.create(seed)
        # Create simulator
        self._simulator = developer.DFTTraceSimulator(self._dft, info, generator)
        # Select the value-type-specific methods once to avoid pybind11 overload
        # resolution for every failable element in every simulation step.
        failable_element = developer.FailableElement
        if developer.DFT.parameters_of(self._dft) == (float,):
            self._as_be = failable_element.as_be_double
            self._as_dependency = failable_element.as_dependency_double
        else:
            self._as_be = failable_element.as_be_ratfunc
            self._as_dependency = failable_element.as_dependency_ratfunc
        # Initialize variables
        self._state = None
        self._fail_candidates = dict()
        self._is_failable_dependency = False
        self._failed = False
        self._update()

    def status(self) -> tuple[str, dict[DFTElement, str]]:
        """
        Get current status of DFT elements.

        :return: Tuple (overall status, dict element -> status).
        """
        if self._state.is_invalid():
            return "State is invalid because a SEQ is violated", dict()

        dft_state = "DFT is {}".format("Failed" if self.is_failed() else "Operational")
        element_states = dict()
        for i in range(self._dft.nr_elements()):
            # Order of checks is important!
            if self._state.is_operational(i):
                status = "Operational"
            elif self._state.dont_care(i):
                status = "Don't Care"
            elif self._state.is_failsafe(i):
                status = "FailSafe"
            elif self._state.has_failed(i):
                status = "Failed"
            else:
                status = "Unknown"
            elem = self._dft.get_element(i)
            if elem.type == developer.DFTElementType.SPARE:
                cur_used = self._state.spare_uses(i)
                if cur_used == i:
                    status += ", not using anything"
                else:
                    elem_used = self._dft.get_element(cur_used)
                    status += ", currently using {}".format(elem_used.name)
            element_states[elem] = status
        return dft_state, element_states

    def nr_next_failures(self) -> int:
        """
        Returns the number of possible BEs which can fail next.

        :return: Number of possible BE failures.
        """
        return len(self._fail_candidates)

    def next_failures(self) -> list[str]:
        """
        Returns the BEs which can fail next.

        :return: Names of the BEs which can fail next.
        """
        return list(self._fail_candidates.keys())

    def is_next_dependency_failure(self) -> bool:
        """
        Returns whether the next failure is due to a dependency (or the BE failing on its own).

        :return: True iff the failure is triggered by a dependency.
        """
        return self._is_failable_dependency

    def _update(self) -> None:
        """
        Update the internal state.
        """
        # Update state
        self._state = self._simulator.get_state()
        self._failed = self._state.has_failed(self._dft.top_level_element.id)
        # Compute next failures
        self._fail_candidates.clear()
        self._is_failable_dependency = False
        for f in self._state.get_failable_elements():
            if f.is_due_dependency():
                self._is_failable_dependency = True
                fail_dependency = self._as_dependency(f, self._dft)
                fail_be = fail_dependency.dependent_events[0]
                self._fail_candidates[fail_be.name] = f
            else:
                fail_be = self._as_be(f, self._dft)
                self._fail_candidates[fail_be.name] = f

    def let_fail(self, be: str, dependency_successful: bool = True) -> SimulationStepResult:
        """
        Let the given BE fail next.
        If the BE fails due to a probabilistic dependency, this failure forwarding can be either successful or unsuccessful.

        :param be: Name of the BE which should fail next.
        :param dependency_successful: Whether the failure forwarding of the dependency was successful.
        :return: Result of the step (successful, unsuccessful, invalid).
        :raises ValueError: If ``be`` cannot fail, or if ``dependency_successful=False`` is given for a
            failure that is not due to a dependency or that is due to an FDEP.
        """
        if be not in self._fail_candidates:
            raise ValueError(f"BE {be} cannot fail.")

        failable = self._fail_candidates[be]
        if not dependency_successful:
            if not failable.is_due_dependency():
                raise ValueError(f"BE {be} does not fail due to a dependency; 'dependency_successful' is not applicable.")
            if self._as_dependency(failable, self._dft).is_fdep:
                raise ValueError(f"BE {be} fails due to an FDEP, which always succeeds; 'dependency_successful=False' is not supported.")

        res = self._simulator.step(failable, dependency_success=dependency_successful)
        self._update()
        return res

    def random_fail(self) -> SimulationStepResult:
        """
        Let a random BE fail next.
        The next BE is chosen according their associated failure probability.

        :return: Result of the step (successful, unsuccessful, invalid).
        """
        res = self._simulator.random_step()
        self._update()
        return res

    def simulate_traces(self, timebound: float, nr_traces: int) -> int:
        """
        Simulate a number of traces via Monte Carlo simulation and check how many led to an overall failure within the given timebound.

        :param timebound: Time bound up till which traces are simulated.
        :param nr_traces: The number of traces to simulate.
        :return: The number of traces which led to an overall failure.
        """
        self.reset()
        success = 0
        for i in range(nr_traces):
            res = self._simulator.simulate_trace(timebound)
            if res == SimulationTraceResult.SUCCESSFUL:
                success += 1
        self.reset()
        return success

    def reset(self) -> None:
        """
        Reset the simulator to the initial state.
        """
        self._simulator.reset()
        self._update()

    def is_failed(self) -> bool:
        """
        Whether the DFT is failed.

        :return: True iff if the top level event is failed.
        """
        return self._failed

    def is_done(self) -> bool:
        """
        Whether the simulation has ended in a sink state.
        A sink state can either be that the DFT is failed, the state is invalid or no further failures are possible anymore.

        :return: True iff the simulation has ended.
        """
        return self.is_failed() or self._state.is_invalid() or self.nr_next_failures() == 0
