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
    eps = 1e-10
    return np.all(np.abs(m1 - m2) < eps)

def test(A, P, Q, LU):
    return check_equality(P.get_matrix() @ A.get_matrix() @ Q.get_matrix(), multiply_LU(LU))