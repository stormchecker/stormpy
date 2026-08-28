import stormpy
import stormpy.simulator
from helpers.helper import get_example_path

import random


class TestSparseModelSimulator:
    def test_simulate_die_steps(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        model = stormpy.build_model(prism_program)
        simulator = stormpy.simulator.create_simulator(model, seed=42)

        assert model.labeling.get_labels_of_state(11) == {"done", "five"}
        # Perform 3 steps
        # each steps returns (state, reward, labels)
        assert simulator.restart() == (0, [0.0], {"init"})
        assert simulator.step() == (2, [1.0], set())
        assert simulator.step() == (5, [1.0], set())
        assert simulator.step() == (11, [1.0], {"done", "five"})
        assert simulator.step() == (11, [0.0], {"done", "five"})
        assert simulator.step() == (11, [0.0], {"done", "five"})
        assert simulator.is_done()

    def test_simulate_die(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        model = stormpy.build_model(prism_program)
        simulator = stormpy.simulator.create_simulator(model, seed=42)

        final_outcomes = dict()
        for n in range(10):
            assert not simulator.is_done()
            while not simulator.is_done():
                observation, reward, labels = simulator.step()
            assert len(labels) == 2
            assert "done" in labels
            if observation not in final_outcomes:
                final_outcomes[observation] = 1
            else:
                final_outcomes[observation] += 1
            simulator.restart()
        assert len(final_outcomes) == 6
        assert set(final_outcomes.keys()) == {7, 8, 9, 10, 11, 12}
        assert sum(final_outcomes.values()) == 10

    def test_simulate_die_steps_vals(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        options = stormpy.BuilderOptions()
        options.set_build_state_valuations()
        model = stormpy.build_sparse_model_with_options(prism_program, options)
        simulator = stormpy.simulator.create_simulator(model, seed=42)
        simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)

        state, reward, label = simulator.restart()
        assert state["d"] == 0
        assert state["s"] == 0
        assert reward == [0.0]
        assert label == {"init"}

    def test_simulate_die_vals(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        options = stormpy.BuilderOptions()
        options.set_build_state_valuations()
        model = stormpy.build_sparse_model_with_options(prism_program, options)
        simulator = stormpy.simulator.create_simulator(model, seed=42)
        simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
        assert simulator.get_reward_names() == ["coin_flips"]

        simulator.restart()
        final_outcomes = dict()
        for n in range(10):
            assert not simulator.is_done()
            while not simulator.is_done():
                observation, reward, labels = simulator.step()
            if observation not in final_outcomes:
                final_outcomes[observation] = 1
            else:
                final_outcomes[observation] += 1
            simulator.restart()

        assert len(final_outcomes) == 6
        assert sum(final_outcomes.values()) == 10
        for vals, count in final_outcomes.items():
            assert 1 <= int(vals["d"]) <= 6
            assert vals["s"] == 7
            assert 1 <= count <= 10

    def test_simulate_mdp(self):
        rng = random.Random(23)
        path = stormpy.examples.files.prism_mdp_slipgrid
        prism_program = stormpy.parse_prism_program(path)
        model = stormpy.build_model(prism_program)
        simulator = stormpy.simulator.create_simulator(model, seed=42)

        # 3 paths of at most 20 steps.
        paths = []
        for m in range(3):
            state, reward, labels = simulator.restart()
            path = [state]
            for n in range(20):
                actions = simulator.available_actions()
                assert len(actions) <= 4
                select_action = rng.randint(0, len(actions) - 1)
                path.append(actions[select_action])
                state, reward, labels = simulator.step(actions[select_action])
                assert 0 <= state <= 15
                path.append(state)
                if simulator.is_done():
                    break
            paths.append(path)

        assert len(paths) == 3
        for path in paths:
            assert path[0] == 0
            assert all(isinstance(p, int) for p in path)
            assert len(path) <= 41

    def test_simulate_mdp_valuations(self):
        rng = random.Random(23)
        path = stormpy.examples.files.prism_mdp_slipgrid
        prism_program = stormpy.parse_prism_program(path)
        options = stormpy.BuilderOptions()
        options.set_build_choice_labels()
        options.set_build_state_valuations()
        model = stormpy.build_sparse_model_with_options(prism_program, options)
        simulator = stormpy.simulator.create_simulator(model, seed=42)
        simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
        simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)

        # 3 paths of at most 20 steps.
        paths = []
        for m in range(3):
            path = []
            state, reward, labels = simulator.restart()
            path = [state]
            for n in range(20):
                actions = simulator.available_actions()
                assert len(actions) <= 4
                select_action = rng.randint(0, len(actions) - 1)
                assert actions[select_action] in ["north", "east", "south", "west"]
                path.append(actions[select_action])
                state, reward, labels = simulator.step(actions[select_action])
                path.append(state)
                assert 1 <= int(state["x"]) <= 4
                assert 1 <= int(state["y"]) <= 4
                if simulator.is_done():
                    break
            paths.append(path)

        assert len(paths) == 3
        for path in paths:
            assert path[0]["x"] == 1
            assert path[0]["y"] == 1
            assert all(isinstance(p["x"], stormpy.utility.JsonContainerRational) for p in path[::2])
            assert all(p in ["north", "east", "south", "west"] for p in path[1::2])
            assert len(path) <= 41


class TestPrismSimulator:
    def test_negative_values(self):
        prism_program = stormpy.parse_prism_program(get_example_path("dtmc", "negativevals.pm"))
        prism_program = stormpy.preprocess_symbolic_input(prism_program, [], "")[0].as_prism_program()

        simulator = stormpy.simulator.create_simulator(prism_program, seed=42)
        simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
        state, rew, labels = simulator.restart()
        assert state["s"] == -1
        assert int(state["s"]) == -1

    def test_simulate_mdp(self):
        rng = random.Random(23)
        path = stormpy.examples.files.prism_mdp_slipgrid
        prism_program = stormpy.parse_prism_program(path)
        simulator = stormpy.simulator.create_simulator(prism_program, seed=42)

        # 3 paths of at most 20 steps.
        paths = []
        for m in range(3):
            state, reward, labels = simulator.restart()
            path = [state]
            for n in range(20):
                actions = simulator.available_actions()
                assert len(actions) <= 4
                select_action = rng.randint(0, len(actions) - 1)
                assert actions[select_action] < 4
                path.append(actions[select_action])
                state, reward, labels = simulator.step(actions[select_action])
                path.append(state)
                assert 1 <= int(state["x"]) <= 4
                assert 1 <= int(state["y"]) <= 4
                if simulator.is_done():
                    break
            paths.append(path)

        assert len(paths) == 3
        for path in paths:
            assert path[0]["x"] == 1
            assert path[0]["y"] == 1
            assert all(isinstance(p["x"], stormpy.utility.JsonContainerDouble) for p in path[::2])
            assert all(isinstance(p, int) for p in path[1::2])
            assert len(path) <= 41
