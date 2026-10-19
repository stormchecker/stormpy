import stormpy
import stormpy.pars
import stormpy.pomdp

import stormpy.examples
import stormpy.examples.files


def example_pomdps_01():
    # Prevent curious side effects from earlier runs (for tests only)
    stormpy.numbers.clear_pools()
    # ###
    # # How to apply an unknown FSC to obtain a pMC from a POMDP
    # path = stormpy.examples.files.prism_pomdp_maze
    # prism_program = stormpy.parse_prism_program(path)
    #
    # formula_str = "P=? [!\"bad\" U \"goal\"]"
    # properties = stormpy.parse_properties(formula_str, prism_program)
    # # construct the POMDP
    # pomdp = stormpy.build_model(prism_program, properties)
    # # make its representation canonic.
    # pomdp = stormpy.pomdp.make_canonic(pomdp)
    # # make the POMDP simple. This step is optional but often beneficial
    # pomdp = stormpy.pomdp.make_simple(pomdp)
    # # construct the memory for the FSC
    # # in this case, a selective counter with two states
    # memory_builder = stormpy.pomdp.PomdpMemoryBuilder()
    # memory = memory_builder.build(stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_COUNTER, 2)
    # # apply the memory onto the POMDP to get the cartesian product
    # pomdp = stormpy.pomdp.unfold_memory(pomdp, memory)
    # # apply the memory onto the POMDP to get the cartesian product
    # pmc = stormpy.pomdp.apply_unknown_fsc(pomdp, stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LINEAR)

    ####
    # How to apply an unknown FSC to obtain a pMC from a pPOMDP
    path = stormpy.examples.files.prism_par_pomdp_maze
    prism_program = stormpy.parse_prism_program(path)

    formula_str = 'P=? [!"bad" U "goal"]'
    prop = stormpy.parse_property(formula_str, prism_program)
    # construct the pPOMDP
    options = stormpy.BuilderOptions(prop)
    options.set_build_state_valuations()
    options.set_build_choice_labels()
    pomdp = stormpy.build_model[stormpy.RationalFunction](prism_program, options=options)
    # make its representation canonic.
    pomdp = stormpy.pomdp.make_canonic(pomdp)

    # construct the memory for the FSC
    # in this case, a selective counter with two states
    memory_builder = stormpy.pomdp.PomdpMemoryBuilder()
    memory = memory_builder.build(stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_COUNTER, 3)
    # apply the memory onto the POMDP to get the cartesian product
    pomdp = stormpy.pomdp.unfold_memory(pomdp, memory, add_memory_labels=True, keep_state_valuations=True)
    # make the POMDP simple. This step is optional but often beneficial
    pomdp = stormpy.pomdp.make_simple(pomdp, keep_state_valuations=True)
    # apply the unknown FSC to obtain a pmc from the POMDP
    pmc = stormpy.pomdp.apply_unknown_fsc(pomdp, stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LINEAR)

    export_pmc = False  # Set to True to export the pMC as drn.
    if export_pmc:
        export_options = stormpy.io.DirectEncodingExporterOptions()
        export_options.allow_placeholders = False
        stormpy.io.export_to_drn(pmc, "test.out", options=export_options)


if __name__ == "__main__":
    example_pomdps_01()
