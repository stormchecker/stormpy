import stormpy
from stormpy.datastructures import BitVector
from stormpy.developer.utility import MatrixFormat, ShortestPathsGenerator
from helpers.helper import get_example_path

import pytest
import math

# this is admittedly slightly overengineered


class ModelWithKnownShortestPaths:
    """Knuth's die model with reference kSP methods"""

    def __init__(self):
        self.target_label = "one"

        program_path = get_example_path("dtmc", "die.pm")
        raw_formula = 'P=? [ F "' + self.target_label + '" ]'
        program = stormpy.parse_prism_program(program_path)
        formula = stormpy.parse_property(raw_formula, program)

        self.model = stormpy.build_model(program, formula)

    def probability(self, k):
        return (1 / 2) ** ((2 * k) + 1)

    def state_set(self, k):
        return BitVector(self.model.nr_states, [0, 1, 3, 7])

    def path(self, k):
        path = [0] + k * [1, 3] + [7]
        return list(reversed(path))  # SPG returns traversal from back


@pytest.fixture(scope="module", params=[1, 2, 3, 3000, 42])
def index(request):
    return request.param


@pytest.fixture(scope="module")
def model_with_known_shortest_paths():
    return ModelWithKnownShortestPaths()


@pytest.fixture(scope="module")
def model(model_with_known_shortest_paths):
    return model_with_known_shortest_paths.model


@pytest.fixture(scope="module")
def expected_distance(model_with_known_shortest_paths):
    return model_with_known_shortest_paths.probability


@pytest.fixture(scope="module")
def expected_state_set(model_with_known_shortest_paths):
    return model_with_known_shortest_paths.state_set


@pytest.fixture(scope="module")
def expected_path(model_with_known_shortest_paths):
    return model_with_known_shortest_paths.path


@pytest.fixture(scope="module")
def target_label(model_with_known_shortest_paths):
    return model_with_known_shortest_paths.target_label


@pytest.fixture
def state(model):
    some_state = 7
    assert model.nr_states > some_state, "test model too small"
    return some_state


@pytest.fixture
def state_list(model):
    some_state_list = [4, 5, 7]
    assert model.nr_states > max(some_state_list), "test model too small"
    return some_state_list


@pytest.fixture
def state_bitvector(model, state_list):
    return BitVector(length=model.nr_states, set_entries=state_list)


@pytest.fixture
def transition_matrix(model):
    return model.transition_matrix


@pytest.fixture
def target_prob_map(model, state_list):
    return {i: (1.0 if i in state_list else 0.0) for i in range(model.nr_states)}


@pytest.fixture
def target_prob_list(target_prob_map):
    return [target_prob_map[i] for i in range(max(target_prob_map.keys()))]


@pytest.fixture
def initial_states(model):
    return BitVector(model.nr_states, model.initial_states)


@pytest.fixture
def matrix_format():
    return MatrixFormat.STRAIGHT


class TestShortestPaths:
    def test_spg_ctor_bitvector_target(self, model, state_bitvector):
        _ = ShortestPathsGenerator(model, state_bitvector)

    def test_spg_ctor_single_state_target(self, model, state):
        _ = ShortestPathsGenerator(model, state)

    def test_spg_ctor_state_list_target(self, model, state_list):
        _ = ShortestPathsGenerator(model, state_list)

    def test_spg_ctor_label_target(self, model, target_label):
        _ = ShortestPathsGenerator(model, target_label)

    def test_spg_ctor_matrix_vector(self, transition_matrix, target_prob_list, initial_states, matrix_format):
        _ = ShortestPathsGenerator(transition_matrix, target_prob_list, initial_states, matrix_format)

    def test_spg_ctor_matrix_map(self, transition_matrix, target_prob_map, initial_states, matrix_format):
        _ = ShortestPathsGenerator(transition_matrix, target_prob_map, initial_states, matrix_format)

    def test_spg_distance(self, model, target_label, index, expected_distance):
        spg = ShortestPathsGenerator(model, target_label)
        assert math.isclose(spg.get_distance(index), expected_distance(index))

    def test_spg_state_set(self, model, target_label, index, expected_state_set):
        spg = ShortestPathsGenerator(model, target_label)
        assert spg.get_states(index) == expected_state_set(index)

    def test_spg_state_list(self, model, target_label, index, expected_path):
        spg = ShortestPathsGenerator(model, target_label)
        assert spg.get_path_as_list(index) == expected_path(index)


def test_shortest_paths_die():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_model(program)
    expected = {
        1: ([0, 1, 4, 8], 0.125),
        2: ([0, 1, 3, 1, 4, 8], 0.03125),
        3: ([0, 1, 3, 1, 3, 1, 4, 8], 0.0078125),
    }
    for k, (path, distance) in expected.items():
        states, probability = stormpy.analysis.shortest_path(model, 8, k=k)
        assert states == path
        assert math.isclose(probability, distance)


@pytest.mark.parametrize("value_type", [float, stormpy.Rational])
@pytest.mark.parametrize("target_kind", ["state", "list", "bitvector", "label"])
def test_shortest_path_convenience(value_type, target_kind):
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_model[value_type](program)
    target = {"state": 8, "list": [8], "bitvector": BitVector(model.nr_states, [8]), "label": "two"}[target_kind]
    states, probability = stormpy.analysis.shortest_path(model, target)
    assert states == [0, 1, 4, 8]
    assert isinstance(probability, value_type)
    assert probability == value_type(1) / 8

    states, probability = stormpy.analysis.shortest_path(model, target, k=3)
    assert states == [0, 1, 3, 1, 3, 1, 4, 8]
    assert probability == value_type(1) / 128


@pytest.mark.parametrize("k", [0, -1])
def test_shortest_path_invalid_rank(model, k):
    with pytest.raises(ValueError, match="k must be positive"):
        stormpy.analysis.shortest_path(model, 8, k=k)


def test_path_keyword_arguments():
    path = stormpy.analysis.Path(predecessor_node=1, predecessor_k=2, distance=0.5)
    assert path.predecessor_k == 2
    assert path.distance == 0.5
    assert str(path) == "Path with predecessorNode: 1 predecessorK: 2 distance: 0.5"
    assert str(stormpy.analysis.Path(predecessor_k=2, distance=0.5)) == "Path with predecessorNode: None predecessorK: 2 distance: 0.5"


def test_developer_shortest_paths_deduce_value_type():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_model(program)
    exact_model = stormpy.build_model[stormpy.Rational](program)
    spg = ShortestPathsGenerator(model, 8)
    exact_spg = ShortestPathsGenerator(exact_model, 8)
    assert isinstance(spg, ShortestPathsGenerator[float])
    assert isinstance(exact_spg, ShortestPathsGenerator[stormpy.Rational])
    assert exact_spg.get_distance(1) == stormpy.Rational("1/8")
    assert exact_spg.get_path_as_list(2) == spg.get_path_as_list(2)
    # Matrix-based construction deduces the value type from the transition matrix
    matrix_spg = ShortestPathsGenerator(
        exact_model.transition_matrix,
        {7: stormpy.Rational(1)},
        exact_model.initial_states_as_bitvector,
        MatrixFormat.STRAIGHT,
    )
    assert isinstance(matrix_spg, ShortestPathsGenerator[stormpy.Rational])

    exact_path = stormpy.analysis.Path[stormpy.Rational](predecessor_k=1, distance=stormpy.Rational("1/2"))
    assert exact_path.distance == stormpy.Rational("1/2")
