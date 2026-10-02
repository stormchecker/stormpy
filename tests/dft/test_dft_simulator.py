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
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
        assert simulator.get_time() - old_time > 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
        assert simulator.get_time() - old_time > 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.developer.SimulationStepResult.UNSUCCESSFUL
        assert simulator.get_time() - old_time <= 0
        old_time = simulator.get_time()
        res = simulator.random_step()
        assert res == stormpy.dft.developer.SimulationStepResult.UNSUCCESSFUL
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
        assert res == stormpy.dft.developer.SimulationTraceResult.UNSUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.developer.SimulationTraceResult.SUCCESSFUL
        res = simulator.simulate_trace(2)
        assert res == stormpy.dft.developer.SimulationTraceResult.UNSUCCESSFUL

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
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
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
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
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
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
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
        assert res == stormpy.dft.developer.SimulationStepResult.SUCCESSFUL
        state = simulator.get_state()
        assert state.has_failed(p)
        assert state.has_failed(b)
        assert state.has_failed(power)

        failable = state.get_failable_elements()
        for f in failable:
            assert False  # no failable elements
