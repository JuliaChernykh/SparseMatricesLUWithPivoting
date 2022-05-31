import numpy as np

def multiply_LU(LU):
    LU_full_matrix = LU.get_matrix()
    L = LU_full_matrix.copy()
    U = LU_full_matrix.copy()
    for i in range(len(L)):
        L[i][i] = 1
        for j in range(i + 1, len(L[i])):
            L[i][j] = 0
        for j in range(i):
            U[i][j] = 0
    return L @ U

def check_equality(m1, m2):
    eps = 1e-7
    return np.all(np.abs(m1 - m2) < eps)

def test(A, P, Q, LU):
    init_m = P.get_matrix() @ A.get_matrix() @ Q.get_matrix()
    lu_m = multiply_LU(LU)
    print(np.nonzero(np.abs(P.get_matrix() @ A.get_matrix() @ Q.get_matrix() - multiply_LU(LU)) > 1e-7))
    # print(init_m[10, 0], lu_m[10, 0])
    # print(init_m[19, 9], lu_m[19, 9])
    # print(init_m[23, 13], lu_m[23, 13])
    return check_equality(init_m, lu_m)