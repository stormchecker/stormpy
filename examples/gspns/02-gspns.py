import stormpy
import stormpy.gspn

import stormpy.examples
import stormpy.examples.files


def example_gspns_02():
    # Use GSPNBuilder to construct a GSPN
    builder = stormpy.gspn.GSPNBuilder()
    builder.set_name("my_gspn")

    # Add immediate transition
    it_1 = builder.add_immediate_transition(1, 0.0, "it_1")
    it_layout = stormpy.gspn.LayoutInfo(1.5, 2.0)
    builder.set_transition_layout_info(it_1, it_layout)

    # Add timed transition
    tt_1 = builder.add_timed_transition(0, 0.4, "tt_1")
    tt_layout = stormpy.gspn.LayoutInfo(12.5, 2.0)
    builder.set_transition_layout_info(tt_1, tt_layout)

    # Add places
    place_1 = builder.add_place(1, 1, "place_1")
    p1_layout = stormpy.gspn.LayoutInfo(6.5, 2.0)
    builder.set_place_layout_info(place_1, p1_layout)

    place_2 = builder.add_place(1, 0, "place_2")
    p2_layout = stormpy.gspn.LayoutInfo(18.5, 2.0)
    builder.set_place_layout_info(place_2, p2_layout)

    # Link places and transitions by arcs
    builder.add_output_arc(it_1, place_1)
    builder.add_inhibition_arc(place_1, it_1)
    builder.add_input_arc(place_1, tt_1)
    builder.add_output_arc(tt_1, place_2)

    # Build GSPN
    gspn = builder.build_gspn()

    print("Name of GSPN: {}.".format(gspn.get_name()))
    print("Number of places: {}.".format(gspn.get_number_of_places()))
    print("Number of immediate transitions: {}.".format(gspn.get_number_of_immediate_transitions()))
    print("Number of timed transitions: {}.".format(gspn.get_number_of_timed_transitions()))

    # Export to file (PNPRO format)
    export_path = stormpy.examples.files.gspn_pnpro_simple
    gspn.export_gspn_pnpro_file(export_path)


if __name__ == "__main__":
    example_gspns_02()
