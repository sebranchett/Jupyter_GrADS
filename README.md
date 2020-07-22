# Jupyter_GrADS

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sebranchett/Jupyter_GrADS/master?filepath=grads_data.ipynb)

Simple Jupyter notebook to display GrADS data for the ExoSPEEDY project.

The easiest way to get this Jupyter notebook running is to use the Binder button above.

If you want to use your own data on your own computer, the easiest way to get everything set up is using Anaconda, as described below.

Recommended reading: https://ipywidgets.readthedocs.io/en/latest/user_install.html

Note: nodejs didn't install properly on my Windows 7 machine, so I installed it from internet.

This notebook works on Jupyter Notebook, but not on Jupyter Lab.

## Create and activate a conda environment

RUN 
```conda create --name grads --file requirements.txt -c conda-forge```

You only have to create the environment once.

RUN 
```conda activate grads```

## Create and install a kernel called 'grads'
This allows you to use the environment just created in a Jupyter Notebook.

RUN
```python -m ipykernel install --user --name grads --display-name "grads"```

You can check the kernel has been installed with:

```jupyter kernelspec list```

and, if something went wrong, uninstall it with:

```jupyter kernelspec uninstall py3widgets```

In the Jupyter Notebook select the kernel "grads".

## Running pytest
If you wish to run pytest, then you need to install a package (found in the 'src' directory). From the main directory:

RUN ```pip install -e .```

You only need to do this once.
Then from the main directory:

RUN ```pytest```
