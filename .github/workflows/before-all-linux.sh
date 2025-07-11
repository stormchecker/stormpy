#!/bin/bash

# Inspired by build process of spead2

set -e -u

sccache_version=0.10.0
boost_version=1.88.0
boost_version_under=${boost_version//./_}
ginac_version=1.8.9

dnf install -y boost-devel cln-devel gmp-devel glpk-devel hwloc-devel z3-devel xerces-c-devel eigen3-devel # missing ginac and boost

cd /tmp

# Install sccache
curl -fsSLO https://github.com/mozilla/sccache/releases/download/v${sccache_version}/sccache-v${sccache_version}-$(arch)-unknown-linux-musl.tar.gz
tar -zxf sccache-v${sccache_version}-$(arch)-unknown-linux-musl.tar.gz
cp sccache-v${sccache_version}-$(arch)-unknown-linux-musl/sccache /usr/bin

## Install boost
#curl -fsSLO https://archives.boost.io/release/${boost_version}/source/boost_${boost_version_under}.tar.bz2
#tar -jxf boost_${boost_version_under}.tar.bz2
## Quick-n-dirty approach (much faster than doing the install, which copies thousands of files)
#ln -s /tmp/boost_${boost_version_under}/boost /usr/include/boost

# Install ginac
curl -fsSLO https://www.ginac.de/ginac-${ginac_version}.tar.bz2
tar -jxf ginac-${ginac_version}.tar.bz2
cd ginac-${ginac_version}
export CXXFLAGS="-Wall -O2"
./configure
make
make install