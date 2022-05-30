def get_abs_max_pivot(matrix, k):
    pivot = 0
    for i in range(k, matrix.n):
        for j in range(matrix.row_start[i], matrix.row_start[i + 1]):
            if matrix.cols[j] >= k and abs(matrix.values[j]) > pivot:
                pivot = abs(matrix.values[j])
                row, col = i, matrix.cols[j]
    return row, col