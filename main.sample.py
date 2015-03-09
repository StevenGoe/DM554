#!/usr/bin/env python

import numpy as np

from latex import *
from matrices import *

doc = LatexDocument("document")

A = np.array([[1, 1],
              [3, 4]])
AI = np.concatenate((A, np.identity(min(A.shape))), axis=1)

B = gaussian_elimination(AI, doc)
print(A)
print(B)


#doc.compile() # Generate and compile a tex file in a folder
doc.to_file() # Only generate
