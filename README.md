## Marketing Mix Modeling

For collaborating and developing Bayesian MMM models in PyMC

### Dev Container

To ensure the reproducibility of this project, the provided Dockerfile is intended to be used
in a Visual Studio (VS) Code devcontainer.

##### Key features:
- Python 3.11
- Conda environment with PyMC 5+
- Jupyter Notebook integration

##### Prerequisites:
- VS Code
- Docker

##### Getting started:

Open VS Code and make sure to have the Dev Containers extension installed.


Open repo folder in a dev container. The contents of the `.devcontainer` folder configure the container using Dockerfile.


The dev container is configured to edit and run Jupyter notebooks directly within VS Code. Test out your new environment by opening notebook `example/pymc_mmm.ipynb`. Select the `mmm` kernel to use the installed Conda environment.