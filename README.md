# DM554

Useful scripts and material for the DM554 course and in particular the exam.

The goal of this repo is to speed up parts of the exam,
either with nifty tools and functions or with implemented algorithms with automatic LaTeX code generation.

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

If the matrix represents a tableau, it is possible to print the tableau as ascii as follows

```
print_tableau(mat)
```

which can then be inserted in LaTeX with the `verbatim` environment.

It is also possible to output as LaTeX as follows:

```
tab = Tableau.slice(mat, True)
print(tab.toLatex())
```

Here we use a slicer that slices the matrix into the individual parts of the tableau
and creates a `Tableau` object to tie it all together.

It is also possible to get the individual parts by

```
A,b,obj,objVal = Tableau.slice(mat)
```



The next course of action is generally up to the user. Some use cases include:

### Simplex

The repo comes with a (buggy) implementation of the simplex algorithm.
It does no error handling, degeneracy check, cycle check nor does it have
any of the smart pivoting rules (if a certain rule is needed, 
it must be implemented in the function `default_pivot_rule` in the simplex file).
There is also no implementation of the dual simplex, thus if the tableau
has an infeasible start, the function will say so and terminate.
It does however output every step to LaTeX.

If a matrix `mat` have been loaded that represents a tableau (remember z column),
then it must be sliced up into its components:

```
tab = Tableau.slice(mat, True)
```

Next, it must be fed to the simplex function:

```
simplex(tab, doc=doc)
```

### Revised simplex

A part of the revised simplex has been implemented. 
It will take a tableau and a new basis and transition the tableau over to that basis.
It writes the result to the screen and does not output LaTeX code.

```
revised_simplex(mat, [a,b,c,...])
```

where a,b,c is the (zero-indexed) indices of the columns corresponding to the variables
(e.g. the corresponding column of x3 is the third one, meaning that its index is 2).

### Row operations

If one wants to do row operations (for instance to do the simplex step by step or do the dual simplex)
it is possible to do so as follows:

```
swap_rows(mat, 0, 2)
```

Swaps the first and third row of a matrix.

```
mult_row(mat, 1, 5)
```

Multiplies the second row by 5.

```
add_row_to_row(mat, 0, 8, 1)
```

Adds the first row multiplied by 8 to the second row.

There are also a couple of high-level operations, for instance

```
one_at_pivot(mat, 0, 0)
```

will take the elem of the first row and first column as pivot and divide the first row by this
to obtain a 1 in that position.

```
zero_around_row(mat, 1, 1)
```

Will take a pivot as before and add the row of the pivot to the rows above and below to obtain
zeros above and below it.

```
one_zero_col(mat, 0, 1)
```

Will combine the previous two operations to get a 1 at the pivot and zeroes above and below.


### Gurobi modeling

As few handy functions have been added to allow for fast prototyping of Gurobi models.

For instance, given a model `m` a pool of variables of a given type can be created as follows:

```
x = gen_vars(m, 5, vtype=GRB.BINARY)
```

`x` will then be a dictionary of variables indexed as `x[3]` to get the third variables (one-indexed for once).
It is also possible to get a two dimensional dict by `x = gen_vars(m, 5, 3)` indexed as `x[1,2]`.

Once a model has been optimized, it is possible to display the value of the variables 
(handy in case of branch and bounds questions) as follows:

```
show_model_solution(m, x)
```

or simply

```
show_model_solution(m)
```

to show all vars.

Lastly, there is a function `one_to(n)` which gives a list of 1 to n.


### Network flows

Define a graph as follows:

```
G = nx.DiGraph()
G.add_node('s', demand=-5)
G.add_edge('s','a', capacity=3.0)
G.add_edge('s','b', capacity=1.0)
...
G.add_edge('e','t', capacity=3.0)
```

`demand` is the balance on a given node, and `capacity` is, well, the max capacity on the edge.

Note: If a node has 0 balance, it is not required to add the node first using `add_node` (see above).

It is possible to draw the graph using

```
draw_graph(G)
```

It will save a file called `plot-netflows.png` by default, but might also display the graph
if you have used `%matplotlib inline` in IPython.

Max flow can for instance be solved using

```
flow_value, flow_dict = nx.maximum_flow(G, 's', 't')

print("Max flow value: %g" % flow_value)
print("Max flow solution: %s" % str(flow_dict))
```

See LP/netflows.py for more functions and examples.

Also once a `flow_dict` has been acquired, it is possible
to also draw this to the graph using

```
draw_graph(G, flow_dict)
```

## Functions

Here is a list of all functions

```
LinAlg/matrices.py:     gaussian_elimination(A_, delim=None, doc=vdoc)
LinAlg/matrices.py:     minor_matrix(A, row, col, doc=vdoc)
LinAlg/matrices.py:     determinant(A_, index=0, axis="row", doc=vdoc)
LinAlg/matrices.py:     cofactors(A_, doc=vdoc)
LinAlg/matrices.py:     adjoint(A, doc=vdoc)
LinAlg/matrices.py:     inverse_cofactor(A, doc=vdoc)
LinAlg/matrices.py:     mult_row(A,row,num)
LinAlg/matrices.py:     swap_rows(A,row1,row2)
LinAlg/matrices.py:     add_row_to_row(A, row1, c, row2)
LinAlg/matrices.py:     one_at_pivot(A,row,col, use_fraction=True)
LinAlg/matrices.py:     zero_around_row(A,row,col, use_fraction=True)
LinAlg/matrices.py:     one_zero_col(A,row,col, use_fraction=True)
LinAlg/matrices.py:     subset_rows(A,row_list)
LinAlg/matrices.py:     subset_cols(A,col_list)
LP/gurobi.py:           one_to_(n): return range(n
LP/gurobi.py:           gen_vars(model, n1, n2=None, letter="x", vtype=GRB.CONTINUOUS)
LP/gurobi.py:           show_model_solution(model, var_dict=None)
LP/gurobi.py:           model_to_matrix(model)
LP/gurobi.py:           plot_matrix(matrix_, doc=vdoc)
LP/revisedsimplex.py:   revised_simplex_to_basis(tableau, basis)
LP/revisedsimplex.py:   partition_basic_non_basic(A, basis)
LP/netflows.py:         draw_graph(G, flow_dict={})
LP/simplex.py:          simplex(tableau, doc=vdoc)
LP/tableau.py:          slice(matrix, return_tableau=False)
Util/matrices.py:       load_matrix(filename="matrix.txt", dtype="symbolic")
Util/matrices.py:       printm(a)
Util/matrices.py:       tableau_to_str(a,W=7)
Util/matrices.py:       print_tableau(a,W=7)
```
