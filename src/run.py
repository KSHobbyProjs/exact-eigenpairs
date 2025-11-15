#!/usr/bin/env python
from . import physics_models

def _save_eigenvalues(parameter_values, eigenvalues):
    pass

def run(model_instance, parameter_values, k_num, outfile):
    # computing exact eigenpairs
    eigenvalues, eigenvectors = model_instance.get_eigenvectors(parameter_values, k_num)

    # output to a file if desired
    if outfile is not None:
        pass

