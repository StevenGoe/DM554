#!/usr/bin/env python

import numpy as np

from latex import *
from matrices import *

doc = LatexDocument("document")

A = np.array([[3, 5, 8],
              [9,-2, 1]])
B = gaussian_elimination(A, doc)
print(A)
print(B)


#doc.compile() # Generate and compile a tex file in a folder
doc.to_file() # Only generate
