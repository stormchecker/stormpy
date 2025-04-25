import stormpy


# Knuth's model of a fair die using only fair coins
def example_building_mdps_01():
    nr_states = 13
    nr_choices = 14

    # Transition matrix with custom row grouping: nondeterministic choice over the actions available in states
    builder = stormpy.SparseMatrixBuilder(rows=0, columns=0, entries=0, force_dimensions=False, has_custom_row_grouping=True, row_groups=0)

    # New row group, for actions of state 0
    builder.new_row_group(0)
    builder.add_next_value(0, 1, 0.5)
    builder.add_next_value(0, 2, 0.5)
    builder.add_next_value(1, 1, 0.2)
    builder.add_next_value(1, 2, 0.8)
    # State 1
    builder.new_row_group(2)
    builder.add_next_value(2, 3, 0.5)
    builder.add_next_value(2, 4, 0.5)
    # State 2
    builder.new_row_group(3)
    builder.add_next_value(3, 5, 0.5)
    builder.add_next_value(3, 6, 0.5)
    # State 3
    builder.new_row_group(4)
    builder.add_next_value(4, 7, 0.5)
    builder.add_next_value(4, 1, 0.5)
    # State 4
    builder.new_row_group(5)
    builder.add_next_value(5, 8, 0.5)
    builder.add_next_value(5, 9, 0.5)
    # State 5
    builder.new_row_group(6)
    builder.add_next_value(6, 10, 0.5)
    builder.add_next_value(6, 11, 0.5)
    # State 6
    builder.new_row_group(7)
    builder.add_next_value(7, 2, 0.5)
    builder.add_next_value(7, 12, 0.5)

    # Add transitions for the final states
    for s in range(8, 14):
        builder.new_row_group(s)
        builder.add_next_value(s, s - 1, 1)

    transition_matrix = builder.build()

    # State labeling
    state_labeling = stormpy.storage.StateLabeling(nr_states)
    # Add labels
    labels = {"init", "one", "two", "three", "four", "five", "six", "done", "deadlock"}
    for label in labels:
        state_labeling.add_label(label)

    # Set labeling of states
    state_labeling.add_label_to_state("init", 0)
    state_labeling.add_label_to_state("one", 7)
    state_labeling.add_label_to_state("two", 8)
    state_labeling.add_label_to_state("three", 9)
    state_labeling.add_label_to_state("four", 10)
    state_labeling.add_label_to_state("five", 11)
    state_labeling.add_label_to_state("six", 12)

    # Set label 'done' for multiple states
    state_labeling.set_states("done", stormpy.BitVector(nr_states, [7, 8, 9, 10, 11, 12]))

    # Choice labeling
    choice_labeling = stormpy.storage.ChoiceLabeling(nr_choices)
    choice_labels = {"a", "b"}
    # Add labels
    for label in choice_labels:
        choice_labeling.add_label(label)

    # Set labels
    choice_labeling.add_label_to_choice("a", 0)
    choice_labeling.add_label_to_choice("b", 1)
    print(choice_labeling)

    # Reward models
    reward_models = {}
    # Create a vector representing the state-action rewards
    action_reward = [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    reward_models["coin_flips"] = stormpy.SparseRewardModel(optional_state_action_reward_vector=action_reward)

    # Collect components
    components = stormpy.SparseModelComponents(
        transition_matrix=transition_matrix, state_labeling=state_labeling, reward_models=reward_models, rate_transitions=False
    )
    components.choice_labeling = choice_labeling

    # Build the model
    mdp = stormpy.storage.SparseMdp(components)
    print(mdp)


if __name__ == "__main__":
    example_building_mdps_01()
