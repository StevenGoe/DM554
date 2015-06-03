#!/usr/bin/env python

from Util.latex import *
from LinAlg.matrices import *

import numpy as np
import sympy

doc = LatexDocument("document")

A = np.array([[0, 1, 2],
              [3, 4, 9],
              [5, 4, 4]])
b = np.array([[2], [5], [0]])
AI = np.concatenate((A, np.identity(min(A.shape))), axis=1)
Ab = np.concatenate((A, b), axis=1)

print(determinant(A,1, "col",doc=doc))
print(inverse_cofactor(A, doc=doc))

B = gaussian_elimination(Ab, delim=min(A.shape)-1, doc=doc)
print(A)
print(B)


doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
