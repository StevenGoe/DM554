#!/usr/bin/env python

import numpy as np

from latex import *
from matrices import *

doc = LatexDocument("document")

A = np.array([[0, 1, 2],
              [3, 4, 9],
              [3, 4, 9]])
b = np.array([[2], [5], [0]])
AI = np.concatenate((A, np.identity(min(A.shape))), axis=1)
Ab = np.concatenate((A, b), axis=1)


B = gaussian_elimination(Ab, delim=min(A.shape)-1, doc=doc)
print(A)
print(B)


doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
