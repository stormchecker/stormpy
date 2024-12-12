# Base Dockerfile for using stormpy
###################################
# The Docker image can be built by executing:
# docker build -t yourusername/stormpy .
# A different Storm base image can be set from the commandline with:
# --build-arg STORM_BASE=<new_base_image>

# Set Storm base image
ARG STORM_BASE=movesrwth/storm:stable
FROM $STORM_BASE
MAINTAINER Matthias Volk <m.volk@utwente.nl>


# Configuration arguments
#########################
# The arguments can be set from the commandline with:
# --build-arg <arg_name>=<value>

# CMake build type
ARG build_type=Release
# Additional arguments for compiling stormpy
ARG setup_args=""
# Additional CMake arguments for carl
ARG carl_cmake_args=""
# Number of threads to use for parallel compilation
ARG no_threads=2
# Carl-storm version
ARG carl_version=master


# Install dependencies
######################
# Uncomment to update packages beforehand
RUN apt-get update -qq
RUN apt-get install -y --no-install-recommends \
    maven \
    uuid-dev \
    python3 \
    python3-venv
# Packages maven and uuid-dev are required for carl-parser

# Build carl-parser
###################
WORKDIR /opt/

# Obtain carl-parser from public repository
RUN git clone https://github.com/moves-rwth/carl-parser.git

# Switch to build directory
RUN mkdir -p /opt/carl-parser/build
WORKDIR /opt/carl-parser/build

# Configure carl-parser
RUN cmake .. -DCMAKE_BUILD_TYPE=$build_type

# Build carl-parser
RUN make carl-parser -j $no_threads


# Set-up virtual environment
############################
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install setuptools

# Build stormpy
###############
RUN mkdir /opt/stormpy
WORKDIR /opt/stormpy

# Copy the content of the current local stormpy repository into the Docker image
COPY . .

# Build stormpy
RUN python setup.py build_ext $setup_args -j $no_threads develop

# Uncomment to build optional dependencies
#RUN pip install -e '.[doc,numpy]'"
