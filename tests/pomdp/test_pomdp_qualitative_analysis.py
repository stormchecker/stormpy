import stormpy
from configurations import pomdp

from helpers.helper import get_example_path


def _policy_search(property_string, environment=None):
    # Each solver runs a single analysis, so every test creates its own solver
    program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
    properties = stormpy.parse_properties(property_string, program)
    model = stormpy.pomdp.make_canonic(stormpy.build_model(program, properties))
    model = stormpy.pomdp.prepare_for_qualitative_search(model, properties[0])
    return model, stormpy.pomdp.create_iterative_policy_search(model, properties[0], environment=environment)


@pomdp
class TestPomdpQualitative:
    def test_winning_region(self, tmp_path):
        model, solver = _policy_search('Pmax=? [F "goal"]')
        assert type(solver) is stormpy.pomdp.IterativePolicySearch[float]
        solver.compute_winning_region(10)
        winning_region = solver.last_winning_region
        assert type(winning_region) is stormpy.pomdp.WinningRegion

        query = stormpy.pomdp.WinningRegionQueryInterface(model, winning_region)
        belief_support = stormpy.datastructures.BitVector(model.nr_states, [model.initial_states[0]])
        assert query.is_in_winning_region(belief_support)

        path = str(tmp_path / "winning_region.txt")
        winning_region.store_to_file(path, "preamble")
        _, preamble = stormpy.pomdp.WinningRegion.load_from_file(path)
        assert preamble.strip() == "preamble"

    def test_analyze_for_initial_states(self):
        _, solver = _policy_search('Pmax=? [F "goal"]')
        assert solver.analyze_for_initial_states(10)

    def test_winning_region_with_environment(self):
        _, solver = _policy_search('Pmax=? [ !"bad" U "goal" ]', environment=stormpy.environments.sound())
        solver.compute_winning_region(10)
        assert type(solver.last_winning_region) is stormpy.pomdp.WinningRegion
