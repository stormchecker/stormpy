cmake_minimum_required(VERSION 3.15)

project(stormpy)

option(USE_STORM_DFT "Enable support for DFTs" ON)
option(USE_STORM_GSPN "Enable support for GSPNs" ON)
option(USE_STORM_PARS "Enable support for parametric models" ON)
option(USE_STORM_POMDP "Enable support for POMDPs" ON)
option(STORM_COMPILE_WITH_ADDRESS_SANITIZER "Sets whether to compile with AddressSanitizer enabled" OFF)
option(STORMPY_DISABLE_SIGNATURE_DOC "Disable the signature in the documentation" OFF)
MARK_AS_ADVANCED(STORMPY_DISABLE_SIGNATURE_DOC)
set(PYBIND_VERSION "" CACHE STRING "Pybind11 version to use")
MARK_AS_ADVANCED(PYBIND_VERSION)
set(STORM_DIR_HINT "" CACHE STRING "A hint where the Storm library can be found.")

if (STORM_COMPILE_WITH_ADDRESS_SANITIZER)
    message(STATUS "Storm - Enabling AddressSanitizer")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -shared-libasan")
endif()

find_package(storm REQUIRED HINTS ${STORM_DIR_HINT})

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
set(PYCARL_IMPORTS "import pycarl")
if (STORM_USE_CLN_EA OR STORM_USE_CLN_RF)
    set(PYCARL_IMPORTS "${PYCARL_IMPORTS}\nimport pycarl.cln")
endif()
if (NOT STORM_USE_CLN_EA OR NOT STORM_USE_CLN_RF)
    set(PYCARL_IMPORTS "${PYCARL_IMPORTS}\nimport pycarl.gmp")
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

# Generate definitions used during compilation
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/src/config.h)


stormpy_module(core)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/core_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/_config.py @ONLY)
stormpy_module(info)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/info_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/info/_config.py @ONLY)
stormpy_module(logic)
stormpy_module(storage)
stormpy_module(utility)

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

