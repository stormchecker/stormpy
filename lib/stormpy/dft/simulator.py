import stormpy
import stormpy.dft


class DftSimulator:
    """
    Simulator for DFT.
    Adds convenience function to stormpy.dft.Simulator.
    """

    def __init__(self, dft, seed=42, relevant=[]):
        """
        Create simulator.

        :param dft: DFT.
        :param seed: Seed for random number generator.
        :param relevant: List of relevant events. 'all' sets all events as relevant.
        """
        self._dft = dft
        # Set only top event as relevant
        relevant_events = stormpy.dft.compute_relevant_events([], additional_relevant_names=relevant)
        self._dft.set_relevant_events(relevant_events, False)
        # Create information for state space generation
        info = self._dft.state_generation_info()
        # Initialize random generator
        generator = stormpy.dft.RandomGenerator.create(seed)
        # Create simulator
        self._simulator = stormpy.dft.DFTSimulator(self._dft, info, generator)
        # Initialize variables
        self._state = None
        self._fail_candidates = dict()
        self._is_failable_dependency = False
        self._failed = False
        self._update()

    def status(self):
        """
        Get current status of DFT elements.

        :return: Dictionary elements -> status.
        """
        if self._state.invalid():
            return "State is invalid because a SEQ is violated", dict()

        dft_state = "DFT is {}".format("Failed" if self.is_failed() else "Operational")
        element_states = dict()
        for i in range(self._dft.nr_elements()):
            # Order of checks is important!
            if self._state.operational(i):
                status = "Operational"
            elif self._state.dontcare(i):
                status = "Don't Care"
            elif self._state.failsafe(i):
                status = "FailSafe"
            elif self._state.failed(i):
                status = "Failed"
            else:
                status = "Unknown"
            elem = self._dft.get_element(i)
            if elem.type == stormpy.dft.DFTElementType.SPARE:
                cur_used = self._state.spare_uses(i)
                if cur_used == i:
                    status += ", not using anything"
                else:
                    elem_used = self._dft.get_element(cur_used)
                    status += ", currently using {}".format(elem_used.name)
            element_states[elem] = status
        return dft_state, element_states

    def nr_next_failures(self):
        """
        Returns the number of possible BEs which can fail next.

        :return: Number of possible BE failures.
        """
        return len(self._fail_candidates)

    def next_failures(self):
        """
        Returns the BEs which can fail next.

        :return: Names of the BEs which can fail next.
        """
        return list(self._fail_candidates.keys())

    def is_next_dependency_failure(self):
        """
        Returns whether the next failure is due to a dependency (or the BE failing on its own).

        :return: True iff the failure is triggered by a dependency.
        """
        return self._is_failable_dependency

    def _update(self):
        """
        Update the internal state.
        """
        # Update state
        self._state = self._simulator.get_state()
        self._failed = self._state.failed(self._dft.top_level_element.id)
        # Compute next failures
        self._fail_candidates.clear()
        self._is_failable_dependency = False
        for f in self._state.failable():
            if f.is_due_dependency():
                self._is_failable_dependency = True
                fail_dependency = f.as_dependency(self._dft)
                fail_be = fail_dependency.dependent_events[0]
                self._fail_candidates[fail_be.name] = f
            else:
                fail_be = f.as_be(self._dft)
                self._fail_candidates[fail_be.name] = f

    def let_fail(self, be, dependency_successful=True):
        """
        Let the given BE fail next.
        If the BE fails due to a probabilistic dependency, this failure forwarding can be either successful or unsuccessful.

        :param be: Name of the BE which should fail next.
        :param dependency_successful: Whether the failure forwarding of the dependency was successful.
        :return: Result of the step (successful, unsuccessful, invalid).
        """
        if be not in self._fail_candidates:
            raise ValueError(f"BE {be} cannot fail.")

        res = self._simulator.step(self._fail_candidates[be], dependency_success=dependency_successful)
        self._update()
        return res

    def random_fail(self):
        """
        Let a random BE fail next.
        The next BE is chosen according their associated failure probability.

        :return: Result of the step (successful, unsuccessful, invalid).
        """
        res = self._simulator.random_step()
        self._update()
        return res

    def simulate_traces(self, timebound, nr_traces):
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
            if res == stormpy.dft.SimulationTraceResult.SUCCESSFUL:
                success += 1
        self.reset()
        return success

    def reset(self):
        """
        Reset the simulator to the initial state.
        """
        self._simulator.reset()
        self._update()

    def is_failed(self):
        """
        Whether the DFT is failed.

        :return: True iff if the top level event is failed.
        """
        return self._failed

    def is_done(self):
        """
        Whether the simulation has ended in a sink state.
        A sink state can either be that the DFT is failed, the state is invalid or no further failures are possible anymore.

        :return: True iff the simulation has ended.
        """
        return self.is_failed() or self._state.invalid() or self.nr_next_failures() == 0
