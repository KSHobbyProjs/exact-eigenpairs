#!/usr/bin/env python3
import os, sys
import argparse
import time
import logging
logger = logging.getLogger(__name__)

import h5py
import numpy as np

from src import parse, io

def setup_logging(verbose=0):
    if verbose == 0: 
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
            level = level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )

def main():
    parser = argparse.ArgumentParser(description="Compute eigenpairs at a set of parameters L for a given model.")
    parser.add_argument("-m", "--model", type=str, default="gaussian.Gaussian1d:N=128,V0=-4.0,R=2.0", help="Model in 'module.Class:kw1=val,kw2=val' format.")
    parser.add_argument("-L", "--parameters", type=str, default="5.0,20.0:20", help="Parameter range in 'start,end:len', '1.0,2.0,3.0', or 'start,end:len,exp' format.")
    parser.add_argument("-k", "--knum", type=int, default=1, help="Number of eigenvalues to compute at each parameter value.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output filename (optional).")
    parser.add_argument("--vectors", action="store_true", help="Output eigenvectors as well as eigenvalues.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv).")

    args = parser.parse_args()   # parse CLI args
    setup_logging(args.verbose)  # setup logging
    start = time.time()          # start timer to measure elapsed time
    print(f"Model = {args.model.strip()}\tLs = {args.parameters.strip()}\tk = {str(args.knum).strip()}")

    # parse parameters + model instance
    logger.info(f"Parsing parameters = {args.parameters} and model = {args.model}.")
    Ls = parse.parse_parameter_values(args.parameters)
    model_instance = parse.parse_model_instance(args.model)
    logger.debug(f"Parsed {args.model} to {type(model_instance).__name__}\n"                      # POSSIBLY DELETE THIS AFTER STABLE
                 f"\tand {args.parameters} to " + 
                 ", ".join(f"{k}={v} ({type(v).__name__})" for k, v in vars(model_instance).items()))

    # compute eigenpairs
    logger.info("Computing eigenvalues.")
    eigenvalues, eigenvectors = model_instance.get_eigenvectors(Ls, args.knum) 

    # write eigenpair data to file if requested
    if args.output:
        logger.info(f"Writing results to {args.output}.")
        # create metadata
        metadata = {"timestamp"      : time.strftime("%A, %b %d, %Y %H:%M:%S"),
                    "model_str"      : args.model,
                    "parameters_str" : args.parameters,
                    "knum"           : args.knum,
                    "command"        : ' '.join(sys.argv)
                    }
        # if file ends in h5, use h5py format, otherwise treat everything like .dat
        if args.output.endswith(".h5"):
            io.write_energies_toh5(args.output, Ls, eigenvalues, eigenvectors if args.vectors else None, **metadata)
            logging.info("Finished writing HDF5 file.")
        else:             
            if args.vectors:
                logger.warning("You selected --vectors but chose an output file that does not support storing full eigenvectors. "
                      "Use a .h5 file if you want full eigenvector output.")
            io.write_energies_todat(args.output, Ls, eigenvalues, **metadata)
            logging.info("Finished writing text output file.")

    # print eigenpairs
    for i, L in enumerate(Ls):
        print(f"Spectrum at L = {L:.3f}")
        print(f"\t{eigenvalues[i]}")
        if args.vectors:
            for k, vec in enumerate(eigenvectors[i]):
                # print only the first 4 elements of each eigenvector
                # (prints all elements if 4 > len(vec))
                formatted_eigenvecs = [f"{v.real:.4f} + {v.imag:.4f}j" for v in vec[:4]]
                print(f"\tEigenvector {k}: {formatted_eigenvecs} ... [{len(vec)} entries total]")
    
    end = time.time()
    # print total time elapsed
    print(f"Done.\nElapsed time: {end - start:.3f} seconds.")

if __name__=="__main__":
    main()
