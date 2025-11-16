#!/usr/bin/env python3
import os, sys
import argparse
import time

import h5py

from src import run

def main():
    parser = argparse.ArgumentParser(description="Compute eigenpairs at a set of parameters L for a given model.")
    parser.add_argument("-model", "--model", type=str, default="gaussian.Gaussian1d:N=128,V0=-4.0,R=2.0", help="Model in 'module.Class:kw1=val,kw2=val' format.")
    parser.add_argument("-L", "--parameters", type=str, default="5.0,20.0:20", help="Parameter range in 'start,end:len', '1.0,2.0,3.0', or 'start,end:len,exp' format.")
    parser.add_argument("-k", "--knum", type=int, default=1, help="Number of eigenvalues to compute at each parameter value.")
    parser.add_argument("-out", "--output", type=str, default=None, help="Output filename (optional).")
    parser.add_argument("-vectors", "--vectors", action="store_true", help="Output eigenvectors as well as eigenvalues.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv).")

    args = parser.parse_args()
  
    start = time.time()

    # setup logging
    #setup_logging(args.verbose)

    # parse parameters + model instance
    Ls = run.parse_parameter_values(args.parameters)
    model_instance = run.parse_model_instance(args.model)

    # compute eigenpairs
    print(f"Model = {args.model}\tLs = {args.parameters}\tk = {args.knum}")
    print("Computing eigenvalues...")
    eigenvalues, eigenvectors = run.compute_eigenpairs(model_instance, Ls, args.knum)

    # print eigenpairs
    for i, L in enumerate(Ls):
        print(f"Spectrum at L = {L:.3f}")
        print(f"\t{eigenvalues[i]}")
        if args.vectors:
            for k, vec in enumerate(eigenvectors[i]):
                # print only the first 3 elements of each eigenvector
                # (prints all elements if 3 > len(vec))
                formatted_eigenvecs = [f"{v.real:.4f} + {v.imag:.4f}j" for v in vec[:4]]
                print(f"\tEigenvector {k}: {formatted_eigenvecs} ... [{len(vec)} entries total]")
                

    # write eigenpair data to file if requested
    if args.output:
        # if file ends in h5, use h5py format, otherwise treat everything like .dat
        if args.output.endswith(".h5"):
            with h5py.File(args.output, "w") as f:
                # save eigenvalues and eigenvectors if requested
                f.create_dataset("Ls", data=Ls)
                f.create_dataset("eigenvalues", data=eigenvalues)
                if args.vectors:
                    f.create_dataset("eigenvectors", data=eigenvectors)

                # add metadata
                f.attrs["timestamp"] = time.strftime("%A, %b %d, %Y %H:%M:%S")
                f.attrs["model"] = args.model
                f.attrs["parameters"] = args.parameters
                f.attrs["knum"] = args.knum
                f.attrs["command"] = ' '.join(sys.argv)
        else:             
            if args.vectors:
                print("Warning: you selected --vectors but chose an output file that does not support storing full eigenvectors. "
                      "Use a file ending in .h5 if you want full eigenvector output.")
            with open(args.output, "w") as f:
                f.write(f"# Timestamp: {time.strftime('%A, %b %d, %Y %H:%M:%S')}\n")
                f.write(f"# Config: model={args.model};parameters={args.parameters};knum={args.knum}\n")
                f.write(f"# Command used: {' '.join(sys.argv)}\n\n")
                np.savetxt(f, np.column_stack([Ls, eigenvalues]), fmt="%.8f", delimiter="\t")

    end = time.time()
    # print total time elapsed
    print(f"Done.\nElapsed time: {end - start:.3f} seconds")

def logger():
    pass

if __name__=="__main__":
    main()
