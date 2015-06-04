import numpy as np

def convert_zeros_to_nan(matrix, allowed_error = 0.001):
    height, width = matrix.shape

    # Convert zeros of matrix to NaN
    for row in range(height):
        for col in range(width):
            if abs(matrix[row,col]) <= allowed_error:
                matrix[row,col] = np.nan
