import os

import stormpy

from configurations import gspn, xml


@gspn
class TestGSPNBuilder:
    def test_layout_info(self):
        layout = stormpy.gspn.LayoutInfo()
        assert layout.x == 0
        assert layout.y == 0
        assert layout.rotation == 0
        layout.x = 1
        assert layout.x == 1

        layout_xy = stormpy.gspn.LayoutInfo(2, 3)
        assert layout_xy.x == 2
        assert layout_xy.rotation == 0

        layout_xyr = stormpy.gspn.LayoutInfo(2, 3, 4)
        assert layout_xyr.rotation == 4

    def test_place(self):
        p_id = 4
        place = stormpy.gspn.Place(id=p_id)
        assert p_id == place.get_id()

        assert not place.has_restricted_capacity()
        place.set_capacity(cap=5)
        assert place.has_restricted_capacity()
        assert place.get_capacity() == 5

        p_name = "P_0"
        place.set_name(name=p_name)
        assert place.get_name() == p_name

        p_tokens = 2
        place.set_number_of_initial_tokens(p_tokens)
        assert place.get_number_of_initial_tokens() == p_tokens

    def test_transition(self):
        # test TimedTransition
        tt = stormpy.gspn.TimedTransition()
        tt_name = " tt"
        tt.set_name(tt_name)
        assert tt_name == tt.get_name()
        tt_rate = 0.2
        tt.set_rate(tt_rate)
        assert tt_rate == tt.get_rate()

        # connect a place to this transition and test arcs
        place = stormpy.gspn.Place(0)
        # test input arcs
        assert not tt.exists_input_arc(place)
        tt.set_input_arc_multiplicity(place, 2)
        assert tt.exists_input_arc(place)
        assert tt.get_input_arc_multiplicity(place) == 2
        tt.remove_input_arc(place)
        assert not tt.exists_input_arc(place)
        # test output arcs
        assert not tt.exists_output_arc(place)
        tt.set_output_arc_multiplicity(place, 3)
        assert tt.exists_output_arc(place)
        assert tt.get_output_arc_multiplicity(place) == 3
        tt.remove_output_arc(place)
        assert not tt.exists_output_arc(place)
        # test inhibition arcs
        assert not tt.exists_inhibition_arc(place)
        tt.set_inhibition_arc_multiplicity(place, 5)
        assert tt.exists_inhibition_arc(place)
        assert tt.get_inhibition_arc_multiplicity(place) == 5
        tt.remove_inhibition_arc(place)
        assert not tt.exists_inhibition_arc(place)

        # test ImmediateTransition
        ti = stormpy.gspn.ImmediateTransition()
        ti_name = " ti"
        ti.set_name(ti_name)
        assert ti_name == ti.get_name()
        assert ti.no_weight_attached()
        ti_weight = 0.2
        ti.set_weight(ti_weight)
        assert ti_weight == ti.get_weight()
        assert not ti.no_weight_attached()

    def test_build_gspn(self):
        gspn_name = "gspn_test"
        builder = stormpy.gspn.GSPNBuilder()

        id_p_0 = builder.add_place()
        id_p_1 = builder.add_place(initial_tokens=1)
        id_p_2 = builder.add_place(initial_tokens=0, name="place_2")
        id_p_3 = builder.add_place(capacity=2, initial_tokens=3, name="place_3")
        p_layout = stormpy.gspn.LayoutInfo(1, 2)
        builder.set_place_layout_info(id_p_0, p_layout)

        id_ti_0 = builder.add_immediate_transition(priority=1, weight=0.5, name="ti_0")
        id_ti_1 = builder.add_immediate_transition()

        id_tt_0 = builder.add_timed_transition(priority=2, rate=0.4, name="tt_0")
        id_tt_1 = builder.add_timed_transition(priority=0, rate=0.5, num_servers=2, name="tt_1")

        t_layout = stormpy.gspn.LayoutInfo(1, 2)
        builder.set_transition_layout_info(id_ti_0, t_layout)

        # add arcs
        builder.add_input_arc(id_p_0, id_ti_1, multiplicity=2)
        builder.add_input_arc("place_2", "ti_0", multiplicity=2)

        builder.add_output_arc(id_ti_1, id_p_2, multiplicity=2)
        builder.add_output_arc("tt_0", "place_3", multiplicity=2)

        builder.add_inhibition_arc(id_p_2, id_tt_0, multiplicity=2)
        builder.add_inhibition_arc("place_3", "tt_0", multiplicity=2)

        builder.add_normal_arc("place_3", "tt_0", multiplicity=2)
        builder.add_normal_arc("tt_0", "place_3", multiplicity=2)

        # test gspn composition
        builder.set_name(gspn_name)
        gspn = builder.build_gspn()

        assert gspn.get_name() == gspn_name
        assert gspn.is_valid()
        assert gspn.get_number_of_immediate_transitions() == 2
        assert gspn.get_number_of_timed_transitions() == 2
        assert gspn.get_number_of_places() == 4

        assert len(gspn.get_places()) == 4
        assert len(gspn.get_immediate_transitions()) == 2
        assert len(gspn.get_timed_transitions()) == 2

        # test places
        p_0 = gspn.get_place(id_p_0)
        assert p_0.get_id() == id_p_0

        p_1 = gspn.get_place(id_p_1)
        assert p_1.get_id() == id_p_1
        assert p_1.get_number_of_initial_tokens() == 1

        p_2 = gspn.get_place(id_p_2)
        assert p_2.get_id() == id_p_2
        assert p_2.get_name() == "place_2"

        p_3 = gspn.get_place(id_p_3)
        assert p_3.get_name() == "place_3"
        assert p_3.get_capacity() == 2
        assert p_3.get_number_of_initial_tokens() == 3
        assert p_3.has_restricted_capacity()

        # test transitions
        ti_0 = gspn.get_immediate_transition("ti_0")
        assert ti_0.get_id() == id_ti_0
        assert ti_0.get_weight() == 0.5
        assert ti_0.get_priority() == 1

        tt_0 = gspn.get_timed_transition("tt_0")
        assert tt_0.get_id() == id_tt_0
        assert tt_0.get_rate() == 0.4
        assert tt_0.get_priority() == 2

        tt_1 = gspn.get_timed_transition("tt_1")
        assert tt_1.get_id() == id_tt_1
        assert tt_1.get_number_of_servers() == 2

        # test new name
        gspn_new_name = "new_name"
        gspn.set_name(gspn_new_name)
        assert gspn.get_name() == gspn_new_name

    @xml
    def test_export_to_pnpro(self, tmpdir):
        builder = stormpy.gspn.GSPNBuilder()
        builder.set_name("gspn_test")

        # add places and transitions
        id_p_0 = builder.add_place()
        id_p_1 = builder.add_place(initial_tokens=3, name="place_1", capacity=2)
        id_ti_0 = builder.add_immediate_transition(priority=0, weight=0.5, name="ti_0")
        id_tt_0 = builder.add_timed_transition(priority=0, rate=0.5, num_servers=2, name="tt_0")

        gspn = builder.build_gspn()

        export_file = os.path.join(str(tmpdir), "gspn.pnpro")

        # export gspn to pnml
        gspn.export_gspn_pnpro_file(export_file)
        assert os.path.exists(export_file)

        # import gspn
        gspn_parser = stormpy.gspn.GSPNParser()
        gspn_import = gspn_parser.parse(export_file)

        # test imported gspn
        assert gspn_import.get_name() == gspn.get_name()
        assert gspn_import.get_number_of_timed_transitions() == gspn.get_number_of_timed_transitions()
        assert gspn_import.get_number_of_immediate_transitions() == gspn.get_number_of_immediate_transitions()
        assert gspn_import.get_number_of_places() == gspn.get_number_of_places()

        p_0 = gspn_import.get_place(id_p_0)
        assert p_0.get_id() == id_p_0
        p_1 = gspn_import.get_place(id_p_1)
        assert p_1.get_name() == "place_1"
        # todo capacity info lost
        # assert p_1.get_capacity() == 2
        # assert p_1.has_restricted_capacity() == True
        assert p_1.get_number_of_initial_tokens() == 3

        ti_0 = gspn_import.get_immediate_transition("ti_0")
        assert ti_0.get_id() == id_ti_0
        tt_0 = gspn_import.get_timed_transition("tt_0")
        assert tt_0.get_id() == id_tt_0

    @xml
    def test_export_to_pnml(self, tmpdir):
        builder = stormpy.gspn.GSPNBuilder()
        builder.set_name("gspn_test")

        # add places and transitions
        id_p_0 = builder.add_place()
        id_p_1 = builder.add_place(initial_tokens=3, name="place_1", capacity=2)
        id_ti_0 = builder.add_immediate_transition(priority=0, weight=0.5, name="ti_0")
        id_tt_0 = builder.add_timed_transition(priority=0, rate=0.5, num_servers=2, name="tt_0")

        gspn = builder.build_gspn()

        export_file = os.path.join(str(tmpdir), "gspn.pnml")

        # export gspn to pnml
        gspn.export_gspn_pnml_file(export_file)
        assert os.path.exists(export_file)

        # import gspn
        gspn_parser = stormpy.gspn.GSPNParser()
        gspn_import = gspn_parser.parse(export_file)

        # test imported gspn
        assert gspn_import.get_name() == gspn.get_name()
        assert gspn_import.get_number_of_timed_transitions() == gspn.get_number_of_timed_transitions()
        assert gspn_import.get_number_of_immediate_transitions() == gspn.get_number_of_immediate_transitions()
        assert gspn_import.get_number_of_places() == gspn.get_number_of_places()

        p_0 = gspn_import.get_place(id_p_0)
        assert p_0.get_id() == id_p_0
        p_1 = gspn_import.get_place(id_p_1)
        assert p_1.get_name() == "place_1"
        assert p_1.get_capacity() == 2
        assert p_1.get_number_of_initial_tokens() == 3
        assert p_1.has_restricted_capacity()

        ti_0 = gspn_import.get_immediate_transition("ti_0")
        assert ti_0.get_id() == id_ti_0
        tt_0 = gspn_import.get_timed_transition("tt_0")
        assert tt_0.get_id() == id_tt_0
