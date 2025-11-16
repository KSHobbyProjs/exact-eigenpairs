#!/usr/bin/env python
import numpy as np
from . import physics_models as pm

import logging
logger = logging.getLogger(__name__)

def parse_parameter_values(Ls_string):
    """
    Parses a flexible CLI argument for parameter values.

    Parameters
    ----------
    Ls_string : str
        CLI string containing parameter info.

    Returns
    -------
    parameter_values : ndarray
        1D array of parameter values.

    Example use cases:
        '1.5'            -> np.array([1.5])
        '1.0,2.0,3.0'    -> np.array([1.0, 2.0, 3.0])
        '5.0,20.0:50'    -> np.linspace(5, 20, 50)
        '5.0,20.0:50,1.5 -> 5 + np.linspace(0, 1, 50)**1.5 * (20 - 5)
    """
    s = Ls_string.strip()

    # If colon syntax (linspace)
    if ":" in s:
        try:
            lmin_lmax, llen_lexp = s.split(":")
            lmin, lmax = lmin_lmax.split(",")
            if "," in llen_lexp:
                llen, lexp = llen_lexp.split(",")
                lexp = float(lexp)
            else:
                llen = llen_lexp
                lexp = 1.0
            lmin, lmax, llen = float(lmin), float(lmax), int(llen)
            logger.debug(f"Converting {Ls_string} to np.linspace format with start={lmin}, end={lmax}, len={llen} "
                         f"and lexp={lexp}.")
            return lmin + np.linspace(0.0, 1.0, llen)**lexp * (lmax - lmin)
        except Exception as e:
            raise ValueError(f"Invalid linspace format: {s}. Use 'start,end:len' or 'start,end:len,exp'") from e
    
    # otherwise, assume comma-separated list of numbers
    if "," in s:
        logger.debug(f"Converting {Ls_string} to np.array from comma-separated list format.")
        return np.array([float(x) for x in s.split(",")])

    # otherwise, assume a single float
    logger.debug(f"Converting {Ls_string} to np.array from float format.")
    return np.array([float(s)])

def parse_model_instance(model_string):
    """
    Parses a CLI argument for the physics model.

    Parameters
    ----------
    model_string : str
        CLI string containing model info.

    Returns
    -------
    model_instance : BaseModel
        An instance of a class that subclasses the abstract class `BaseModel`.

    Example use cases:
        'gaussian.Gaussian1d:N=128,V0=-4.0,R=2.0' -> pm.gaussian.Gaussian1d(N=128, V0=-4.0, R=2.0)
        'independent.Independent'                 -> pm.independent.Independent()
    """
    s = model_string.strip()

    if ":" in s:
        model_name, model_kwargs_str = s.split(":", 1)
        model_kwargs = _parse_kwargs(model_kwargs_str)
    else:
        model_name = s
        model_kwargs = {}

    submodule_name, class_name = model_name.split(".", 1)
    try:
        submodule = getattr(pm, submodule_name)
        ModelClass = getattr(submodule, class_name)
    except AttributeError as e:
        raise RuntimeError(f"Model {model_name} not found in `physics_models` module.") from e
    model_instance = ModelClass(**model_kwargs)
    logger.debug(f"Converted {model_string} to instance of {model_instance.__class__.__name__} with "
                 f"attributes {[(k, v, type(v)) for k, v in vars(model_instance).items()]}.")

    return model_instance

def compute_eigenpairs(model_instance, parameter_values, k_num):
    """
    A function to compute the first `k_num` eigenpairs of physics model `model_instance` at
    every value of `parameter_values`.

    Parameters
    ----------
    model_instance : BaseModel
        An instance of a class that must subclass the abstract class `BaseModel`.
    parameter_values : float or array-like
        List of parameter values at which to compute the eigenpairs.
    k_num : int
        The number of eigenpairs to take at each parameter value.

    Returns
    -------
    eigenvalues : ndarray
        Array of `k_num`-lowest eigenvalues at each L in `parameter_values`.
        Shape (len(`parameter_values`), `k_num`). Listed in ascending order.
    eigenvectors : ndarray
        Array of `k_num`-lowest eigenvectors at each L in `parameter_values`.
        Shape (len(`parameter_values`), `k_num`, n), where n is the dimension of the Hamiltonian.
        Listed in order according to eigenvalues.
        
    Note
    ----
    This just wraps the get_eigenvectors method in the abstract class BaseModel.
    """
    eigenvalues, eigenvectors = model_instance.get_eigenvectors(parameter_values, k_num)
    return eigenvalues, eigenvectors

def _parse_kwargs(kwargs_string):
    """
    Parses a comma-separated list of key=val pairs into a dictionary.

    Parameters
    ----------
    kwargs_string : str
        Comma-separated string containing kwarg info.

    Returns
    -------
    kwargs : dict
        Dictionary containing the key=val pairs in `kwargs_string`.
    
    Example
    -------
    'N=32,V0=-4.0,R=2.0' -> {"N" : 32, "V0" : -4.0, "R" : 2.0}.
    """
    
    def _convert_value(v):
        """
        Takes a string and determines if it's meant to be an int, float, bool, or str
        """
        v = v.strip().lower()
        try:
            return int(v)       # check int
        except ValueError:
            pass

        try:
            return float(v)     # check float
        except ValueError:
            pass

        if v == "true":
            return True
        elif v == "false":
            return False        
        return v                # fallback string

    s = kwargs_string.strip()
    kwargs = {}
    for kv in s.split(","):
        if not kv.strip():
            continue
        if "=" not in kv:
            raise RuntimeError(f"Invalid argument input: '{kv}'. Kwarg arguments need to be input in the form 'key1=val1,key2=val2'")
        k, v = kv.split("=", 1)   
        kwargs[k.strip()] = _convert_value(v)
    return kwargs
