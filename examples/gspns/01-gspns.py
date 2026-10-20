import stormpy
import stormpy.gspn

import stormpy.examples
import stormpy.examples.files


def example_gspns_01():
    # Load a GSPN from file (PNML format)
    import_path = stormpy.examples.files.gspn_pnml_simple
    gspn = stormpy.gspn.load_gspn_file(import_path)

    print("Name of GSPN: {}.".format(gspn.get_name()))
    print("Number of places: {}.".format(gspn.get_number_of_places()))
    print("Number of immediate transitions: {}.".format(gspn.get_number_of_immediate_transitions()))
    print("Number of timed transitions: {}.".format(gspn.get_number_of_timed_transitions()))


if __name__ == "__main__":
    example_gspns_01()
