# DM554

Useful scripts and material for the DM554 course and in particular the exam.

## Dependencies

The repo has the following dependencies:
- Python 3
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


## TODO

Implement:

- Better way to construct tableau for homemade simplex
- Revised simplex
- Templates for LP models in Gurobi
