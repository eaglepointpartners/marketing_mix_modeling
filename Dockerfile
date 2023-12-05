FROM condaforge/mambaforge

# add missing SSH client
RUN apt-get update && apt-get install -y openssh-client

# setup Python environment with Conda
COPY environment.yml .
RUN mamba env create --file environment.yml
