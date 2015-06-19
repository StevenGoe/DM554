from Util.latex import *

import numpy as np

def simplex(tableau, doc=vdoc):

    def default_pivot_rule(cols):
        return cols[0] # Whatever, just take the first column

    def print_basis():
        s = ""
        var_list = []
        for idx in basis:
            var_list.append(r"x_{%d}" % (idx+1))
        s = " , ".join(var_list)
        return r"\{ %s \}" % s


    if np.any(tableau.b < 0):
        print("A value in the b column is negative, i.e. we have an infeasible starting solution.")
        print("Now the dual simplex should be applied to regain feasibility.")
        print("However, this implementation does not feature the dual simplex, so it must be done manually.")
        return

    if np.any(tableau.b == 0):
        print("The tableau has degeneracies, i.e. a value in the b column is zero. Strange things might happen.")

    iteration = 0

    # Find the initial basis / BFS
    basis = []
    for i in range(tableau.n):
        if tableau.obj[0,i] == 0:
            col = tableau.A[:,i]
            one_count = 0
            zero_count = 0
            for elem in col:
                if elem == 1: one_count  += 1
                if elem == 0: zero_count += 1
            if one_count == 1 and zero_count == tableau.m-1:
                basis.append(i)

    if len(basis) != tableau.m:
        print("Basis has %d elements, but number of constraints is %d." % (len(basis), tableau.m))

    doc.line(r"Initial tableau:")

    doc.skip()

    doc.line(tableau.toLatex())

    doc.skip()

    doc.line(r"Initial basis: $%s$" % print_basis())

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
                if pivot_row_val is None or ratio < pivot_row_val:
                    pivot_row = i
                    pivot_row_val = ratio

        if pivot_row is None:
            raise ValueError("Something is wrong. No pivot row could be found.")

        doc.skip()
        doc.line("Row $%d$ and column $%d$ has been chosen as pivot." % (pivot_row+1, pivot_col+1))
        doc.skip()

        entering_var_index = pivot_col
        exiting_var_index  = basis[pivot_row]

        basis[pivot_row] = pivot_col

        entering_var_name = r"x_{%d}" % (entering_var_index+1)
        exiting_var_name  = r"x_{%d}" % (exiting_var_index+1)

        doc.line(r"$%s$ enters the basis. $%s$ leaves." % (entering_var_name, exiting_var_name))
        doc.line(r"New basis: $%s$" % print_basis())

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

    doc.skip()

    doc.line(r"Final tableau:")

    doc.skip()

    doc.line(tableau.toLatex())

    doc.skip()

    doc.line(r"Final basis:")
    doc.line(r"$%s$" % print_basis())

    doc.skip()

    return basis

