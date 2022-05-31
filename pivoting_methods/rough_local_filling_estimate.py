import numpy as np
from typing import Callable
from functools import partial

def get_pivot_with_lowest_local_filling_estimate(matrix, k, estimation: Callable):
    min_estimation = 100000000
    row, col = k, k
    rows, cols = calculate_non_zeros(matrix, k)
    for i in range(k, matrix.n):
        for j in range(matrix.row_start[i], matrix.row_start[i+1]):
            if matrix.cols[j] >= k:
                cur_estimation = estimation(cols[matrix.cols[j]], rows[i])
                if cur_estimation < min_estimation:
                    min_estimation = cur_estimation
                    row, col = i, matrix.cols[j]

    return row, col

def calculate_non_zeros(matrix, k):
    cols = np.zeros(matrix.n)
    rows = np.zeros(matrix.n)

    for i in range(k, matrix.n):
        for j in range(matrix.row_start[i], matrix.row_start[i+1]):
            if matrix.cols[j] >= k:
                rows[i] += 1
                cols[matrix.cols[j]] += 1

    return rows, cols

#  minimizing the product of the row count and the column count
def get_estimation(n_cj, n_ri):
    return (n_cj - 1)*(n_ri - 1)

#  minimizing the sum of the row count and the column count
def get_estimation_2(n_cj, n_ri):
    return (n_cj - 1) + (n_ri - 1)

#  minimizing the product of the row count and the square of the column count
def get_estimation_3(n_cj, n_ri):
    return ((n_cj - 1)**2)*(n_ri - 1)

def without_pivoting(matrix, k):
    return k, k

# taking the non-zero in the row with minimum row count which has minimum column count
def get_pivot_from_min_row_column_count(matrix, k):
    min_row_count = 100000000000
    min_row_count_i = -1
    min_col_count_j = -1
    min_col_count = 100000000000

    for i in range(k, matrix.n):
        for j in range(matrix.row_start[i], matrix.row_start[i+1]):
            if matrix.cols[j] >= k:
                if 0 < matrix.row_start[i + 1] - j < min_row_count:
                    min_row_count = matrix.row_start[i + 1] - j
                    min_row_count_i = i
                break

    for j in range(matrix.row_start[min_row_count_i], matrix.row_start[min_row_count_i + 1]):
        if matrix.cols[j] >= k:
            cols_count = matrix.cols[matrix.row_start[k]:].count(matrix.cols[j])
            if cols_count < min_col_count:
                min_col_count = cols_count
                min_col_count_j = matrix.cols[j]

    return min_row_count_i, min_col_count_j

# taking the non-zero in the column with minimum column count which has minimum row count
def get_pivot_from_min_column_row_count(matrix, k):
    rows, cols = calculate_non_zeros(matrix, k)
    min_row_count = 100000000000
    min_row_count_i = -1
    min_col_count_j = -1
    min_col_count = 100000000000

    for j in range(k, matrix.n):
        if 0 < cols[j] < min_col_count:
            min_col_count = cols[j]
            min_col_count_j = j

    for i in range(k, matrix.n):
        for j in range(matrix.row_start[i], matrix.row_start[i+1]):
            if matrix.cols[j] == min_col_count_j:
                if rows[i] < min_row_count:
                    min_row_count = rows[i]
                    min_row_count_i = i
                break

    return min_row_count_i, min_col_count_j
