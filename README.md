# Marketing Mix Modeling

For collaborating and developing Bayesian MMM models in PyMC

## Dev Container

To help with reproducibility in this projectdo, the provided Dockerfile is intended to be used
in a Visual Studio (VS) Code devcontainer.

#### Key features:
- Python 3.11
- Conda environment with PyMC 5+
- Jupyter Notebook integration
- Access to local data sets
- DuckDB for working with Parquet

#### Prerequisites:
- [VS Code](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)

#### Getting started:

1. Open VS Code and make sure to have the Dev Containers extension installed.
<img width="764" alt="dev container extension" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/f8293184-af7f-4efd-9c57-2523a4cf03f6">  

2. Set the environment variable `MMM_DATA_PATH=/local/path/to/data/directory`. This variable will need to point to a valid directory in order to build the dev container. See the "Incorporating Data" section below.  

3. Open repo folder in a dev container. The contents of the `.devcontainer` folder configure the container using Dockerfile. The Docker image will need to be built from scratch the first time, so be patient.
<img width="733" alt="initiate dev container" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/a6ce3fb6-ab6d-4090-94c9-867fa7dbd4f5">  

4. The dev container is configured to edit and run Jupyter notebooks directly within VS Code. Test out your new environment by opening notebook `example/pymc_mmm.ipynb`. Select the `mmm` kernel to use the installed Conda environment.
<img width="980" alt="select python environment" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/3d503b5d-110e-4bc8-8f7e-f731f0bd5e95">

## Incorportating Data

Please keep this repo free of data, credentials and other secrets (one exception being data accompanying example notebook). Instead, the dev container is setup to use an environment variable `MMM_DATA_PATH` to access datasets outside this repo. When the dev container gets built, the contents of your local folder will get mounted to `/root/data` within the container. Try it out with `example/using_data.ipynb`.
