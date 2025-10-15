cmake_minimum_required(VERSION 3.24)

# Scikit-build-core sets these values
project(
    ${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX C
)

# Set configurations
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/macros.cmake)

set(CMAKE_CXX_STANDARD 20)

# Configuration options
set(STORM_DIR_HINT "" CACHE STRING "A hint where the Storm library can be found.")
option(ALLOW_STORM_SYSTEM "Allow finding a Storm version on the system" ON)
option(ALLOW_STORM_FETCH "Allow fetching Storm" ON)
# No defaults set here, they should be governed by the pyproject.toml
set(STORM_GIT_REPO "" CACHE STRING  "Git repo used for fetching Storm")
set(STORM_GIT_TAG "" CACHE STRING "Git repo tag used for fetching Storm")
option(USE_STORM_DFT "Enable support for DFTs" ON)
option(USE_STORM_GSPN "Enable support for GSPNs" ON)
option(USE_STORM_PARS "Enable support for parametric models" ON)
option(USE_STORM_POMDP "Enable support for POMDPs" ON)
option(USE_CLN_NUMBERS "Make cln numbers available in pycarl" ON)
option(USE_PARSER "Make carlparser available in pycarl" ON)
set(CARLPARSER_DIR_HINT "" CACHE STRING "A hint where the Carl-parser library can be found.")
option(STORMPY_DISABLE_SIGNATURE_DOC "Disable the signature in the documentation" OFF)
MARK_AS_ADVANCED(STORMPY_DISABLE_SIGNATURE_DOC)
option(COMPILE_WITH_CCACHE "Compile using CCache (if found)" ON)
mark_as_advanced(COMPILE_WITH_CCACHE)
option(STORMPY_INFO_PRETEND_FETCH "[INTERNAL] Use for overriding some flags in the info by cibuildwheel." OFF)
mark_as_advanced(STORMPY_INFO_PRETEND_FETCH)

# Check whether inputs are sane.
if (NOT ALLOW_STORM_SYSTEM AND NOT ALLOW_STORM_FETCH)
    message(FATAL_ERROR "Stormpy - Storm must be either fetched or used from system, yet ALLOW_STORM_SYSTEM=OFF and ALLOW_STORM_FETCH=OFF.")
endif()
if (NOT ALLOW_STORM_SYSTEM AND STORM_DIR_HINT)
	message(WARNING "Stormpy - Storm directory hint was given but ALLOW_STORM_SYSTEM=OFF.")
endif()
if (NOT USE_PARSER AND CARLPARSER_DIR_HINT)
	message(WARNING "Stormpy - Carl-parser directory hint was given but USE_PARSER=OFF.")
endif()

find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Stormpy - Using pybind11 version ${pybind11_VERSION}")

# Helper function to print path where library was found and check whether hint was used
function(check_hint NAME DIR_FOUND HINT_DIR FOUND_VERSION)
    # Get absolute path
    get_filename_component(PATH_FOUND ${DIR_FOUND} ABSOLUTE)
    # Print path
    if (NOT "${FOUND_VERSION}" STREQUAL "")
        message(STATUS "Stormpy - Using ${NAME} version ${FOUND_VERSION} from ${PATH_FOUND}")
    else()
        message(STATUS "Stormpy - Using ${NAME} from ${PATH_FOUND}")
    endif()

    # Check that hint was used
    if (NOT "${HINT_DIR}" STREQUAL "")
        get_filename_component(PATH_HINT ${HINT_DIR} ABSOLUTE)
        if (NOT "${PATH_FOUND}" STREQUAL "${PATH_HINT}")
            MESSAGE(SEND_ERROR "Stormpy - Using different ${NAME} directory ${PATH_FOUND} instead of given ${HINT_DIR}!")
        endif()
    endif()
endfunction(check_hint)

if(ALLOW_STORM_SYSTEM)
    set(STORM_MIN_VERSION "1.11.0")
    if (ALLOW_STORM_FETCH)
        find_package(storm HINTS ${STORM_DIR_HINT}) # NOT REQUIRED, can be fetched.
    else()
        find_package(storm REQUIRED HINTS ${STORM_DIR_HINT}) # REQUIRED, cannot be fetched.
    endif()
    if (storm_FOUND)
        check_hint("Storm" ${storm_DIR} "${STORM_DIR_HINT}" ${storm_VERSION})
        # Check Storm version
        if (${storm_VERSION} VERSION_LESS ${STORM_MIN_VERSION})
            MESSAGE(FATAL_ERROR "Stormpy - Storm version ${storm_VERSION} from ${storm_DIR} is not supported anymore!\nStormpy requires at least Storm version >= ${STORM_MIN_VERSION}.\nFor more information, see https://moves-rwth.github.io/stormpy/installation.html#compatibility-of-stormpy-and-storm")
        endif()
        if (STORM_VERSION_DEV)
            message(WARNING "Stormpy - Using a development version of Storm. This may lead to issues and we recommend using a release of Storm instead.")
        endif()

        set(STORM_FROM_SYSTEM TRUE)
        get_filename_component(STORM_DIR_PATH ${storm_DIR} ABSOLUTE)
        set(STORM_DIR "\"${STORM_DIR_PATH}\"")
        if (STORMPY_INFO_PRETEND_FETCH)
            # This is a workaround for our wheel construction which uses a system version for efficiency,
            # but should provide wheels as if it they were fetched.
            message(WARNING "Stormpy - The behavior of STORMPY_INFO_PRETEND_FETCH is something we only want when building wheels. Please ensure that STORM_GIT_REPO and STORM_GIT_TAG are set accordingly.")
            set(STORM_FETCHED_FROM_REPO ${STORM_GIT_REPO})
            set(STORM_FETCHED_FROM_TAG ${STORM_GIT_TAG})
            set(STORM_FROM_SYSTEM FALSE)
            set(STORM_DIR "None")
        endif()
        # Set dependency variables
        set_dependency_var(SPOT)
        set_dependency_var(XERCES)
        # Check for optional Storm libraries
        storm_with_lib(DFT)
        storm_with_lib(GSPN)
        storm_with_lib(PARS)
        storm_with_lib(POMDP)
    elseif (STORM_DIR_HINT)
        MESSAGE(FATAL_ERROR "Stormpy - Storm could not be found in ${STORM_DIR_HINT}.")
    endif()
endif()

if (NOT storm_FOUND)
    if (ALLOW_STORM_FETCH)
        if (STORMPY_INFO_PRETEND_FETCH)
            message(FATAL_ERROR "Stormpy - Do not set STORMPY_INFO_PRETEND_FETCH when fetching." )
        endif()
        # Storm not yet available.
        include(FetchContent)
        SET(FETCHCONTENT_QUIET OFF)
        SET(STORM_BUILD_EXECUTABLES OFF)
        SET(STORM_BUILD_TESTS OFF)
        FetchContent_Declare(
                storm
                GIT_REPOSITORY ${STORM_GIT_REPO}
                GIT_TAG        ${STORM_GIT_TAG}
        )
        FETCHCONTENT_MAKEAVAILABLE(storm)
        include(${storm_BINARY_DIR}/stormOptions.cmake)
        set(HAVE_STORM_DFT TRUE)
        set(HAVE_STORM_GSPN TRUE)
        set(HAVE_STORM_PARS TRUE)
        set(HAVE_STORM_POMDP TRUE)
        # Set dependency variables
        set_dependency_var(SPOT)
        set_dependency_var(XERCES)
        if (FETCHCONTENT_SOURCE_DIR_storm)
            # We are setting the Storm source to be something local from the outside.
            set(STORM_FETCHED_FROM_REPO ${FETCHCONTENT_SOURCE_DIR_storm})
            set(STORM_FETCHED_FROM_TAG "__local-source-dir__")
        else()
            set(STORM_FETCHED_FROM_REPO ${STORM_GIT_REPO})
            set(STORM_FETCHED_FROM_TAG ${STORM_GIT_TAG})
        endif()
        set(STORM_FROM_SYSTEM FALSE)
        set(STORM_DIR "None")
    else()
        # Should not be reachable because storm is required if we cannot fetch it.
        message(FATAL_ERROR "Stormpy - No version of Storm configured. This situation should not occur. Please contact the Storm developers.")
    endif()
endif()


find_package(carlparser QUIET HINTS ${CARLPARSER_DIR_HINT})
if (carlparser_FOUND)
    check_hint("carl-parser" ${carlparser_DIR} "${CARLPARSER_DIR_HINT}" "")
    get_filename_component(CARL_PARSER_DIR_PATH ${carlparser_DIR} ABSOLUTE)
    set(CARL_PARSER_DIR "\"${CARL_PARSER_DIR_PATH}\"")
else()
    if (CARLPARSER_DIR_HINT)
	    MESSAGE(FATAL_ERROR "Stormpy - Carl-parser could not be found in ${CARL_PARSER_DIR_HINT}.")
    endif()
    set(CARL_PARSER_DIR "None")
endif()

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib/stormpy")

# This sets interprocedural optimization off as this leads to some problems on some systems
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF)

if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    # This sets the default visibility from hidden to default,
    # which is recommended *not* to do, but leads to errors otherwise.
    set(CMAKE_CXX_VISIBILITY_PRESET "default")
endif()

# RPATH settings (https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling#always-full-rpath)
# don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
# when building, don't use the install RPATH already (but only when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
# the RPATH to be used when installing
if(APPLE)
    set(RELPOS_STRING "@loader_path")
else()
    set(RELPOS_STRING "$ORIGIN")
endif()
SET(CMAKE_INSTALL_RPATH "${RELPOS_STRING}/../../../lib/storm;${RELPOS_STRING}/../../../lib/storm/resources;${RELPOS_STRING}/../../lib/storm;${RELPOS_STRING}/../../lib/storm/resources;${RELPOS_STRING}/../lib/storm;${RELPOS_STRING}/../lib/storm/resources;${RELPOS_STRING}/lib/storm;${RELPOS_STRING}/lib/storm/resources;${RELPOS_STRING};${RELPOS_STRING}/resources")
# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
SET(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)


# Workaround for issue with Boost >= 1.81
# TODO: In the future, this should be inherited somehow from Storm.
find_package(Boost 1.70 QUIET REQUIRED CONFIG)
if (Boost_FOUND)
    if (${Boost_VERSION} VERSION_GREATER_EQUAL "1.81.0")
        message(STATUS "Stormpy - Using workaround for Boost >= 1.81")
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_PHOENIX_STL_TUPLE_H_")
    endif()
endif()

# CCache
if(COMPILE_WITH_CCACHE)
    find_program(CCACHE_FOUND ccache)
    mark_as_advanced(CCACHE_FOUND)
    if(CCACHE_FOUND)
        message(STATUS "Stormpy - Using ccache")
        set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
        set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache)
    else()
        message(STATUS "Stormpy - Could not find ccache.")
    endif()
else()
    message(STATUS "Stormpy - Disabled use of ccache.")
endif()

# Set number types from Carl
set_variable_string(STORM_USE_CLN_EA_BOOL ${STORM_USE_CLN_EA})
set_variable_string(STORM_USE_CLN_RF_BOOL ${STORM_USE_CLN_RF})
set_variable_string(STORMPY_PRETEND_FETCH ${STORMPY_INFO_PRETEND_FETCH})
set_variable_string(STORM_DEVELOPER_VERSION ${STORM_VERSION_DEV})
if (STORM_FETCHED_FROM_REPO)
    set(STORM_ORIGIN_REPO "\"${STORM_FETCHED_FROM_REPO}\"")
else()
    set(STORM_ORIGIN_REPO "None")
endif()
if(STORM_FETCHED_FROM_TAG)
    set(STORM_ORIGIN_TAG "\"${STORM_FETCHED_FROM_TAG}\"")
else()
    set(STORM_ORIGIN_TAG "None")
endif()
set_variable_string(STORM_FROM_SYSTEM ${STORM_FROM_SYSTEM})
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
# Check support for carl-parser
if(USE_PARSER AND carlparser_FOUND)
    set(PYCARL_HAS_PARSE ON)
else()
    set(PYCARL_HAS_PARSE OFF)
endif()
set_variable_string(CARL_WITH_PARSER ${PYCARL_HAS_PARSE})
# Check support for CLN
if(STORM_USE_CLN_EA OR STORM_USE_CLN_RF)
    set(PYCARL_HAS_CLN ON)
else()
    set(PYCARL_HAS_CLN OFF)
endif()
set_variable_string(CARL_WITH_CLN ${PYCARL_HAS_CLN})

# Set optional library variables
set_optional_lib_var(DFT)
set_optional_lib_var(GSPN)
set_optional_lib_var(PARS)
set_optional_lib_var(POMDP)


# Helper functions
######
# Helper function to build a general module
function(build_module MOD_NAME # Module name
                      OUT_DIR OUT_NAME # Output directory and name for library
                      MOD_FILE SOURCE_PATH # Module source file and regex for all module source files
                      ADDITIONAL_INCLUDES ADDITIONAL_LIBS) # Additional include directories and libraries
    file(GLOB_RECURSE "${MOD_NAME}_SOURCES" "${CMAKE_CURRENT_SOURCE_DIR}/src/${SOURCE_PATH}")
    pybind11_add_module(${MOD_NAME} "${CMAKE_CURRENT_SOURCE_DIR}/src/${MOD_FILE}" ${${MOD_NAME}_SOURCES})
    target_include_directories(${MOD_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${ADDITIONAL_INCLUDES} ${CMAKE_CURRENT_BINARY_DIR}/src)
    target_link_libraries(${MOD_NAME} PRIVATE ${ADDITIONAL_LIBS})
    set_target_properties(${MOD_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${OUT_DIR}" OUTPUT_NAME "_${OUT_NAME}")
    install(TARGETS ${MOD_NAME} DESTINATION ${OUT_DIR})
endfunction(build_module)

# Helper function to build stormpy module
function(build_stormpy_module MOD_NAME OUT_DIR OUT_NAME MOD_FILE SOURCE_PATH ADDITIONAL_INCLUDES ADDITIONAL_LIBS)
    build_module("${MOD_NAME}"
                 "${OUT_DIR}" "${OUT_NAME}"
                 "${MOD_FILE}" "${SOURCE_PATH}"
                 "${storm_INCLUDE_DIR};${storm-parsers_INCLUDE_DIR};${ADDITIONAL_INCLUDES}"
                 "storm;storm-parsers;${ADDITIONAL_LIBS}")
endfunction(build_stormpy_module)
function(stormpy_module MOD_NAME OUT_DIR ADDITIONAL_INCLUDES ADDITIONAL_LIBS)
    build_stormpy_module("stormpy_${MOD_NAME}"
                         "${OUT_DIR}" "${MOD_NAME}"
                         "mod_${MOD_NAME}.cpp" "${MOD_NAME}/*.cpp"
                         "${ADDITIONAL_INCLUDES}"
                         "${ADDITIONAL_LIBS}")
endfunction(stormpy_module)
# Helper function to build an optional stormpy module (if supported and required)
function(stormpy_optional_module MOD_NAME DESCRIPTION)
    string(TOUPPER "${MOD_NAME}" LIB_NAME)
    if(HAVE_STORM_${LIB_NAME} AND USE_STORM_${LIB_NAME})
        build_stormpy_module("stormpy_${MOD_NAME}"
                             "${MOD_NAME}" "${MOD_NAME}"
                             "mod_${MOD_NAME}.cpp" "${MOD_NAME}/*.cpp"
                             "${storm-${MOD_NAME}_INCLUDE_DIR}"
                             "storm-${MOD_NAME}")
        MESSAGE(STATUS "Stormpy - Support for ${DESCRIPTION} found and included.")
    else()
        MESSAGE(WARNING "Stormpy - No support for ${DESCRIPTION}!")
    endif()
endfunction(stormpy_optional_module)

# Helper function to build a pycarl module
function(build_pycarl_module MOD_NAME OUT_DIR OUT_NAME MOD_FILE SOURCE_PATH ADDITIONAL_INCLUDES ADDITIONAL_LIBS)
    build_module("${MOD_NAME}"
                 "${OUT_DIR}" "${OUT_NAME}"
                 "${MOD_FILE}" "${SOURCE_PATH}"
                 "${carl_INCLUDE_DIR};${ADDITIONAL_INCLUDES}"
                 "lib_carl;${ADDITIONAL_LIBS}")
endfunction(build_pycarl_module)
function(pycarl_module MOD_NAME ADDITIONAL_INCLUDES ADDITIONAL_LIBS)
    build_pycarl_module("pycarl_${MOD_NAME}"
                        "pycarl/${MOD_NAME}" "${MOD_NAME}"
                        "pycarl/mod_${MOD_NAME}.cpp" "pycarl/${MOD_NAME}/*.cpp"
                        "${ADDITIONAL_INCLUDES}"
                        "${ADDITIONAL_LIBS}")
endfunction(pycarl_module)
# Helper function to build an optional pycarl module
function(pycarl_typed_module MOD_NAME TYPE ADDITIONAL_INCLUDES ADDITIONAL_LIBS)
    build_pycarl_module("pycarl_${MOD_NAME}_${TYPE}"
                        "pycarl/${TYPE}/${MOD_NAME}" "${MOD_NAME}"
                        "pycarl/mod_typed_${MOD_NAME}.cpp" "pycarl/typed_${MOD_NAME}/*.cpp"
                        "${ADDITIONAL_INCLUDES}"
                        "${ADDITIONAL_LIBS}")
endfunction(pycarl_typed_module)

# Generate stormpy definitions used during compilation
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/src/config.h)
# Generate pycarl definitions used during compilation
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/pycarl/definitions.h.in ${CMAKE_CURRENT_BINARY_DIR}/src/pycarl/definitions.h)


# Build stormpy
######
# Build stormpy modules
stormpy_module(core "." "${storm-counterexamples_INCLUDE_DIR}" storm-counterexamples)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/core_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/_config.py @ONLY)
stormpy_module(info info "${storm-version-info_INCLUDE_DIR}" storm-version-info)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/info_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/info/_config.py @ONLY)
stormpy_module(logic logic "" "")
stormpy_module(storage storage "" "")
stormpy_module(utility utility "" "")

# Build optional stormpy modules
stormpy_optional_module(dft "DFT")
stormpy_optional_module(gspn "GSPN")
stormpy_optional_module(pars "parametric models")
stormpy_optional_module(pomdp "POMDP")

# Build pycarl modules
######
# Pycarl core
build_pycarl_module(pycarl_core
                    "pycarl" "pycarl_core"
                    "pycarl/mod_core.cpp" "pycarl/core/*.cpp"
                    ""
                    "")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/pycarl_core_config.py.in ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/pycarl/_config.py @ONLY)
build_pycarl_module(pycarl_gmp
                    "pycarl/gmp" "gmp"
                    "pycarl/mod_gmp.cpp" "pycarl/typed_core/*.cpp"
                    ""
                    "")
if (PYCARL_HAS_CLN)
    build_pycarl_module(pycarl_cln
                        "pycarl/cln" "cln"
                        "pycarl/mod_cln.cpp" "pycarl/typed_core/*.cpp"
                        ""
                        "")
    target_compile_definitions(pycarl_cln PUBLIC "PYCARL_USE_CLN=ON")
endif()

# Pycarl formula
pycarl_module(formula "" "")
pycarl_typed_module(formula gmp "" "")
if (PYCARL_HAS_CLN)
    pycarl_typed_module(formula cln "" "")
    target_compile_definitions(pycarl_formula_cln PUBLIC "PYCARL_USE_CLN=ON")
endif()

# Pycarl parse
if (PYCARL_HAS_PARSE)
    MESSAGE(STATUS "Stormpy - Support for carl-parser found and included.")
    pycarl_module(parse "${carlparser_INCLUDE_DIR}" carl-parser)
    pycarl_typed_module(parse gmp "${carlparser_INCLUDE_DIR}" carl-parser)
    if (PYCARL_HAS_CLN)
        pycarl_typed_module(parse cln "${carlparser_INCLUDE_DIR}" carl-parser)
        target_compile_definitions(pycarl_parse_cln PUBLIC "PYCARL_USE_CLN=ON")
    endif()
else()
    MESSAGE(WARNING "Stormpy - No support for carl-parser")
endif()
