import numpy as np
import matplotlib.pyplot as plt
import random

from Util.matrices import *
from Util.latex import *

def model_to_matrix(model):
    m = model.getAttr("NumConstrs")
    n = model.getAttr("NumVars")

    matrix = np.zeros((m,n))

    for i, c in enumerate(model.getConstrs()):
        for j, v in enumerate(model.getVars()):
            coef = model.getCoeff(c,v)
            matrix[i,j] = coef

    return matrix

def plot_matrix(matrix_, doc=vdoc):
    matrix = np.array(matrix_, copy=True, dtype=float)

    # Convert zeros of matrix to NaN
    # such that they will be shown as white
    convert_zeros_to_nan(matrix)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.rainbow)
    plt.colorbar()
    if doc is vdoc:
        plt.show()
    else:
        filename = "matrix-plot-%d" % (random.randint(0,999999))
        ext = ".png"
        path = "%s/%s%s" % (doc.filename, filename, ext)
        plt.savefig(path, bbox_inches="tight")

        caption = "Plot of matrix"

        doc.line(r"\begin{figure}[h]")
        doc.line(r"\centering")
        doc.line(r"\includegraphics[width=\linewidth]{%s%s}" % (filename, ext))
        doc.line(r"\label{fig:%s}" % filename)
        doc.line(r"\caption{%s}" % caption)
        doc.line(r"\end{figure}")
