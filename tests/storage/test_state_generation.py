import stormpy
from stormpy.examples.files import prism_dtmc_die
import pytest


class _DfsQueue:
    def __init__(self):
        self.queue = []
        self.visited = set()

    def push(self, state_id):
        if state_id not in self.visited:
            self.queue.append(state_id)
            self.visited.add(state_id)

    def pop(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return None


def _dfs_explore(program, callback):
    generator = stormpy.StateGenerator(program)

    queue = _DfsQueue()
    current_state_id = generator.load_initial_state()
    queue.visited.add(current_state_id)

    while True:
        callback(current_state_id, generator)

        successors = generator.expand()
        assert len(successors) <= 1
        for choice in successors:
            for state_id, _prob in choice.distribution:
                queue.push(state_id)
        current_state_id = queue.pop()
        if current_state_id is None:
            break
        generator.load(current_state_id)


def _load_program(filename):
    program = stormpy.parse_prism_program(filename)  # pylint: disable=no-member
    program = program.substitute_constants()

    expression_parser = stormpy.ExpressionParser(program.expression_manager)
    expression_parser.set_identifier_mapping({var.name: var.get_expression() for var in program.get_variables()})
    return program, expression_parser


def _find_variable(program, name):
    for var in program.get_variables():
        if var.name is name:
            return var
    return None


@pytest.mark.skipif(True, reason="State generation is broken")
def test_knuth_yao_die():
    program, expression_parser = _load_program(prism_dtmc_die)
    s_variable = _find_variable(program, "s")
    upper_bound_invariant = expression_parser.parse("d <= 6")

    number_states = 0

    def callback(_state_id, generator):
        nonlocal number_states
        number_states += 1

        valuation = generator.current_state_to_valuation()
        assert valuation.integer_values[s_variable] <= 7
        assert generator.current_state_satisfies(upper_bound_invariant)

    _dfs_explore(program, callback)
    assert number_states == 13
