# Binder image for stormpy
# Build from root level with:
#     docker build -t binder -f binder/Dockerfile .
# Run with:
#     docker run -it --rm -p 8888:8888 binder jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888

FROM quay.io/jupyter/minimal-notebook:2026-03-09
LABEL org.opencontainers.image.authors="dev@stormchecker.org"

# Install Python libraries from requirements.txt
COPY --chown=${NB_UID}:${NB_GID} binder/requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Copy files
COPY doc/source/*.ipynb notebooks/
COPY doc/source/doc/ notebooks/doc/
COPY examples/ examples/
