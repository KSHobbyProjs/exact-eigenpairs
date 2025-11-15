#!usr/bin/env python3
import os, sys
import argparse

from src import utils
from src import run

def main():
    parser = argparse.ArgumentParser(description="Compute eigenpairs at a set of parameters L for a given model with Hamiltonian H(L)")
    parser.add_argument("-model", "--model", type=str, default="gaussian.Gaussian1d:V0=-4.0,R=2.0", help="The name of the physical model in 'module.class:modelkwargs' format. E.g., 'gaussian.Gaussian1d:V0=-4.0,R=2.0'")
    parser.add_argument("-L", "--parameters", type=str, default="5.0,20.0:20", help="The set of parameter values to compute exact eigenpairs at. E.g., 5.0,20.0:20")
    parser.add_argument("-k", "--knum", type=int, default=1, help="The number of eigenvalues to compute at each parameter value.")
    parser.add_argument("-out", "--out", type=str, default=None, help="The file, if any, to output the eigenpairs to.")
    parser.add_argument("-vectors", "--vectors", action="store_true", help="Output eigenvectors as well as eigenvalues.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv for more).")
    args = parse_args()
    setup_logging(args.verbose)


def logger():
    pass

if __name__=="__main__":
    main()
