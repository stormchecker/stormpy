import argparse
import logging
import pathlib

import stormpy
import stormpy.dft
from stormpy.dft.simulator import DftSimulator


def get_status(simulator):
    dft_state, states = simulator.status()
    s = dft_state
    for element, status in states.items():
        elem_str = "{} ({})".format(element.name, element.type)
        s += "\n\t{0: <20} : {1}".format(elem_str, status)
    return s


def get_user_fail_be(candidates):
    while True:
        inp = input("Select index of BE to fail next (use 'q' to abort)\n")
        if inp == "q":
            return None
        try:
            inp_number = int(inp)
        except ValueError:
            logging.error("The input is not a number.")
        else:
            if 0 <= inp_number < len(candidates):
                return candidates[inp_number]
            else:
                logging.error("Selected index is not valid.")


def get_user_dep_success():
    while True:
        inp = input("Should the failure due a dependency be successful? (y/n)\n")
        if inp == "y":
            return True
        elif inp == "n":
            return False
        else:
            logging.error("Input is not valid.")


def main():
    parser = argparse.ArgumentParser(description="Interactive simulator for DFTs.")
    parser.add_argument("infile", help="Input Galileo file", type=str)
    parser.add_argument("--verbose", "-v", help="print more output", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if args.verbose else logging.INFO)

    # Load DFT from file
    if pathlib.Path(args.infile).suffix == ".json":
        dft = stormpy.dft.load_dft_json_file(args.infile)
    else:
        dft = stormpy.dft.load_dft_galileo_file(args.infile)
    logging.info("Loaded DFT with {} elements, {} BEs and {} dynamic elements.".format(dft.nr_elements(), dft.nr_be(), dft.nr_dynamic()))
    dft = stormpy.dft.prepare_for_analysis(dft)

    # Create simulator
    simulator = DftSimulator(dft, seed=42, relevant=["all"])

    # Get initial state
    logging.info("Initial status:")
    logging.info(get_status(simulator))

    while True:
        if simulator.nr_next_failures() == 0:
            logging.info("No BE can fail anymore -> will terminate")
            return

        # Ask user for next BE to fail
        candidates = simulator.next_failures()
        logging.info("Failable BEs:\n" + "\n".join(["\t{}: {}".format(i, candidates[i]) for i in range(len(candidates))]))
        be_fail = get_user_fail_be(candidates)
        if be_fail is None:
            # Exit
            return
        dep_success = True
        if simulator.is_next_dependency_failure():
            dep_success = get_user_dep_success()
        if not dep_success:
            logging.debug("Let {} not fail due to dependency".format(be_fail))
        else:
            logging.debug("Let {} fail".format(be_fail))
        # Let chosen BE fail
        res = simulator.let_fail(be_fail, dependency_successful=dep_success)
        if res == stormpy.dft.SimulationStepResult.INVALID:
            logging.warning("Failure leads to invalid state -> undo last failure")
        logging.debug("Simulation was {}".format(res))
        logging.info("New status:")
        logging.info(get_status(simulator))


if __name__ == "__main__":
    main()
