import os

testfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")


def _path(folder, file):
    """
    Internal method for simpler listing of examples.
    :param folder: Folder.
    :param file: Example file.
    :return: Complete path to example file.
    """
    return os.path.join(testfile_dir, folder, file)


# DTMC
prism_dtmc_die = _path("dtmc", "die.pm")
"""Prism version of Knuth Yao Die example"""
jani_dtmc_die = _path("dtmc", "die.jani")
"""Jani version of Knuth Yao Die example"""
prism_dtmc_brp = _path("dtmc", "brp-16-2.pm")
"""Prism version of Bounded Retransmission Protocol"""

prism_pdtmc_die = _path("pdtmc", "parametric_die.pm")
"""Prism version of Knuth Yao Die with 2 unfair coins"""
drn_pdtmc_die = _path("pdtmc", "die.drn")
"""DRN format of a parametric version of the Knuth Yao Die"""
prism_pdtmc_brp = _path("pdtmc", "brp16_2.pm")
"""Prism version of Bounded Retransmission Protocol with parameters"""

# MDP
prism_mdp_coin_2_2 = _path("mdp", "coin2-2.nm")
"""Prism version of 2-coin Knuth-Yao Die"""
prism_mdp_firewire = _path("mdp", "firewire.nm")
"""Prism version for Firewire protocol"""
prism_mdp_maze = _path("mdp", "maze_2.nm")
"""Prism version of maze MDP"""
prism_mdp_slipgrid = _path("mdp", "slipgrid.nm")
"""Prism version of maze MDP towards sketching"""
prism_mdp_slipgrid_sketch = _path("mdp", "slipgrid_sketch.nm")
"""Prism version of a slippery grid with fixed dimensions"""
prism_pmdp_coin_two_dice = _path("pmdp", "two_dice.nm")
"""Prism version of parametric two dice"""

# CTMC
drn_ctmc_dft = _path("ctmc", "dft.drn")
"""DRN format of a CTMC from a DFT"""

# MA
prism_ma_simple = _path("ma", "simple.ma")
"""Prism version of a simple Markov automaton"""

# POMDP
prism_pomdp_maze = _path("pomdp", "maze_2.prism")
"""Prism version of the maze POMDP"""
drn_pomdp_maze = _path("pomdp", "maze.drn")
"""DRN format of the maze POMDP"""
prism_par_pomdp_maze = _path("pomdp", "maze_2_par.prism")
"""Prism version of the parametric maze POMDP"""

# DFT
dft_galileo_hecs = _path("dft", "hecs.dft")
"""DFT in Galileo format for HECS"""
dft_json_and = _path("dft", "and.json")
"""DFT in JSON format for simple AND gate"""

# GSPN
gspn_pnpro_simple = _path("gspn", "gspn_simple.pnpro")
"""GSPN example in PNPRO format"""
gspn_pnml_simple = _path("gspn", "gspn_simple.pnml")
"""GSPN example in PNML format"""
