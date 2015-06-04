#!/usr/bin/env python3

from Util.latex import *
from LP.gurobi import *

import numpy as np

doc = LatexDocument("document")


# Your script and calculations here


A = np.array([[5, 10, 1, 0],
              [4,  4, 0, 1]])

plot_matrix(A)

doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
