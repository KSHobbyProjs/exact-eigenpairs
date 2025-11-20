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
- `.h5` files contain three datasets:
  - `parameters` - the parameters at which the eigenpairs are calculated.
  - `energies` - eigenvalues.
  - `eigenvectors` - corresponding eigenvectors.
- `.dat` files contain two columns:
  - `parameters` and `energies`.
     (`eigenvectors` are not written to `.dat` files).

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
- `Gaussian1d` - single-particle (or relative coordinate for two-particle) 1D Gaussian potential.
- `Gaussian3d` - single-particle (or relative coordinate for two-particle) 3D Gaussian potential.
- `Ising` - 1D Ising model with periodic boundary conditions.
- `NoninteractingSpins` - 1D series of non-interacting particles influenced by external magnetic field.
- `NewModel` - A custom template for user-defined models.

---

## Adding a Model
Add a model by altering the class `NewModel` stored in `src/physics_models/new_model.py`.
- Implement the `construct_H(self, L)` function.
- Optionally, adjust the constructor to take in new arguments.
- Eigenvectors will be computed automatically.
Once defined, the model can be used with `--model-name new_model.NewModel:arg1=val1,arg2=val2`.
