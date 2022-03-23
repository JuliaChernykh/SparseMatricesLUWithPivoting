import numpy as np

def calculate_local_filling(matrix, k):
    B = matrix.get_boolean_matrix()[k:, k:]
    invertedTransposedB = ((B == 0).astype(dtype=int)).transpose()
    return B @ invertedTransposedB @ B

def get_pivot_with_lowest_local_filling(matrix, k):
    localFillingMatrix = calculate_local_filling(matrix, k)
    ind = np.unravel_index(np.argmin(localFillingMatrix, axis=None), localFillingMatrix.shape)
    while matrix.get_element(ind[0] + k, ind[1] + k) == 0:
        localFillingMatrix[ind[0]][ind[1]] = np.argmax(localFillingMatrix, axis=None) + 1000
        ind = np.unravel_index(np.argmin(localFillingMatrix, axis=None), localFillingMatrix.shape)
    return ind[0] + k, ind[1] + k