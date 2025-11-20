# exact-eigenpairs
A toolkit for computing exact eigenpairs of simple physical models (e.g., Gaussian potentials, Ising models) over a range of parameter values such as system size or coupling constant.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/KSHobbyProjs/exact-eigenpairs.git
cd exact-eigenpairs
pip install -r requirements.txt
```
Dependencies include `numpy`, `scipy`, `h5py`

---

## Usage
Compute eigenpairs using `get_eigenpairs.py`.  

```bash
python get_eigenpairs.py \
    --model-name gaussian.Gaussian1d:N=128,V0=-4.0,R=2.0 \
    --parameters 5.0,20.0:50 \
    --knum 5 \
    --vectors
    --out eigenpair_data.h5
```

---

## Output

The program writes results to a file specified by the user.  
- If the output filename ends with `.h5`, the program writes a full HDF5 dataset.  
- Any other file extension will produce a `.dat`-style column-format summary.

- `.h5` files — full dataset
  - `parameters` — 1D NumPy array of parameter values (`len(parameters)`).  
  - `energies` — 2D NumPy array of shape (`len(parameters)`, `knum`) containing eigenvalues.  
    (*knum* is the number of eigenpairs per parameter, as set by `--knum`). 
  - `eigenvectors` — 3D NumPy array of shape (`len(parameters)`, `knum`, `vector dimension`) containing eigenvectors.

- `.dat` files — summary dataset
  - Column 1: `parameters` — parameter values.  
  - Columns 2..(knum+1): `energies` — one column per eigenvalue.  
  - Note: `eigenvectors` are **not** included in `.dat` files, and columns separated by `\t` delimiter.

---

## Key Arguments
- `--model-name` : Model specifier in `module.ClassName:arg1=val1,arg2=val2` format.
  Example: `gaussian.Gaussian3d:N=32,V0=4.0,R=2.0`.
- `--parameters` : Parameter values in `start,end:len`, `start,end:len,exp` or `val1,val2,val3` format.
  Example: `5.0,6.0,7.0` or `5.0,20.0:150`.
- `--knum`       : Number of eigenpairs to compute at each parameter value.
- `--vectors`    : Include eigenvectors in the output.
- `--out`        : Output filename.
- `--verbose`    : Increase verbosity.

---

## Supported Models
All models are stored in `src/physics_models`.
- `Gaussian1d` - single-particle (or relative coordinate for two-particle) 1D Gaussian potential. [Gaussian1d model details](models.md#gaussian1d).
- `Gaussian3d` - single-particle (or relative coordinate for two-particle) 3D Gaussian potential. [Gaussian3d model details](models.md#gaussian3d).
- `Ising` - 1D Ising model with periodic boundary conditions. [Ising model details](models.md#ising).
- `NoninteractingSpins` - 1D series of non-interacting particles influenced by external magnetic field. [Non-interacting spins model details](models.md#non-interacting-spins).
- `NewModel` - A custom template for user-defined models.

---

## Adding a Model
Add a model by altering the class `NewModel` stored in `src/physics_models/new_model.py`.
- Implement the `construct_H(self, L)` function.
- Optionally, adjust the constructor to take in new arguments.
- Eigenvectors will be computed automatically.
Once defined, the model can be used with `--model-name new_model.NewModel:arg1=val1,arg2=val2`.
