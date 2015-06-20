import numpy as np
from Util.latex import *
from Util.matrices import *
from LinAlg.matrices import *
from LP.tableau import *

def revised_simplex_to_basis(tableau, basis):
    if isinstance(tableau, Tableau):
        A,b,obj,objVal = tableau.A,tableau.b,tableau.obj,tableau.objVal
    else:
        A,b,obj,objVal = Tableau.slice(tableau)

    A_B, A_N = partition_basic_non_basic(A,basis)
    c_B, c_N = partition_basic_non_basic(obj,basis)

    print("A_B and A_N:")
    print(A_B)
    print(A_N)

    print("c_B and c_N:")
    print(c_B)
    print(c_N)

    A_B_inv = np.linalg.inv(A_B)

    print("A_B inverse:")
    print(A_B_inv)

    y = c_B.dot(A_B_inv)

    print("y (c_B * A_B_inv):")
    print(y)

    c_N_bar = c_N - y.dot(A_N) # Should actually be y.T

    print("c_N_bar (c_N - y.T * A_N) (reduced cost):")
    print(c_N_bar)

    if np.any(c_N_bar >= 0):
        print("Since all reduced costs are non-negative, the solution is optimal.")

    x_B = A_B_inv.dot(b)

    print("x_B:")
    print(x_B)


def partition_basic_non_basic(A, basis):
    m,n = A.shape
    non_basis = []
    for i in range(n):
        if i not in basis:
            non_basis.append(i)

    return (A[:,basis], A[:,non_basis])
