#!/usr/bin/env python

from Util.latex import *
#from LinAlg.matrices import *
from LP.tableau import *
from LP.simplex import *

import numpy as np

doc = LatexDocument("document")

A = np.array([[5, 10, 1, 0],
              [4,  4, 0, 1]], dtype="float64")
b = np.array([60, 40], dtype="float64")

obj = np.array([6,8,0,0], dtype="float64")

tableau = Tableau(A,b,obj)

result = simplex(tableau, doc)

print(result)

doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
