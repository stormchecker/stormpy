#!/bin/bash

# Inspired by build process of spead2

set -e -u

ginac_version=1.8.10

dnf install -y boost-devel cln-devel glpk-devel gmp-devel hwloc-devel libarchive-devel xerces-c-devel z3-devel eigen3-devel # missing ginac-devel

cd /tmp

# Install ginac
curl -fsSLO https://www.ginac.de/ginac-${ginac_version}.tar.bz2
tar -jxf ginac-${ginac_version}.tar.bz2
cd ginac-${ginac_version}
./configure CXXFLAGS="-O2"
make -j ${NR_JOBS}
make install
cd ..

# Install Storm
git clone https://github.com/stormchecker/storm.git -b ${STORM_VERSION}
cd storm
mkdir build
cd build
cmake .. -DSTORM_BUILD_TESTS=OFF -DSTORM_BUILD_EXECUTABLES=OFF -DSTORM_PORTABLE=ON
make -j ${NR_JOBS}
make install
cd ..
rm -rf build
