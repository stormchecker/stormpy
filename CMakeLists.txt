cmake_minimum_required(VERSION 3.15)

project(stormpy)

# include(FetchContent)

# FetchContent_Declare(
#     storm
#     GIT_REPOSITORY https://github.com/moves-rwth/storm.git
#     GIT_BRANCH     master
#     OVERRIDE_FIND_PACKAGE
# )
# message(Callign make available)
# FetchContent_MakeAvailable(storm)
# message(Done with make)


option(USE_STORM_DFT "Enable support for DFTs" ON)
option(USE_STORM_GSPN "Enable support for GSPNs" ON)
option(USE_STORM_PARS "Enable support for parametric models" ON)
option(USE_STORM_POMDP "Enable support for POMDPs" ON)
option(STORMPY_DISABLE_SIGNATURE_DOC "Disable the signature in the documentation" OFF)

option(USE_CLN_NUMBERS "Make cln numbers available in pycarl" ON)
option(USE_PARSER "Make carlparser available in pycarl" ON)

MARK_AS_ADVANCED(STORMPY_DISABLE_SIGNATURE_DOC)
set(PYBIND_VERSION "" CACHE STRING "Pybind11 version to use")
MARK_AS_ADVANCED(PYBIND_VERSION)
set(STORM_DIR_HINT "" CACHE STRING "A hint where the Storm library can be found.")
set(CARL_DIR_HINT "" CACHE STRING "A hint where the Carl library can be found.")
set(CARLPARSER_DIR_HINT "" CACHE STRING "A hint where the Carl-parser library can be found.")

find_package(storm REQUIRED HINTS ${STORM_DIR_HINT})
find_package(carl REQUIRED HINTS ${CARL_DIR_HINT})
find_package(carlparser QUIET HINTS ${CARLPARSER_DIR_HINT})

find_package(Python COMPONENTS Interpreter Development REQUIRED)
include(resources/include_pybind11.cmake)

include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/macros.cmake)

set(CMAKE_CXX_STANDARD 20)

# This sets interprocedural optimization off as this leads to some problems on some systems
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF)
# This sets the default visibility from hidden to default,
# which is recommended *not* to do, but leads to errors otherwise.
set(CMAKE_CXX_VISIBILITY_PRESET "default")


# Workaround for issue with Boost >= 1.81
find_package(Boost 1.65.1 QUIET REQUIRED COMPONENTS filesystem system)
if (Boost_FOUND)
    if (${Boost_VERSION} VERSION_GREATER_EQUAL "1.81.0")
        message(STATUS "Stormpy - Using workaround for Boost >= 1.81")
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_PHOENIX_STL_TUPLE_H_")
    endif()
endif ()


# Set configurations
set(STORM_VERSION ${storm_VERSION})
# Set number types from Carl
set_variable_string(STORM_USE_CLN_EA_BOOL ${STORM_USE_CLN_EA})
set_variable_string(STORM_USE_CLN_RF_BOOL ${STORM_USE_CLN_RF})
if (STORM_USE_CLN_EA)
    set(PYCARL_EA_PACKAGE "cln")
else()
    set(PYCARL_EA_PACKAGE "gmp")
endif()
if (STORM_USE_CLN_RF)
    set(PYCARL_RF_PACKAGE "cln")
else()
    set(PYCARL_RF_PACKAGE "gmp")
endif()
set(PYCARL_IMPORTS "from stormpy import pycarl")
if (STORM_USE_CLN_EA OR STORM_USE_CLN_RF)
    set(PYCARL_IMPORTS "${PYCARL_IMPORTS}\nfrom stormpy.pycarl import cln")
endif()
if (NOT STORM_USE_CLN_EA OR NOT STORM_USE_CLN_RF)
    set(PYCARL_IMPORTS "${PYCARL_IMPORTS}\nfrom stormpy.pycarl import gmp")
endif()

set(CARL_VERSION ${carl_VERSION})
if ((USE_PARSER) AND (carlparser_FOUND))
    set(CARL_WITH_PARSER "True")
else()
    set(CARL_WITH_PARSER "False")
endif()
if ((USE_CLN_NUMBERS) AND (CARL_USE_CLN_NUMBERS))
    set(CARL_WITH_CLN "True")
    set(PYCARL_HAS_CLN TRUE)
else()
    set(CARL_WITH_CLN "False")
    set(PYCARL_HAS_CLN FALSE)
endif()

# Set dependency variables
set_dependency_var(SPOT)
set_dependency_var(XERCES)
# Check for optional Storm libraries
storm_with_lib(DFT)
storm_with_lib(GSPN)
storm_with_lib(PARS)
storm_with_lib(POMDP)
# Set optional library variables
set_optional_lib_var(DFT)
set_optional_lib_var(GSPN)
set_optional_lib_var(PARS)
set_optional_lib_var(POMDP)

# Helper functions
function(stormpy_module NAME)
    file(GLOB_RECURSE "STORM_${NAME}_SOURCES" "${CMAKE_CURRENT_SOURCE_DIR}/src/${NAME}/*.cpp")
    pybind11_add_module(${NAME} "${CMAKE_CURRENT_SOURCE_DIR}/src/mod_${NAME}.cpp" ${STORM_${NAME}_SOURCES})
    target_include_directories(${NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${storm_INCLUDE_DIR} ${storm-parsers_INCLUDE_DIR} ${storm-counterexamples_INCLUDE_DIR} ${storm-version-info_INCLUDE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src)
    target_link_libraries(${NAME} PRIVATE storm storm-parsers storm-counterexamples storm-version-info )
    if (NOT (${NAME} STREQUAL "core"))
        set_target_properties(${NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${NAME}")
    endif()
endfunction(stormpy_module)

function(stormpy_optional_module NAME ADDITIONAL_LIBS ADDITIONAL_INCLUDES)
    file(GLOB_RECURSE "STORM_${NAME}_SOURCES" "${CMAKE_CURRENT_SOURCE_DIR}/src/${NAME}/*.cpp")
    pybind11_add_module(${NAME} "${CMAKE_CURRENT_SOURCE_DIR}/src/mod_${NAME}.cpp" ${STORM_${NAME}_SOURCES})
    target_include_directories(${NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${storm_INCLUDE_DIR} ${storm-parsers_INCLUDE_DIR} ${storm-counterexamples_INCLUDE_DIR} ${storm-version-info_INCLUDE_DIR} ${ADDITIONAL_INCLUDES} ${CMAKE_CURRENT_BINARY_DIR}/src)
    target_link_libraries(${NAME} PRIVATE storm storm-parsers storm-counterexamples storm-version-info ${ADDITIONAL_LIBS})
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/${NAME}_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${NAME}/_config.py @ONLY)
    set_target_properties(${NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${NAME}")
endfunction(stormpy_optional_module)

# Generate stormpy definitions used during compilation
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/src/config.h)
# Generate pycarl definitions used during compilation
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/definitions.h.in ${CMAKE_CURRENT_BINARY_DIR}/src/pycarl/definitions.h)

stormpy_module(core)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/core_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/_config.py @ONLY)
stormpy_module(info)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/info_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/info/_config.py @ONLY)
stormpy_module(logic)
stormpy_module(storage)
stormpy_module(utility)

# Pycarl Core
######
file(GLOB_RECURSE pycarl_core_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/pycarl_core/*.cpp)
pybind11_add_module(pycarl_core ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_core.cpp ${pycarl_core_SOURCES})
target_include_directories(pycarl_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src/)
target_link_libraries(pycarl_core PRIVATE lib_carl)
set_target_properties(pycarl_core PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl" OUTPUT_NAME "pycarl_core")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_core_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/_config.py @ONLY)

# Optional modules
if(HAVE_STORM_DFT)
    stormpy_optional_module(dft storm-dft "${storm-dft_INCLUDE_DIR}")
endif()
if(HAVE_STORM_GSPN)
    stormpy_optional_module(gspn storm-gspn "${storm-gspn_INCLUDE_DIR}")
endif()
if(HAVE_STORM_PARS)
    stormpy_optional_module(pars storm-pars "${storm-pars_INCLUDE_DIR}")
endif()
if(HAVE_STORM_POMDP)
    stormpy_optional_module(pomdp storm-pomdp "${storm-pomdp_INCLUDE_DIR}")
endif()

message("Configure done")

# TODO Extensions
############


# Typed core
file(GLOB_RECURSE PYCARL_TYPED_CORE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/typed_core/*.cpp)
# GMP
pybind11_add_module(pycarl.gmp ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_gmp.cpp ${PYCARL_TYPED_CORE_SOURCES})
target_include_directories(pycarl.gmp PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src)
target_link_libraries(pycarl.gmp PRIVATE lib_carl)
set_target_properties(pycarl.gmp PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/gmp" OUTPUT_NAME "gmp")
# CLN
pybind11_add_module(pycarl.cln ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_cln.cpp ${PYCARL_TYPED_CORE_SOURCES})
target_include_directories(pycarl.cln PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src)
target_link_libraries(pycarl.cln PRIVATE lib_carl)
target_compile_definitions(pycarl.cln PUBLIC "PYCARL_USE_CLN=ON")
set_target_properties(pycarl.cln PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln" OUTPUT_NAME "cln")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_cln_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln/_config.py @ONLY)


# Formula
#########
file(GLOB_RECURSE PYCARL_FORMULA_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/formula/*.cpp)
pybind11_add_module(pycarl.formula ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_formula.cpp ${PYCARL_FORMULA_SOURCES})
target_include_directories(pycarl.formula PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}  ${CMAKE_CURRENT_BINARY_DIR}/src)
target_link_libraries(pycarl.formula PRIVATE lib_carl)
set_target_properties(pycarl.formula PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/formula" OUTPUT_NAME "formula")

# Typed formula
file(GLOB_RECURSE PYCARL_TYPED_FORMULA_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/typed_formula/*.cpp)
# GMP
pybind11_add_module(pycarl.formula-gmp ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_typed_formula.cpp ${PYCARL_TYPED_FORMULA_SOURCES})
target_include_directories(pycarl.formula-gmp PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}  ${CMAKE_CURRENT_BINARY_DIR}/src)
target_link_libraries(pycarl.formula-gmp PRIVATE lib_carl)
set_target_properties(pycarl.formula-gmp PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/gmp/formula" OUTPUT_NAME "formula")
# CLN
pybind11_add_module(pycarl.formula-cln ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_typed_formula.cpp ${PYCARL_TYPED_FORMULA_SOURCES})
target_include_directories(pycarl.formula-cln PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}  ${CMAKE_CURRENT_BINARY_DIR}/src)
target_link_libraries(pycarl.formula-cln PRIVATE lib_carl)
target_compile_definitions(pycarl.formula-cln PUBLIC "PYCARL_USE_CLN=ON")
set_target_properties(pycarl.formula-cln PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln/formula" OUTPUT_NAME "formula")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_cln_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln/formula/_config.py @ONLY)


# Parse
# #######
# file(GLOB_RECURSE PYCARL_PARSE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/parse/*.cpp)

# pybind11_add_module(pycarl.parse ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_parse.cpp ${PYCARL_PARSE_SOURCES})
# target_include_directories(pycarl.parse PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}  ${CMAKE_CURRENT_BINARY_DIR}/src)
# target_link_libraries(pycarl.parse PRIVATE lib_carl carl-parser)
# set_target_properties(pycarl.parse PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/parse" OUTPUT_NAME "parse")
# configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_parser_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/parse/_config.py @ONLY)

# # Typed parse
# file(GLOB_RECURSE PYCARL_TYPED_PARSE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/typed_parse/*.cpp)
# GMP
# pybind11_add_module(pycarl.parse-gmp ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_typed_parse.cpp ${PYCARL_TYPED_PARSE_SOURCES})
# target_include_directories(pycarl.parse-gmp PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src)
# target_link_libraries(pycarl.parse-gmp PRIVATE lib_carl carl-parser)
# set_target_properties(pycarl.parse-gmp PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/gmp/parse" OUTPUT_NAME "parse")
# configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_parser_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/gmp/parse/_config.py @ONLY)
# # CLN
# pybind11_add_module(pycarl.parse-cln ${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/mod_typed_parse.cpp ${PYCARL_TYPED_PARSE_SOURCES})
# target_include_directories(pycarl.parse-cln PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/src)
# target_link_libraries(pycarl.parse-cln PRIVATE lib_carl carl-parser)
# target_compile_definitions(pycarl.parse-cln PUBLIC "PYCARL_USE_CLN=ON")
# set_target_properties(pycarl.parse-cln PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln/parse" OUTPUT_NAME "parse")
# configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_parser_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/cln/parse/_config.py @ONLY)
