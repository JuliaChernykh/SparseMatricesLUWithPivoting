from CSR.CSR import CSR
from math import hypot
import numpy as np
from tqdm import tqdm
from functools import partial

# QR разложение реализовано с помощью поворота Гивенса
def QR_decompose(A, get_pivot_position):
    size = A.n
    P = CSR([1] * size, list(range(size)), list(range(size + 1)), size)  # rows permutations
    CC = CSR([1] * size, list(range(size)), list(range(size + 1)), size)  # cols permutations

    # Initialize orthogonal matrix Q and upper triangular matrix R
    Q = CSR([1] * size, list(range(size)), list(range(size + 1)), size)
    R = A.copy()

    # Iterate over lower triangular matrix
    rows, cols = np.tril_indices(size, -1, size)
    for row in tqdm(range(size)):
        # for row, col in tqdm(list(zip(rows, cols))):
        # pivoting
        # pivot_row, pivot_col = get_pivot_position(R, col)
        pivot_row, pivot_col = get_pivot_position(R, row)
        make_transposition(Q, R, P, CC, pivot_row, pivot_col, row)
        for col in range(0, row):
            # Compute Givens rotation matrix and zero-out lower triangular matrix entries.
            if R.get_element(row, col) != 0:
                print('hello')
                (c, s) = get_givens_rotation_matrix_entries(R.get_element(col, col), R.get_element(row, col))

                G = CSR([1] * size, list(range(size)), list(range(size + 1)), size)
                G.set_value(c, col, col)
                G.set_value(c, row, row)
                G.set_value(s, row, col)
                G.set_value(-s, col, row)

                R = G.multiply_by(R)
                Q = Q.multiply_by(G.transpose())

    return Q, R, P, CC

def make_transposition(Q, R, P, C, pivot_row, pivot_col, k):
    # при перестановке в R строк переставляем строки и столбцы в Q
    # при перестановке в R столбцов ничего не меняем
    if k != pivot_row:
        Q.swap_rows(k, pivot_row)
        Q.swap_cols(k, pivot_row)
        R.swap_rows(k, pivot_row)
        P.swap_rows(k, pivot_row)
    if k != pivot_col:
        R.swap_cols(k, pivot_col)
        C.swap_cols(k, pivot_col)

def get_givens_rotation_matrix_entries(a, b):
    r = hypot(a, b)
    c = a / r
    s = -b / r
    return c, s
