# Binder image for stormpy
# Build from root level with:
#     docker build -t binder -f binder/Dockerfile .
# Run with:
#     docker run -it --rm -p 8888:8888 binder jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888
FROM movesrwth/stormpy:1.9.0
LABEL org.opencontainers.image.authors="dev@stormchecker.org"


##########
# Create user
##########

# Ubuntu base image already uses UID/GID 1000
# Change it so the Binder user can use 1000
RUN usermod -u 1001 ubuntu
RUN groupmod -g 1001 ubuntu

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Change the owner of the virtual environment
WORKDIR /opt
USER root
RUN chown -R ${NB_UID} venv
USER ${NB_USER}

##########
# Install dependencies
##########

# Jupyter notebook and Jupyterlab
RUN pip install --no-cache-dir notebook==6.5.7
RUN pip install --no-cache-dir jupyterlab==4.1.8
# Use older version of jupyter-server to avoid issue with token
# see https://github.com/jupyter/notebook/issues/6702#issuecomment-1412832225
RUN pip install --no-cache-dir jupyter-server==1.24.0
# Dependencies for stormpy
RUN pip install --no-cache-dir numpy==1.26.4

##########
# Prepare files for notebooks
##########

# Copy files
WORKDIR ${HOME}
COPY doc/source/*.ipynb notebooks/
COPY doc/source/doc/ notebooks/doc/
COPY examples/ examples/

# Set owner of files to user
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# Add missing path
ENV PATH="$HOME/.local/bin:$PATH"

# Unset entrypoint
ENTRYPOINT []
