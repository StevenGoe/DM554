import numpy as np
from fractions import Fraction

from latex import *

def gaussian_elimination(A_, doc=vdoc):
    m, n = A_.shape
    l = min(m,n)

    count = 0
    width = 2

    def matrix_arrow():
        nonlocal count
        nonlocal width
        count += 1
        if count >= width:
            count %= width
            doc.line(r" \\ ")
            doc.line(r"\rightarrow &")
        else:
            doc.line(r"& \rightarrow")

    one  = Fraction(1)
    zero = Fraction(0)

    doc.line(r"\begin{align*}")
    doc.line(r"&")

    # Convert to Fraction
    A = np.array(A_, dtype=Fraction)
    for i in range(m):
        for j in range(n):
            A[i,j] = Fraction(A[i,j])


    for col in range(l):
        A_old = np.copy(A)
        row = col
        p = A[row,col]
        i = row + 1
        swapped = False
        while p == zero and i < m:
            A[[row, i],:] = A[[i, row],:] # Swap rows
            p = A[row,col]
            i += 1
            swapped = True

        if swapped:
            doc.matrix(A_old, rowops=[r"\swap{%d}{%d}" % (row, i-1)])
            matrix_arrow()

        if p == zero:
            print("Matrix has a row or column of zeroes")
            doc.line(r"\end{align*}")
            doc.line(r"As we can see the matrix has a row")
            doc.line(r"or column of zeroes, thus we cannot proceed")
            doc.line(r"with gaussian elimination")
            return None

        if p != one:
            doc.matrix(A, rowops=[
                r"\mult{%d}{\cdot %s}" % (row, doc.frac(Fraction(1,p)))
            ])
            matrix_arrow()

        # Convert pivot to 1
        A[row,:] *= Fraction(1,p) # Multiply row by scalar

        A_old = np.copy(A)
        ops = []

        # Create zeroes under the pivot
        for other_row in range(row+1, m):
            d = -Fraction(A[other_row, row])
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]

            if d != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.frac(d), row, other_row))

        if len(ops) > 0:
            doc.matrix(A_old, rowops=ops)
            matrix_arrow()



    # Back-substitution
    for col in range(l)[::-1]:
        row = col

        A_old = np.copy(A)
        ops = []

        # Create zeroes over the pivot
        for other_row in range(row):
            d = -Fraction(A[other_row, row])
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]

            if d != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.frac(d), row, other_row))

        if len(ops) > 0:
            doc.matrix(A_old, rowops=ops)
            matrix_arrow()

    doc.matrix(A, delim=1)

    doc.line(r"\end{align*}")

    return A
