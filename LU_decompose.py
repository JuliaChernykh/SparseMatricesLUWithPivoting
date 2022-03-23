from CSR import CSR

def LU_decompose(matrix, get_pivot_position):
    P = CSR([1] * matrix.n, list(range(matrix.n)), list(range(matrix.n + 1)), matrix.n)  # rows permutations
    Q = CSR([1] * matrix.n, list(range(matrix.n)), list(range(matrix.n + 1)), matrix.n)  # cols permutations
    LU = matrix.make_copy()
    for i in range(LU.n - 1):
        # pivoting
        pivot_row, pivot_col = get_pivot_position(LU, i)
        makeTransposition(LU, P, Q, pivot_row, pivot_col, i)

        # gauss elimination
        for j in range(i + 1, LU.n):
            coef = LU.get_element(j, i) / LU.get_element(i, i)
            LU.set_value(coef, j, i)
            for k in range(i + 1, LU.n):
                new_value = LU.get_element(j, k) - coef * LU.get_element(i, k)
                LU.set_value(new_value, j, k)
    return LU, P, Q

def makeTransposition(LU, P, Q, pivot_row, pivot_col, k):
    if k != pivot_row:
        LU.swap_rows(k, pivot_row)
        P.swap_rows(k, pivot_row)
    if k != pivot_col:
        LU.swap_cols(k, pivot_col)
        Q.swap_cols(k, pivot_col)