#!/bin/bash

# Inspired by build process of spead2

set -e -u

brew install ccache automake boost cln ginac glpk hwloc z3 xerces-c

# Install Storm
git clone https://github.com/moves-rwth/storm.git -b ${STORM_VERSION}
cd storm
mkdir build
cd build
cmake .. -DSTORM_BUILD_TESTS=OFF -DSTORM_BUILD_EXECUTABLES=OFF -DSTORM_PORTABLE=ON
make -j ${NR_JOBS}
sudo chown runner:admin /usr/local/ # Permission differ in macOS 14, see https://github.com/actions/runner-images/issues/9272
make install
cd ..
rm -rf build
