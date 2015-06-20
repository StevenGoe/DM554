# DM554

Useful scripts and material for the DM554 course and in particular the exam.

The goal of this repo is to speed up parts of the exam,
either with nifty tools and functions or with implemented algorihms with automatic LaTeX code generation.

The repo consists of a couple of different part: 

- Util: General helpful things, like printing matrices
- LinAlg: Linear algebra functions
- LP: Linear and integer programming functions
- Examples: A couple of examples of usage and Gurobi modelling.

## Dependencies

The repo has the following dependencies:
- Python 3 (Python 2 will almost certainly also work)
- Python packages (see below)
- gurobipy
- pdflatex (optional, to compile generated tex file for rapid testing)

To install the Python packages from `dependencies.txt` do:

```bash
pip install -r dependencies.txt
```

## Usage

The recommended way of using this repo is to open `main.py` in IPython interactively:

```
ipython -i main.py
```

If the above starts without errors, all dependencies have been installed correctly.

All packages will be imported be default, 
for instance `numpy` as `np`, `Fraction` as `frac`,
`sympy` as `sy` and `networkx` as `nx`.
Additionally, all implemented functions will be available in global scope.

Also, a LaTeX document named `doc` is available. Some functions take
this document as an argument and will produce LaTeX code.
Remember to run `doc.compile()` (requires pdflatex) or `doc.to_file()` to output the code.
It will be placed in a folder called `document` in the root of this repo.

---

The general work flow is to load in a numpy matrix, either by writing `mat = np.array([[2,3,4...`
or by editing the file matrix.txt and running

```
mat = load_matrix()
```

It is possible to print the tableau as ascii as follows

```
print_tableau(mat)
```

which can then be inserted in LaTeX with the `verbatim` environment.


The next course of action is generally up to the user. Some use cases include:

### Simplex

The repo comes with a (buggy) implementation of the simplex algorithm.
It does no error handling, degeneracy check, cycle check nor does it have
any of the smart pivoting rules (if a certain rule is needed, 
it must be implemented in the function `default_pivot_rule` in the simplex file).
It does however output every step to LaTeX.

If a matrix `mat` have been loaded that represents a tableau (remember z column),
then it must be sliced up into its components:

```
tab = Tableau.slice(mat)
```

Next, it must be fed to the simplex function:

```
simplex(tab, doc=doc)
```
