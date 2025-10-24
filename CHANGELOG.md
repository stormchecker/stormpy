Changelog
=============

Version 1.11.x
--------------

### Version 1.11.3 (2025/10)
Requires Storm version >= 1.11.0. Binaries for this release are linked with Storm 1.11.1.

- Use latest Storm version in CI workflow for releases.

### Version 1.11.2 (2025/10)
Requires Storm version >= 1.11.0. Binaries for this release are linked with Storm 1.11.0.

- Prebuilt binaries on mac require at least macOS version 14 (Apple Silicon) or version 15 (Intel) 
- Documentation: Revised installation guide
- Developer: Improved workflow for creating wheels and added support for Linux ARM
- Developer: Use fixed versions for Python dependencies

### Version 1.11.1 (2025/09)
Requires Storm version >= 1.11.0. 

- Fixed issue in CI workflow for releases

### Version 1.11.0 (2025/09)
Requires Storm version >= 1.11.0

- Restructured build process:
    * Migrated build process to scikit-build-core
    * Adaptions to build process of Storm
    * Developer: added information on used Storm library (e.g. installation location) to `stormpy.info`
    * Developer: internal libraries are denoted by underscore prefix (e.g. `_storage`) now
- Generalized functions `get_value` and `get_values_states` for valuations
- Adaption to changes in Storm
- Documentation: Use Sphinx theme Nefertiti and updated documentation
- Developer: CI workflow for new releases including publishing to pypi


Version 1.10.x
--------------

### Version 1.10.1 (2025/07)
Requires Storm version > 1.10.0

- First stand-alone (including Storm) release to [pypi](https://pypi.org/project/stormpy/).

### Version 1.10.0 (2025/05)
Requires Storm version >= 1.10.0

- Integrated pycarl into stormpy. Pycarl is no longer available as a separate library.
- Support for forcing exact mode in environment
- Support for building Prism SMGs
- Support for building interval POMDPs from DRN
- Added convenience functions for state valuations
- Multi-objective plotting
- Check DFT for potential modeling issues
- Added argument `use_groups` to submatrix
- Bug fixes in interactive belief explorer, `prob01max_states`, parsing properties and `program.variables`
- Improved documentation
- Adaption to changes in Storm
- Developer: support for automatic code formatting
- Developer: support for multi-platform Docker images
- Developer: use C++20


Version 1.9.x
-------------

### Version 1.9.0 (2024/08)
Requires Storm version >= 1.9.0 and pycarl version >= 2.3.0

- Support for computing steady-state distributions
- Support for quantitative POMDP analysis
- Support for interval-based models
- Extended ADD support
- Support for all-in-one MDP
- Bindings for Smg and GameFormula
- Build parametric models from model components
- Improved access to state valuations, choice labels and choice origins
- Adaption to changes in Storm such as DFT simulator
- Developer: improved build process


Version 1.8.x
-------------

### Version 1.8.0 (2023/06)
Requires Storm version >= 1.8.0 and pycarl version >= 2.2.0

- Scheduler extraction for exact models
- Adaption to changes in Storm such as the removal of JIT compilation and changes in `storm-pomdp`
- Added bindings for DFT modules
- Developer: improved build process
- Developer: updated pybind version to 2.10.0. Check compatibility to pybind version of pycarl


Version 1.7.x
-------------

### Version 1.7.0 (2022/07)
Requires Storm version >= 1.7.0 and pycarl version >= 2.1.0

- Support for plotting via extras `plot`
- Support for LTL model checking via Spot
- Some support for multi-objective model checking queries
- Bindings for maximal end components
- Support for computing expected number of visits
- Added accessors for Prism program
- Added documentation for simulator
- Support for building complete/partial state space of DFT
- Instantiator for parametric DFT
- Simulator for DFT
- Added Dockerfile
- Developer: stormpy is built with C++17
- Developer: updated pybind11 to version 2.8.1 and adapted bindings accordingly
- Adaption to changes in Storm such as the new namespace `storm::dft`


Version 1.6.x
-------------

### Version 1.6.4 (2022/01)
Requires storm version >= 1.6.4 and pycarl version >= 2.0.5

- Simulator for sparse models updated, added simulator for prism programs.
- Renamed PrismProgram::isDeterministicModel -> is_deterministic_model for consistency
- Support for specifying the returned quotient format (symbolic or sparse) for symbolic bisimulation
- Added support for continuous integration with Github Actions
- Updated bindings for, e.g., Jani to reflect changes in Storm
- Bindings for end component elimination

### Version 1.6.3 (2020/12)
Requires storm version >= 1.6.3 and pycarl version >= 2.0.4

- Documentation is largely based on Jupyter notebooks now and supports launch with Binder
- Support for exact arithmetic in models
- Support for timeouts/signal handlers in Storm
- Code for parametric/exact/floating-point models data structures unified
- Extended support for Prism and Jani data structures
- `export_parametric_to_drn` no longer exists, use `export_to_drn` instead

### Version 1.6.2 (2020/09)
Requires storm version >= 1.6.2 and pycarl version >= 2.0.4

- Adaptions to changes in Storm
- Create models (DTMC, MDP, CTMC, MA) directly from model components. Support creation of transition matrix, labeling, reward models, etc.
- Explicit State Lookup: Finding a state based on the variable values
- Support for pPOMDPs
- (p)POMDPs: Support for unfolding memory, making POMDPs simple, and exporting POMDP to a pMC
- Export to DRN options to support exporting without placeholders
- Renamed `preprocess_prism_program` to `preprocess_symbolic_input`
- Bindings for Storm-dft; most notably transformations, symmetries and relevant events

### Version 1.6.1
Skipped for compatibility with Storm.

### Version 1.6.0 (2020/06)
Requires storm version >= 1.6.0 and pycarl version >= 2.0.4

- Adaptions to changes in Storm: most notably state valuations
- Support for GSPNs: parsing, exploring, building
- Support for matrix building
- Extended expression operators with {conjunction, disjunction}
- Added information collector to extract information from jani models
- Bindings for elimination of chains of non-Markovian states
- Early support for POMDPs
- Early support for simulations on explicit-state models 


Version 1.5.x
-------------

### Version 1.5.1
Skipped for compatibility with Storm.

### Version 1.5.0
Skipped for compatibility with Storm.


Version 1.4.x
-------------

### Version 1.4.1 (2019/12)
Requires storm version >= 1.4.1 and pycarl version >= 2.0.4
- Adaptions to changes in Storm
- Extended simple accessors such as `parse_properties`, `model_checking`, to handle variety of inputs.
- Added and extended environments
- Changed constructor of `ParameterRegion` to take a valuation instead of string.
  Use `ParameterRegion.create_from_string()` to create a region from string.
- Added InstantiationModelChecker for pMDPs and allow instations with rational numbers
- Added transformation of CTMCs to DTMCs
- Further bindings for Prism Programs and their preprocessing
- SettingsManager updated
- Allow building models annotated with valuations
- A custom state exploration that allows to explore successor states of a prism program
- Extended documentation, in particular examples.
- Fix for compilation with Xcode 11


### Version 1.4.0
Skipped for compatibility with Storm.


Version 1.3.x
-------------

### Version 1.3.0 (2019/01)
Requires storm version >= 1.3.0 and pycarl version >= 2.0.3
- Adaptions to changes in Storm
- Bindings for symbolic models:
    * building symbolic models
    * bisimulation
    * transforming symbolic to sparse models
- Extraction of schedulers and queries on schedulers
- High-level counterexamples connected
- Drastically extended JANI bindings
- Extended bindings for expressions
- Extended PLA bindings
- Extended DFT bindings
- Extended documentation
- Improved and extended setup


Version 1.2.x
-------------

### Version 1.2.0
Requires storm version >= 1.2.0 and pycarl version >= 2.0.2
- Adaptions to changes in Storm
- Bindings for simplification of parametric models
- Handling of rewards
- Building of model with all labels if no formula is given
- Support for `submatrix()`
- Extended documentation
- Extended build script


Version 1.1.x
-------------

### Version 1.1.0 (2017/08)
Requires storm version >= 1.1.0
- Bindings for `storm-pars`
- Bindings for graph constraints
- Bindings for handling JANI files
- Moved expressions from own module into `storage` module
- Travis support for build process
- Tests for documentation
- Updated pybind version


Version 1.0.x
-------------
Skipped, to keep on par with storm


Version 0.9.x
-------------

### Version 0.9.1 (2017/04)
- Bindings for DFTs
- Bindings for PLA
- Updated to pycarl version 2.0.0 (support for both CLN and GMP)
- Improved building system, read flags from storm build system

### Version 0.9 (2017/03)
- Start of this changelog


# Appendix: Pycarl Changelog
=============

Version 2.3.x
-------------

### Version 2.3.0 (2024/08)
Requires carl-storm version >= 14.23

- Added support for intervals with different number types
- Automated code formatting
- Developer: improved build and CMake support
- Developer: improved CI


Version 2.2.x
-------------

### Version 2.2.0 (2023/06)
Requires carl-storm version >= 14.23

- Upgraded repo / version for carl, requires [carl-storm](https://github.com/moves-rwth/carl-storm) from now on
- Developer: added Dockerfile
- Developer: improved build process
- Developer: updated pybind11 to version 2.10.0


Version 2.1.x
-------------

### Version 2.1.0 (2022/07)
Requires carl with branch `master14`

- Developer: updated pybind11 to version 2.8.1 and adapted bindings accordingly
- Improved continuous integration with Github Actions


Version 2.0.x
-------------

### Version 2.0.5 (2022/01)
Requires carl with branch `master14`

- Added support for continuous integration with Github Actions

### Version 2.0.4 (2019/11)
Requires carl with branch `master14`

- Extended conversion of number types to formulae
- (minor) changed `constant_part` to function for `Polynomial`
- (minor) added an additional operator on polynomials
- Fix for compilation with Xcode 11

### Version 2.0.3 (2019/01)
Requires carl with branch `master14` or a carl version between 17.12 and 18.08

- Extended bindings for arithmetic operations
- Fixed negation comparison
- Improved error output in installation
- Extended documentation
- Improved and extended setup

### Version 2.0.2 (2017/12)
Requires carl version >= 17.12

- Adaptions to changes in carl
- Extended bindings for rational functions and factorized rational functions
- `Variable` constructor no longer returns an existing variable if a variable with that name exists
- `expand()` allows to obtain the expanded polynomial and rational function
- Added methods for getting information about pycarl configuration
- Extended build script:
    * uses config file
    * support for disabling build of CLN and parser bindings
    * fixed debug build type

### Version 2.0.1 (2017/08)
Requires carl version >= 17.08

- Added conversions between CLN and GMP
- Added variable and integer pickling support. Throw errors if pickling is not supported
- Added hash functions
- Hide factorization caches for user
- Depend on [carl-parser](https://github.com/ths-rwth/carl-parser) for parsing routines
- Check for carl version
- Fixed issues when CLN is not available

### Version 2.0.0 (2017/05)
- First version with support for CLN and GMP.
  This means that no longer all operators are supported as it would be ambiguous
- Using bigint


Version 1.2.x
-------------

### Version 1.2.1 (2017/04)
- Arbitrary-size integers (CLN and GMP)

### Version 1.2.0 (2017/03)
- Start of this changelog
