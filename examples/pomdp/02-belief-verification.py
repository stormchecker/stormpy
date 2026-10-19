import stormpy
import stormpy.pomdp

import stormpy.examples
import stormpy.examples.files


def example_pomdps_02():
    # How to compute bounds on the optimal value of a POMDP
    path = stormpy.examples.files.prism_pomdp_maze
    prism_program = stormpy.parse_prism_program(path)

    formula_str = 'Pmax=? [!"bad" U "goal"]'
    prop = stormpy.parse_property(formula_str, prism_program)
    # construct the POMDP
    options = stormpy.BuilderOptions(prop)
    options.set_build_choice_labels()
    pomdp = stormpy.build_model(prism_program, options=options)

    # Unfolding the belief MDP yields a lower bound for maximization (an upper bound for minimization).
    # The exploration can be limited, e.g., to a number of beliefs.
    lower = stormpy.pomdp.verify_with_belief_unfolding(pomdp, prop, max_exploration_size=1000, generate_policy=True)
    # Discretizing the belief space yields an upper bound for maximization (a lower bound for minimization).
    upper = stormpy.pomdp.verify_with_belief_discretization(pomdp, prop, 4)
    print(f"Maximal probability is in [{lower.value:.4f}, {upper.value:.4f}]")
    assert lower.value <= upper.value + 1e-6

    # The unfolding can also provide a finite-state controller achieving the lower bound
    print(lower.policy)


if __name__ == "__main__":
    example_pomdps_02()
