import numpy as np
from fractions import Fraction

from latex import *

def gaussian_elimination(A_, doc=vdoc):
    m, n = A_.shape
    l = min(m,n)

    zero = Fraction(0)

    doc.line(r"\[")

    # Convert to Fraction
    A = np.array(A_, dtype=Fraction)
    for i in range(m):
        for j in range(n):
            A[i,j] = Fraction(A[i,j])


    for col in range(l):
        row = col
        p = A[row,col]
        i = row + 1
        while p == zero and i < m:
            A[[row, i],:] = A[[i, row],:] # Swap rows
            p = A[row,col]
            i += 1

        if p == zero:
            print("Matrix has a row or column of zeroes")
            doc.line(r"\]")
            return None

        doc.matrix(A, rowops=[r"\mult{%d}{%s}" % (row, str(p))])

        # Convert pivot to 1
        A[row,:] *= Fraction(1,p) # Multiply row by scalar

        # Create zeroes under the pivot
        for other_row in range(row+1, m):
            d = -Fraction(A[other_row, row])
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]


    # Back-substitution
    for col in range(l)[::-1]:
        row = col

        # Create zeroes over the pivot
        for other_row in range(row):
            d = -Fraction(A[other_row, row])
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]

    doc.matrix(A, delim=1)

    doc.line(r"\]")

    return A
