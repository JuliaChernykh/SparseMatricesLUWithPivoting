import pytest
import numpy as np
from CSR import CSR
from QR_decomposition import QR_decompose
from read_matrix_collection import read_data
from main import QR_PIVOTING_METHODS


number_of_tests = len(read_data())


@pytest.fixture(scope='session')
def matrices():
    all_matricies = [CSR(*matrix) for matrix in read_data()]
    return [matrix for matrix in all_matricies if matrix.n == 494]


@pytest.fixture(scope='session')
def matrix(request, matrices):
    return matrices[request.param]

def check_equality(m1, m2):
    eps = 1e-7
    return np.all(np.abs(m1 - m2) < eps)

@pytest.mark.parametrize('matrix', list(range(1)), indirect=True)
@pytest.mark.parametrize('pivoting_method', [method for method_name, method in QR_PIVOTING_METHODS])
def test_lu(matrix, pivoting_method):

    Q, R, P, C = QR_decompose(matrix, pivoting_method)
    assert check_equality(P.get_matrix() @ matrix.get_matrix() @ C.get_matrix(), Q.get_matrix() @ R.get_matrix())
