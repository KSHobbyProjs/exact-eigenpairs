#!/usr/bin/env python3
import h5py
import numpy as np

import logging
logger = logging.getLogger(__name__)

def write_energies_to_h5(path, parameters, energies, eigenvectors=None, metadata=None):
    with h5py.File(path, "w") as f:
        # save eigenvalues and eigenvectors if requested
        f.create_dataset("parameters", data=parameters)
        f.create_dataset("energies", data=energies)
        if eigenvectors is not None:
            f.create_dataset("eigenvectors", data=eigenvectors)

        # add metadata
        metadata = metadata or {}
        for key, val in metadata.items():
            f.attrs[key] = val

def write_energies_to_dat(path, parameters, energies, metadata=None):
    with open(path, "w") as f:
        # add metadata
        metadata = metadata or {}
        for key, val in metadata.items():
            f.write(f"# {key} : {val}\n")
        np.savetxt(f, np.column_stack([parameters, energies]), fmt="%.8f", delimiter="\t")

        
