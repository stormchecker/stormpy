cmake_minimum_required(VERSION 3.15)

project(storm-version)

include(FetchContent)

set(INSTALL_STORM TRUE CACHE BOOL "Whether to install storm from scratch.")
set(STORM_DIR_HINT "" CACHE STRING "A hint where the Storm library can be found.")
set(CARL_DIR_HINT "" CACHE STRING "A hint where the Carl library can be found.")
set(CARLPARSER_DIR_HINT "" CACHE STRING "A hint where the Carl-parser library can be found.")

if(INSTALL_STORM)
    message(STATUS "Installing Storm from scratch")
endif()

find_package(storm REQUIRED HINTS ${STORM_DIR_HINT})
find_package(carl REQUIRED HINTS ${CARL_DIR_HINT})
find_package(carlparser QUIET HINTS ${CARLPARSER_DIR_HINT})

include(${CMAKE_CURRENT_SOURCE_DIR}/macros.cmake)

# Set configuration
set(STORM_DIR ${storm_DIR})
set(STORM_VERSION ${storm_VERSION})
set(STORM_LIBS ${storm_LIBRARIES})

# Check for optional Storm libraries
storm_with_lib(DFT)
storm_with_lib(GSPN)
storm_with_lib(PARS)
storm_with_lib(POMDP)

# Set variables
set_variable_string(STORM_CLN_EA_BOOL ${STORM_USE_CLN_EA})
set_variable_string(STORM_CLN_RF_BOOL ${STORM_USE_CLN_RF})

set_variable_string(STORM_XERCES_BOOL ${STORM_HAVE_XERCES})
set_variable_string(STORM_SPOT_BOOL ${STORM_HAVE_SPOT})

set_variable_string(HAVE_STORM_DFT_BOOL ${HAVE_STORM_DFT})
set_variable_string(HAVE_STORM_GSPN_BOOL ${HAVE_STORM_GSPN})
set_variable_string(HAVE_STORM_PARS_BOOL ${HAVE_STORM_PARS})
set_variable_string(HAVE_STORM_POMDP_BOOL ${HAVE_STORM_POMDP})

# Set configuration
set(CARL_DIR ${carl_DIR})
set(CARL_VERSION ${carl_VERSION})
if(carlparser_FOUND)
    set(CARL_PARSER_DIR ${carlparser_DIR})
    set_variable_string(CARL_WITH_PARSER "True")
else()
    set(CARL_PARSER_DIR "")
    set_variable_string(CARL_WITH_PARSER "False")
endif()
if(CARL_USE_CLN_NUMBERS)
    set_variable_string(CARL_WITH_CLN "True")
else()
    set_variable_string(CARL_WITH_CLN "False")
endif()

# Write configuration file
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.py.in ${CMAKE_CURRENT_BINARY_DIR}/generated/config.py @ONLY)
