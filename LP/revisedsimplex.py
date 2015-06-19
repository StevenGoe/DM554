from Util.latex import *
from Util.matrices import *
from LinAlg.matrices import *
from LP.tableau import *


def partition_basic_non_basic(A, basis):
    m,n = A.shape
    non_basis = []
    for i in range(n):
        if i not in basis:
            non_basis.append(i)

    return (A[:,basis], A[:,non_basis])
