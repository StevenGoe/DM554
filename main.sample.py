#!/usr/bin/env python

from Util.latex import *
#from LinAlg.matrices import *
from LP.simplex import *

import numpy as np

doc = LatexDocument("document")

A = np.array([[5, 10, 1, 0],
              [4,  4, 0, 1]])
b = np.array([60, 40])

obj = np.array([6,8,0,0])

tableau = Tableau(A,b,obj)
print(tableau.toArray())

result = simplex(tableau, doc)

print(result)

doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
