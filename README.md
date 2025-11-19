# exact-eigenpairs
A repository for computing exact eigenpairs of physical models (e.g., Gaussian potentials, Ising model) at a series of parameters (system length, coupling constant, etc.).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/KSHobbyProjs/exact-eigenpairs.git
cd exact-eigenpairs
pip install -r requirements.txt
```
Dependencies include `numpy`, `scipy`, `matplotlib`, `jax`

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
  - `parameters` - the parameters at which the eigenpairs are calculated
  - `energies` - eigenvalues
  - `eigenvectors` - corresponding eigenvectors
- `.dat` files contain two columns:
  - `parameters` and `energies`
     (`eigenvectors` are not written to `.dat` files)
---
