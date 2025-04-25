import stormpy

# Check if numpy is available
try:
    import numpy as np

    numpy_found = True
except ModuleNotFoundError:
    numpy_found = False


def example_building_mas_01():
    if not numpy_found:
        print("Numpy not available")
        return

    # Building the transition matrix using numpy
    transitions = np.array([[0, 1, 0, 0, 0], [0.8, 0, 0.2, 0, 0], [0.9, 0, 0, 0.1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype="float64")

    # Build matrix and define indices of row groups (ascending order)
    transition_matrix = stormpy.build_sparse_matrix(transitions, [0, 2, 3, 4, 5])
    print(transition_matrix)

    # StateLabeling
    state_labeling = stormpy.storage.StateLabeling(5)
    # Add labels
    state_labels = {"init", "deadlock"}
    # Set labeling of states
    for label in state_labels:
        state_labeling.add_label(label)
    state_labeling.add_label_to_state("init", 0)

    # Choice labeling
    choice_labeling = stormpy.storage.ChoiceLabeling(6)
    # Add labels
    choice_labels = {"alpha", "beta"}
    # Set labeling of choices
    for label in choice_labels:
        choice_labeling.add_label(label)
    choice_labeling.add_label_to_choice("alpha", 0)
    choice_labeling.add_label_to_choice("beta", 1)

    # Provide exit rates (for Markovian states)
    exit_rates = [0.0, 10.0, 12.0, 1.0, 1.0]

    markovian_states = stormpy.BitVector(5, [1, 2, 3, 4])

    # Collect components
    components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling, markovian_states=markovian_states)
    components.choice_labeling = choice_labeling
    components.exit_rates = exit_rates

    # Build the model
    ma = stormpy.storage.SparseMA(components)
    print(ma)


if __name__ == "__main__":
    example_building_mas_01()
