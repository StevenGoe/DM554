import numpy as np
import matplotlib.pyplot as plt

from Util.matrices import *

def model_to_matrix(model):
    pass

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
