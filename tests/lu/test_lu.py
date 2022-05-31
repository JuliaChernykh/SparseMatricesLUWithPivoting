import pytest
import numpy as np
from CSR import CSR
from LU_decomposition import LU_decompose
from read_matrix_collection import read_data
from main import LU_PIVOTING_METHODS


number_of_tests = len(read_data())


@pytest.fixture(scope='session')
def matrices():
    all_matricies = [CSR(*matrix) for matrix in read_data()]
    return [matrix for matrix in all_matricies if matrix.n == 48]


@pytest.fixture(scope='session')
def matrix(request, matrices):
    return matrices[request.param]


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


@pytest.mark.parametrize('matrix', list(range(1)), indirect=True)
@pytest.mark.parametrize('pivoting_method', [method for method_name, method in LU_PIVOTING_METHODS])
def test_lu(matrix, pivoting_method):

    LU, P, Q = LU_decompose(matrix, pivoting_method)
    assert check_equality(P.get_matrix() @ matrix.get_matrix() @ Q.get_matrix(), multiply_LU(LU))
