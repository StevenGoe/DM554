#!/usr/bin/env python

# Recommended: Open this in IPython interactively
#   ipython -i main.py
# Alternatively, write program here and run
#   python main.py

from Util.latex import *
from Util.matrices import *
from LinAlg.matrices import *
from LP.gurobi import *
from LP.simplex import *
from LP.tableau import *
from LP.netflows import *
from LP.revisedsimplex import *

import numpy as np
from fractions import Fraction as frac
from sympy import *

doc = LatexDocument("document")



#doc.compile() # Generate and compile a tex file in a folder
#doc.to_file() # Only generate
