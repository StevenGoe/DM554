from Util.latex import *

import numpy as np

class Tableau:
    def __init__(self, A, b, obj):
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
        self.objVal = 0
        self.n_slack_vars = int(self.n / 2)

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
        return str(self.toArray())

def simplex(tableau, doc=vdoc):

    def default_pivot_rule(cols):
        return cols[0] # Whatever, just take the first column

    iteration = 0

    # Find the initial basis / BFS (as column indices)
    basis = list(range(tableau.n_slack_vars, tableau.n))

    doc.line(r"Initial tableau:")

    doc.skip()

    doc.line(tableau.toLatex())

    doc.skip()

    doc.line(r"Initial basis: $\{ %s \}$" % (",".join([str(b) for b in basis])))

    possible_cols = [j for j in range(tableau.n) if tableau.obj[0,j] > 0]

    while len(possible_cols) > 0:
        iteration += 1

        doc.skip()
        doc.line("Iteration %d:" % iteration)

        pivot_col = default_pivot_rule(possible_cols)

        # Find most limiting row (constraint)
        pivot_row = None
        pivot_row_val = None
        for i in range(tableau.m):
            a_is = tableau.A[i,pivot_col]
            if a_is > 0:
                b_i = tableau.b[i,0]
                ratio = b_i / a_is
                print(ratio)
                if pivot_row_val is None or ratio < pivot_row_val:
                    pivot_row = i
                    pivot_row_val = ratio

        if pivot_row is None:
            raise ValueError("Something is wrong. No pivot row could be found.")

        doc.skip()
        doc.line("Row $%d$ and column $%d$ has been chosen as pivot." % (pivot_row, pivot_col))
        doc.skip()

        entering_var_index = pivot_col
        exiting_var_index  = basis[pivot_row]

        basis[pivot_row] = pivot_col

        entering_var_name = r"x_{%d}" % (entering_var_index+1)
        exiting_var_name  = r"x_{%d}" % (exiting_var_index+1)

        doc.line(r"$%s$ enters the basis. $%s$ leaves." % (entering_var_name, exiting_var_name))
        doc.line(r"New basis: $\{ %s \}$" % (",".join([str(b) for b in basis])))

        pivot = (pivot_row, pivot_col)
        pivot_val = tableau.A[pivot]

        if pivot_val == 0:
            raise ValueError("Pivot value is zero.")


        # Divide pivot row by pivot val
        tableau.A[pivot_row,:] *= (1 / pivot_val)
        tableau.b[pivot_row,0] *= (1 / pivot_val)


        # Zero out the rest of the column with row operations
        for i in range(tableau.m):
            if i == pivot_row: continue
            val = tableau.A[i,pivot_col]
            for j in range(tableau.n):
                tableau.A[i,j] += -val * tableau.A[pivot_row, j]
            tableau.b[i,0] += -val * tableau.b[pivot_row,0]

        # We must remember to also apply these operations to the obj vector
        val = tableau.obj[0,pivot_col]
        for j in range(tableau.n):
            tableau.obj[0,j] += -val * tableau.A[pivot_row, j]
        tableau.objVal += -val * tableau.b[pivot_row,0]

        doc.skip()
        doc.line("New tableau:")
        doc.skip()
        doc.line(tableau.toLatex())
        doc.skip()

        possible_cols = [j for j in range(tableau.n) if tableau.obj[0,j] > 0]

    doc.line(r"Final objective value: $%d$" % (-tableau.objVal))

    print("Final tableau:")
    print(tableau)

