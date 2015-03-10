import numpy as np
from fractions import Fraction

from latex import *

count = 0
width = 2

def gaussian_elimination(A_, delim=None, doc=vdoc):
    m, n = A_.shape
    l = min(m,n)

    global count
    count = 0

    one  = Fraction(1)
    zero = Fraction(0)

    singular = False

    def matrix_arrow():
        #nonlocal count
        #nonlocal width
        global count
        global width
        count += 1
        if count >= width:
            count %= width
            doc.line(r" \\ ")
            doc.line(r"\rightarrow &")
        else:
            doc.line(r"& \rightarrow &")


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
            doc.matrix(A_old, delim=delim, rowops=[r"\swap{%d}{%d}" % (row, i-1)])
            matrix_arrow()

        if p == zero:
            singular = True
            break

        if p != one:
            doc.matrix(A, delim=delim, rowops=[
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

            if d != zero and A_old[row, col] != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.frac(d), row, other_row))

        if len(ops) > 0:
            doc.matrix(A_old, delim=delim, rowops=ops)
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

            if d != zero and A_old[row, col] != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.frac(d), row, other_row))

        if len(ops) > 0:
            doc.matrix(A_old, delim=delim, rowops=ops)
            matrix_arrow()

    doc.matrix(A, delim=delim)

    doc.line(r"\end{align*}")

    if singular:
        doc.line(r"As we can see the matrix is singular.")

    return A

def minor_matrix(A, row, col, doc=vdoc):
    A_  = np.delete(A,  (row), axis=0)
    A__ = np.delete(A_, (col), axis=1)
    return A__


def determinant(A_, index=0, axis="row", doc=vdoc):
    m, n = A_.shape
    if m != n:
        print("Matrix is not square")
        return None

    # Convert to Fraction
    A = np.array(A_, dtype=Fraction)
    for i in range(m):
        for j in range(n):
            A[i,j] = Fraction(A[i,j])

    if n == 2:
        doc.line(r"\[")
        doc.matrix(A, typ="v")
        d = A[0,0] * A[1,1] - A[1,0] * A[0,1]
        doc.line(r"= %d \cdot %d - %d \cdot %d" % (A[0,0], A[1,1], A[1,0], A[0,1]))
        doc.line(r"= %d" % d)
        doc.line(r"\]")
        return d


    # Cofactor expansion
    if axis == "row":
        line = A[:, index]
    elif axis == "col":
        line = A[index, :]
    else:
        print("Error: Invalid axis %s" % axis)

    subdoc = doc.subdoc()

    subdoc.line(r"\[")
    subdoc.matrix(A, typ="v")
    subdoc.line(r" = ")
    
    d = Fraction(0)
    for i, a in enumerate(line):
        M = minor_matrix(A, index, i)
        dM = determinant(M)
        sign = -1 if (index + i) % 2 == 1 else 1
        d += sign * a * dM
        if sign == -1:
            sign_str = "-"
        elif i > 0:
            sign_str = "+"
        else:
            sign_str = ""
        subdoc.line(r"%s%d \cdot " % (sign_str, a))
        subdoc.matrix(M, typ="v")
    subdoc.line(r"= %d" % d)

    subdoc.line(r"\]")

    doc.from_subdoc(subdoc)

    return d
