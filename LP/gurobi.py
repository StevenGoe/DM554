import numpy as np
import matplotlib.pyplot as plt

from Util.matrices import *

def model_to_matrix(model):
    m = model.getAttr("NumConstrs")
    n = model.getAttr("NumVars")

    matrix = np.zeros((m,n))

    for i, c in enumerate(model.getConstrs()):
        for j, v in enumerate(model.getVars()):
            coef = model.getCoeff(c,v)
            matrix[i,j] = coef

    return matrix

def plot_matrix(matrix_):
    matrix = np.array(matrix_, copy=True, dtype=float)

    # Convert zeros of matrix to NaN
    # such that they will be shown as white
    convert_zeros_to_nan(matrix)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.rainbow)
    plt.colorbar()
    plt.show()
