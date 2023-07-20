# Marketing Mix Modeling

For collaborating and developing Bayesian MMM models in PyMC

## Dev Container

To help with reproducibility in this projectdo, the provided Dockerfile is intended to be used
in a Visual Studio (VS) Code devcontainer.

#### Key features:
- Python 3.11
- Conda environment with PyMC 5+
- Jupyter Notebook integration

#### Prerequisites:
- [VS Code](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)

#### Getting started:

1. Open VS Code and make sure to have the Dev Containers extension installed.
<img width="764" alt="dev container extension" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/f8293184-af7f-4efd-9c57-2523a4cf03f6">  

2. Open repo folder in a dev container. The contents of the `.devcontainer` folder configure the container using Dockerfile. The Docker image will need to be built from scratch the first time, so be patient.
<img width="733" alt="initiate dev container" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/a6ce3fb6-ab6d-4090-94c9-867fa7dbd4f5">  

3. The dev container is configured to edit and run Jupyter notebooks directly within VS Code. Test out your new environment by opening notebook `example/pymc_mmm.ipynb`. Select the `mmm` kernel to use the installed Conda environment.
<img width="980" alt="select python environment" src="https://github.com/eaglepointpartners/marketing_mix_modeling/assets/4998142/3d503b5d-110e-4bc8-8f7e-f731f0bd5e95">
