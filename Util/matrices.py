import re
import numpy as np
from numpy import *
from fractions import Fraction as f
import sympy
set_printoptions(precision=3,suppress=True)

def load_matrix(filename="matrix.txt", dtype="symbolic"):
    split_by = r'\s+' # Any whitespace
    lines = [line.strip() for line in open(filename)]
    rows = len(lines)
    cols = 0
    for line in lines:
        s = re.split(split_by, line)
        if len(s) > cols:
            cols = len(s)

    if dtype == "symbolic":
        A = np.zeros((rows, cols), dtype=np.object)
    else:
        A = np.zeros((rows, cols), dtype=dtype)

    for row, line in enumerate(lines):
        s = re.split(split_by, line)
        for col, elem in enumerate(s):
            if len(elem) == 0:
                print("Empty elem at row %d, col %d" % (row,col))
                return
            if dtype == "symbolic":
                A[row,col] = sympy.S(elem)
            else:
                A[row,col] = elem
    return A


def convert_zeros_to_nan(matrix, allowed_error = 0.001):
    height, width = matrix.shape

    # Convert zeros of matrix to NaN
    for row in range(height):
        for col in range(width):
            if abs(matrix[row,col]) <= allowed_error:
                matrix[row,col] = np.nan

def printm(a):
    """Prints the array as strings
    :a: numpy array
    :returns: prints the array
    """
    def p(x):
        return str(x)
    p = vectorize(p,otypes=[str])
    print(p(a))

def tableau_to_str(a,W=7):
    """Returns a string for verbatim printing
    :a: numpy array
    :returns: a string
    """
    if len(a.shape) != 2:
        raise ValueError('verbatim displays two dimensions')
    rv = []
    rv+=[r'|'+'+'.join('{:-^{width}}'.format('',width=W) for i in range(a.shape[1]))+"+"]
    rv+=[r'|'+'|'.join(map(lambda i: '{0:>{width}}'.format("x"+str(i+1)+" ",width=W), range(a.shape[1]-2)) )+"|"+
         '{0:>{width}}'.format("-z ",width=W)+"|"
         '{0:>{width}}'.format("b ",width=W)+"|"]
    rv+=[r'|'+'+'.join('{:-^{width}}'.format('',width=W) for i in range(a.shape[1]))+"+"]
    for i in range(a.shape[0]-1):
        rv += [r'| '+' | '.join(['{0:>{width}}'.format(str(a[i,j]),width=W-2) for j in range(a.shape[1])])+" |"]
    rv+=[r'|'+'+'.join('{:-^{width}}'.format('',width=W) for i in range(a.shape[1]))+"+"]
    i = a.shape[0]-1
    rv += [r'| '+' | '.join(['{0:>{width}}'.format(str(a[i,j]),width=W-2) for j in range(a.shape[1])])+" |"]
    rv+=[r'|'+'+'.join('{:-^{width}}'.format('',width=W) for i in range(a.shape[1]))+"+"]
    s = '\n'.join(rv)
    return s

def print_tableau(a,W=7):
    print(tableau_to_str(a,W))
