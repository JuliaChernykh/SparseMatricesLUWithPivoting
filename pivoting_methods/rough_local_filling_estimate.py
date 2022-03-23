def get_pivot_with_lowest_local_filling_estimate(matrix, k):
    min_estimation = 100000000
    for i in range(k, matrix.n):
        for j in range(k, matrix.n):
            cur_estimation = get_estimation(matrix, i, j)
            if cur_estimation < min_estimation and matrix.get_element(i, j) != 0:
                min_estimation = cur_estimation
                row, col = i, j
    return row, col

def get_pivot_with_lowest_local_filling_estimate_2(matrix, k):
    min_estimation = 100000000
    for i in range(k, matrix.n):
        for j in range(k, matrix.n):
            cur_estimation = get_estimation_2(matrix, i, j)
            if cur_estimation < min_estimation and matrix.get_element(i, j) != 0:
                min_estimation = cur_estimation
                row, col = i, j
    return row, col

def get_estimation(matrix, row, col):
    n_cj = get_n_cj(matrix, col)
    n_ri = get_n_ri(matrix, row)
    return (n_cj - 1)*(n_ri - 1)

def get_estimation_2(matrix, row, col):
    n_cj = get_n_cj(matrix, col)
    n_ri = get_n_ri(matrix, row)
    return (n_cj - 1) + (n_ri - 1)

def get_n_cj(matrix, col):
    count = 0
    for i in range(len(matrix.cols)):
        if matrix.cols[i] == col and matrix.values[i] != 0:
            count += 1
    return count

def get_n_ri(matrix, row):
    return len(list(filter(lambda x: x != 0, matrix.values[matrix.row_start[row]:matrix.row_start[row + 1]])))