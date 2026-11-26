#!/bin/bash

# Inspired by build process of spead2

set -e -u

brew install ccache automake boost cln ginac glpk gmp hwloc libarchive xerces-c z3
export CCACHE_DIR="${CCACHE_DIR:-$RUNNER_TEMP/ccache}"

# Install Storm
git clone https://github.com/stormchecker/storm.git -b ${STORM_VERSION}
cd storm
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE:-Release} -DSTORM_BUILD_TESTS=OFF -DSTORM_BUILD_EXECUTABLES=OFF -DSTORM_PORTABLE=ON -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
make -j ${NR_JOBS}
sudo chown runner:admin /usr/local/ # /usr/local is not writable by default on macOS 14+ runners, see https://github.com/actions/runner-images/issues/9272
make install
cd ..
