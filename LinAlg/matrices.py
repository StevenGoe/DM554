import numpy as np
from fractions import Fraction
import sympy

from Util.latex import *

count = 0
width = 2

def convert_matrix_decimal(A_):
    m, n = A_.shape

    # Convert to Fraction
    A = np.array(A_, dtype=Fraction)
    for i in range(m):
        for j in range(n):
            A[i,j] = sympy.S(A[i,j])
            #if not isinstance(A[i,j], sympy.Symbol):
            #    A[i,j] = Fraction(A[i,j])

    return A

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
    A = convert_matrix_decimal(A_)


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
                r"\mult{%d}{\cdot %s}" % (row, doc.mathExp(1 / p))
            ])
            matrix_arrow()

        # Convert pivot to 1
        A[row,:] *= 1 / p # Multiply row by scalar

        A_old = np.copy(A)
        ops = []

        # Create zeroes under the pivot
        for other_row in range(row+1, m):
            d = -A[other_row, row]
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]

            if d != zero and A_old[row, col] != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.mathExp(d), row, other_row))

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
            d = -A[other_row, row]
            for j in range(n): # Add row to another row
                A[other_row,j] += d * A[row, j]

            if d != zero and A_old[row, col] != zero:
                ops.append(r"\add[%s]{%d}{%d}" % (doc.mathExp(d), row, other_row))

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
    A = convert_matrix_decimal(A_)

    if n == 2:
        doc.line(r"\[")
        doc.matrix(A, typ="v")
        d = A[0,0] * A[1,1] - A[1,0] * A[0,1]
        doc.line(r"= %s \cdot %s - %s \cdot %s" % (
            doc.mathExp(A[0,0]), doc.mathExp(A[1,1]),
            doc.mathExp(A[1,0]), doc.mathExp(A[0,1]))
        )
        doc.line(r"= %s" % doc.mathExp(d))
        doc.line(r"\]")
        return d


    # Cofactor expansion
    if axis == "row":
        line = A[index, :]
    elif axis == "col":
        line = A[:, index]
    else:
        print("Error: Invalid axis %s" % axis)
        return

    subdoc = doc.subdoc()

    subdoc.line(r"\[")
    subdoc.matrix(A, typ="v")
    subdoc.line(r" = ")
    
    d = Fraction(0)
    for i, a in enumerate(line):
        if axis == "row":
            M = minor_matrix(A, index, i)
        elif axis == "col":
            M = minor_matrix(A, i, index)
        dM = determinant(M)
        sign = -1 if (index + i) % 2 == 1 else 1
        d += sign * a * dM
        if sign == -1:
            sign_str = "-"
        elif i > 0:
            sign_str = "+"
        else:
            sign_str = ""
        subdoc.line(r"%s%s \cdot " % (sign_str, doc.mathExp(a)))
        subdoc.matrix(M, typ="v")
    subdoc.line(r"= %s" % doc.mathExp(d))

    subdoc.line(r"\]")

    doc.from_subdoc(subdoc)

    return d

def cofactors(A_, doc=vdoc):
    m, n = A_.shape
    A = convert_matrix_decimal(A_)
    C = convert_matrix_decimal(np.zeros((m,n)))
    doc.line(r"\begin{align*}")
    for i in range(m):
        for j in range(n):
            M = minor_matrix(A, i, j)
            d = determinant(M)
            C[i,j] = d
            doc.line(r"C_{%d%d} &= " % (i+1,j+1))
            doc.matrix(M, typ="v")
            doc.line(r" = %s &" % doc.mathExp(d))
        doc.line(r" \\ ")
    doc.line(r"\end{align*}")

    doc.line(r"\[")
    doc.line(r"C = ")
    doc.matrix(C)
    doc.line(r"\]")

    return C

def adjoint(A, doc=vdoc):
    C = cofactors(A, doc=doc)
    CT = C.T
    doc.line(r"\[")
    doc.line(r"\adj(A) = ")
    doc.matrix(CT)
    doc.line(r"\]")
    return CT

def inverse_cofactor(A, doc=vdoc):
    d = determinant(A, doc=doc)

    if d == Fraction(0):
        print("Determinant is zero. Inverse does not exist.")
        return None

    Adj = adjoint(A, doc=doc)
    Inv = np.copy(Adj)
    Inv[:,:] *= 1 / d

    doc.line(r"\[")
    doc.line(r"A^{-1} = \frac{1}{|A|} \adj(A) = ")
    doc.line(r"%s \cdot " % doc.mathExp(1 / d))
    doc.matrix(Adj)
    doc.line(r" = ")
    doc.matrix(Inv)
    doc.line(r"\]")

    return Inv

# === Row operations ===

def mult_row(A,row,num):
    A[row,:] *= num
    return A

def swap_rows(A,row1,row2):
    A[[row1, row2],:] = A[[row2, row1],:]
    return A

def add_row_to_row(A, row1, c, row2):
    m,n = A.shape
    for j in range(n):
        A[row2,j] += c * A[row1, j]
    return A

def one_at_pivot(A,row,col, use_fraction=True):
    pivot = A[row,col]
    if use_fraction:
        mult_row(A,row, sympy.S(1) / pivot)
    else:
        mult_row(A,row, 1.0 / pivot)
    return A

def zero_around_row(A,row,col, use_fraction=True):
    m,n = A.shape
    pivot = A[row,col]
    for i in range(m):
        if i != row:
            d = A[i,col]
            add_row_to_row(A,row, -(d / pivot), i)
    return A

def one_zero_col(A,row,col, use_fraction=True):
    pivot = A[row,col]
    one_at_pivot(A,row,col, use_fraction)
    zero_around_row(A, row, col, use_fraction)
    return A

def subset_rows(A,row_list):
    return A[row_list,:]

def subset_cols(A,col_list):
    return A[:,col_list]
