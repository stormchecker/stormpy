import pytest

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestSimulator:
    def test_random_steps(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        dft.set_relevant_events(stormpy.dft.developer.RelevantEvents(), False)
        info = dft.build_state_generation_info(stormpy.dft.developer.DftSymmetries())
        generator = stormpy.dft.developer.RandomGenerator.create(5)
        simulator = stormpy.dft.developer.DFTTraceSimulator(dft, info, generator)
        assert type(simulator) is stormpy.dft.developer.DFTTraceSimulator[float]
        old_time = 0
        res = simulator.random_step()
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        assert simulator.get_time() - old_time > 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        assert simulator.get_time() - old_time > 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.SimulationStepResult.UNSUCCESSFUL
        assert simulator.get_time() - old_time <= 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.SimulationStepResult.UNSUCCESSFUL
        assert simulator.get_time() - old_time <= 0

    def test_simulate_trace_and(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        dft.set_relevant_events(stormpy.dft.developer.RelevantEvents(), False)
        info = dft.build_state_generation_info(stormpy.dft.developer.DftSymmetries())
        generator = stormpy.dft.developer.RandomGenerator.create(5)
        simulator = stormpy.dft.developer.DFTTraceSimulator(dft, info, generator)
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.SUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.UNSUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.UNSUCCESSFUL

    def test_simulate_trace_rc(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        dft.set_relevant_events(stormpy.dft.developer.RelevantEvents(), False)
        info = dft.build_state_generation_info(stormpy.dft.developer.DftSymmetries())
        generator = stormpy.dft.developer.RandomGenerator.create(5)
        simulator = stormpy.dft.developer.DFTTraceSimulator(dft, info, generator)
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.UNSUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.SUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.SimulationTraceResult.UNSUCCESSFUL

    def test_steps(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        dft.set_relevant_events(stormpy.dft.developer.RelevantEvents(), False)
        info = dft.build_state_generation_info(stormpy.dft.developer.DftSymmetries())
        generator = stormpy.dft.developer.RandomGenerator.create(5)
        simulator = stormpy.dft.developer.DFTTraceSimulator(dft, info, generator)

        failable_check = ["B", "C"]
        a = dft.get_element_by_name("A").id
        b = dft.get_element_by_name("B").id
        c = dft.get_element_by_name("C").id

        state = simulator.get_state()
        assert state.is_operational(a)
        assert not state.has_failed(a)
        assert state.is_operational(b)
        assert not state.has_failed(b)
        assert state.is_operational(c)
        assert not state.has_failed(c)

        # Let C fail
        failable = state.get_failable_elements()
        for f in failable:
            assert not f.is_due_dependency()
            fail_be = f.as_be(dft)
            assert fail_be.name in failable_check
            if fail_be.name == "C":
                next_fail = f
        res = simulator.step(next_fail)
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        state = simulator.get_state()
        assert state.is_operational(a)
        assert not state.has_failed(a)
        assert state.is_operational(b)
        assert not state.has_failed(b)
        assert not state.is_operational(c)
        assert state.has_failed(c)

        # Let B fail
        state = simulator.get_state()
        failable = state.get_failable_elements()
        for f in failable:
            assert not f.is_due_dependency()
            fail_be = f.as_be(dft)
            assert fail_be.name == "B"
            next_fail = f
        res = simulator.step(next_fail)
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        state = simulator.get_state()
        assert not state.is_operational(a)
        assert state.has_failed(a)
        assert not state.is_operational(b)
        assert state.has_failed(b)
        assert not state.is_operational(c)
        assert state.has_failed(c)

        failable = state.get_failable_elements()
        for f in failable:
            assert False  # no failable elements

    def test_steps_dependency(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "fdep.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        dft.set_relevant_events(stormpy.dft.developer.RelevantEvents(), False)
        info = dft.build_state_generation_info(stormpy.dft.developer.DftSymmetries())
        generator = stormpy.dft.developer.RandomGenerator.create(5)
        simulator = stormpy.dft.developer.DFTTraceSimulator(dft, info, generator)

        p = dft.get_element_by_name("P").id
        b = dft.get_element_by_name("B").id
        power = dft.get_element_by_name("B_Power").id

        state = simulator.get_state()
        assert state.is_operational(p)
        assert state.is_operational(b)
        assert state.is_operational(power)

        # Let B_Power fail
        failable = state.get_failable_elements()
        for f in failable:
            assert not f.is_due_dependency()
            fail_be = f.as_be(dft)
            assert fail_be.name in ["B", "P", "B_Power"]
            if fail_be.name == "B_Power":
                next_fail = f
        res = simulator.step(next_fail)
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        state = simulator.get_state()
        assert state.is_operational(p)
        assert state.is_operational(b)
        assert state.has_failed(power)

        # Let B fail
        failable = state.get_failable_elements()
        for f in failable:
            assert f.is_due_dependency()
            fail_dependency = f.as_dependency(dft)
            assert len(fail_dependency.dependent_events) == 1
            fail_be = fail_dependency.dependent_events[0]
            assert fail_be.name in ["B", "P"]
            if fail_be.name == "B":
                next_fail = f
        res = simulator.step(next_fail)
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        state = simulator.get_state()
        assert state.has_failed(p)
        assert state.has_failed(b)
        assert state.has_failed(power)

        failable = state.get_failable_elements()
        for f in failable:
            assert False  # no failable elements

    def test_random_fail(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)
        assert not simulator.is_failed()
        assert not simulator.is_done()
        assert simulator.random_fail() == stormpy.dft.SimulationStepResult.SUCCESSFUL
        assert not simulator.is_done()
        assert simulator.random_fail() == stormpy.dft.SimulationStepResult.SUCCESSFUL
        assert simulator.is_failed()
        assert simulator.is_done()
        # No further BE can fail
        assert simulator.random_fail() == stormpy.dft.SimulationStepResult.UNSUCCESSFUL

    def test_simulate_traces(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)
        successes = simulator.simulate_traces(2, 3)
        assert successes == 1

    def test_let_fail(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)

        assert not simulator.is_next_dependency_failure()
        candidates = simulator.next_failures()
        assert set(candidates) == {"B", "C"}

        simulator.let_fail("C")
        assert not simulator.is_failed()
        assert simulator.next_failures() == ["B"]

        simulator.let_fail("B")
        assert simulator.is_failed()
        assert simulator.is_done()
        dft_state, element_states = simulator.status()
        assert dft_state == "DFT is Failed"
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        assert statuses_by_name["A"] == "Failed"
        assert statuses_by_name["B"] in ("Failed", "Don't Care")
        assert statuses_by_name["C"] in ("Failed", "Don't Care")

    def test_let_fail_dependency(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "fdep.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)

        assert not simulator.is_next_dependency_failure()
        candidates = simulator.next_failures()
        assert set(candidates) == {"B", "P", "B_Power"}

        simulator.let_fail("B_Power")
        assert simulator.is_next_dependency_failure()

        simulator.let_fail("B")
        assert simulator.is_failed()
        _, element_states = simulator.status()
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        assert statuses_by_name["P"] in ("Failed", "Don't Care")
        assert statuses_by_name["B"] in ("Failed", "Don't Care")
        assert statuses_by_name["B_Power"] in ("Failed", "Don't Care")
        assert statuses_by_name["System"] == "Failed"

    def test_let_fail_fdep_unsuccessful_raises(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "fdep.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)

        simulator.let_fail("B_Power")
        assert simulator.is_next_dependency_failure()
        with pytest.raises(ValueError):
            simulator.let_fail("B", dependency_successful=False)

    def test_let_fail_dependency_unsuccessful(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "pdep.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)

        simulator.let_fail("B_Power")
        assert simulator.is_next_dependency_failure()
        candidates = simulator.next_failures()
        assert len(candidates) == 1
        dependent_be = candidates[0]

        simulator.let_fail(dependent_be, dependency_successful=False)
        assert not simulator.is_failed()
        _, element_states = simulator.status()
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        assert statuses_by_name[dependent_be] != "Failed"

    def test_let_fail_unknown_be_raises(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)
        with pytest.raises(ValueError):
            simulator.let_fail("NonExistentBE")

    def test_nr_next_failures(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)
        assert simulator.nr_next_failures() == len(simulator.next_failures()) == 2

        simulator.let_fail("C")
        assert simulator.nr_next_failures() == len(simulator.next_failures()) == 1

    def test_reset(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)
        initial_candidates = set(simulator.next_failures())

        simulator.let_fail("C")
        assert not simulator.is_failed()
        assert set(simulator.next_failures()) != initial_candidates

        simulator.reset()
        assert not simulator.is_failed()
        assert set(simulator.next_failures()) == initial_candidates

    def test_constructor_relevant_events(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5, relevant_events=["B"])

        simulator.let_fail("C")
        simulator.let_fail("B")
        assert simulator.is_failed()
        _, element_states = simulator.status()
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        # "B" was marked as an additional relevant event, so it must not be collapsed into "Don't Care"
        assert statuses_by_name["B"] == "Failed"

    def test_status_spare_usage(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5, relevant_events=["n137", "n139", "n9"])

        _, element_states = simulator.status()
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        initial_status = statuses_by_name["n137"]
        assert "not using anything" in initial_status or "currently using" in initial_status

        # Fail the primary component of the spare pool, forcing a claim of the spare
        simulator.let_fail("n139")
        _, element_states = simulator.status()
        statuses_by_name = {element.name: status for element, status in element_states.items()}
        assert "currently using n9" in statuses_by_name["n137"]

    def test_let_fail_seq_violation_invalid(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "seq.dft"))
        simulator = stormpy.dft.DFTSimulator(dft, seed=5)

        res = simulator.let_fail("Second1")
        assert res == stormpy.dft.SimulationStepResult.SUCCESSFUL
        res = simulator.let_fail("Second2")
        assert res == stormpy.dft.SimulationStepResult.INVALID
