FROM condaforge/mambaforge

# add missing SSH client
RUN apt-get update && apt-get install -y openssh-client

# setup Python environment with Conda
COPY environment.yml .
RUN mamba env create --file environment.yml
# RUN mamba install -n mmm -y \
#     "pymc>=5,<6" \
#     "pymc-marketing>=0.2,<0.3" \
#     "numpy<1.26" \
#     python-duckdb \
#     pandas \
#     pyyaml \
#     matplotlib \
#     seaborn \
#     python-graphviz \
#     ipykernel
