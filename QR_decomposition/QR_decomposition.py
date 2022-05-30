from CSR.CSR import CSR
from math import copysign, hypot
import numpy as np
from pivoting_methods.rough_local_filling_estimate import (
    without_pivoting,
    get_pivot_with_lowest_local_filling_estimate,
    get_estimation,
    get_estimation_2,
)
from tqdm import tqdm
from functools import partial

# QR разложение реализовано с помощью поворота Гивенса
def QR_decompose(A):
    size = A.n
    # P = CSR([1] * size, list(range(size)), list(range(size + 1)), size)  # rows permutations
    # CC = CSR([1] * size, list(range(size)), list(range(size + 1)), size)  # cols permutations

    # Initialize orthogonal matrix Q and upper triangular matrix R
    Q = CSR([1] * size, list(range(size)), list(range(size + 1)), size)
    R = A.copy()

    # Iterate over lower triangular matrix
    (rows, cols) = np.tril_indices(size, -1, size)
    for (row, col) in tqdm(list(zip(rows, cols))):
        # pivoting
        # pivot_row, pivot_col = get_pivot_position(R, col)
        # make_transposition(Q, R, pivot_row, pivot_col, col)

        # Compute Givens rotation matrix and zero-out lower triangular matrix entries.
        if R.get_element(row, col) != 0:
            (c, s) = get_givens_rotation_matrix_entries(R.get_element(col, col), R.get_element(row, col))

            G = CSR([1] * A.n, list(range(A.n)), list(range(A.n + 1)), A.n)
            G.set_value(c, col, col)
            G.set_value(c, row, row)
            G.set_value(s, row, col)
            G.set_value(-s, col, row)

            R = G.multiply_by(R)
            Q = Q.multiply_by(G.transpose())

    # print('A', A.get_matrix())
    # print('PAC', P.get_matrix() @ A.get_matrix() @ CC.get_matrix())
    # print('QR', Q.get_matrix() @ R.get_matrix())
    # print(check_equality(P.get_matrix() @ A.get_matrix() @ CC.get_matrix(), Q.get_matrix() @ R.get_matrix()))
    return Q, R

def check_equality(m1, m2):
    eps = 1e-10
    return np.all(np.abs(m1 - m2) < eps)

def make_transposition(Q, R, pivot_row, pivot_col, k):
    # при перестановке в R строк переставляем строки и столбцы в Q
    # при перестановке в R столбцов ничего не меняем
    if k != pivot_row:
        Q.swap_rows(k, pivot_row)
        Q.swap_cols(k, pivot_row)
        R.swap_rows(k, pivot_row)
        # P.swap_rows(k, pivot_row)
    if k != pivot_col:
        R.swap_cols(k, pivot_col)
        # C.swap_cols(k, pivot_col)

def get_givens_rotation_matrix_entries(a, b):
    r = hypot(a, b)
    c = a / r
    s = -b / r
    return (c, s)


# A = CSR([-1, 1, 4, 2, 3, 4], [1, 2, 0, 1, 0, 1], [0, 2, 4, 6], 3)
# Q, R = QR_decompose(A, partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_2))