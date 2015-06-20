from Util.latex import *
from Util.matrices import *

import numpy as np

class Tableau:
    def __init__(self, A, b, obj, objVal = 0):
        # Make sure that all input is 2-dim
        if len(A.shape) == 1:
            A = np.array([A])

        if len(b.shape) == 1:
            b = np.array([b]).T

        if len(obj.shape) == 1:
            obj = np.array([obj])

        # Make sure that the A and b fit
        if A.shape[0] != b.shape[0]:
            raise ValueError("A matrix does not have same number of rows as b vector")
        self.m = A.shape[0] # Store number of contraints

        # Make sure that the A and obj fit
        if A.shape[1] != obj.shape[1]:
            raise ValueError("A matrix does not have same number of columns as obj vector")
        self.n = A.shape[1] # Store the number of variables

        self.A = A
        self.b = b
        self.obj = obj
        self.z_col = np.zeros((self.m+1,1))
        self.z_col[self.m,0] = 1
        self.objVal = objVal
        self.n_slack_vars = self.m

    def toArray(self):
        objVal_elem = np.array([[self.objVal]])
        b_extended = np.concatenate((self.b, objVal_elem), axis=0)
        arr = np.concatenate((self.A, self.obj), axis=0)
        arr = np.concatenate((arr, self.z_col), axis=1)
        arr = np.concatenate((arr, b_extended), axis=1)
        return arr

    def toLatex(self):
        arr = self.toArray()
        tab_math = r">{$}c<{$}"
        block_start = r"\begin{tabular}{| %s | %s | %s |}" % ((tab_math+" ") * self.n, tab_math, tab_math)
        block_end   = r"\end{tabular}"
        lines = []
        lines.append(r" & ".join(["x_{%d}" % i for i in range(1,self.n+1)]) + r" & -z & b \\ \hline")
        for i in range(self.m+1):
            row = arr[i,:]
            line = (r" & ".join([str(elem) for elem in row]) + r" \\")
            if i == self.m - 1:
                line += r"\hline"
            lines.append(line)
        return block_start + "\n" + "\n".join(lines) + "\n" + block_end

    def __str__(self):
        return tableau_to_str(self.toArray())

    @staticmethod
    def slice(matrix, return_tableau=False):
        rows, cols = matrix.shape

        A = matrix[:-1,:-2]
        b = matrix[:-1,-1]
        obj = matrix[-1,:-2]
        objVal = matrix[-1,-1]

        if len(A.shape) == 1:
            A = np.array([A])

        if len(b.shape) == 1:
            b = np.array([b]).T

        if len(obj.shape) == 1:
            obj = np.array([obj])

        if return_tableau:
            tableau = Tableau(A,b,obj,objVal)
            return tableau
        else:
            return (A,b,obj,objVal)
