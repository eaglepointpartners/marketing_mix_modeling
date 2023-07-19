FROM condaforge/miniforge3

# add missing SSH client
RUN apt-get update && apt-get install -y openssh-client

# setup conda environment with Python
RUN conda create -y -n mmm python=3.11
RUN conda install -n mmm -y \
    "pymc>=5,<6" \
    pymc-marketing \
    pandas \
    matplotlib \
    seaborn \
    ipykernel
