from CSR.CSR import CSR
from QR_decomposition import QR_decompose
from pivoting_methods.absolute_maximum import get_abs_max_pivot
import numpy as np

class TestQRDecomposition:
    eps = 1e-10

    def test_QR_1(self):
        A = CSR([-1, 1, 4, 2, 3, 4], [1, 2, 0, 1, 0, 1], [0, 2, 4, 6], 3)
        Q, R = QR_decompose(A, get_abs_max_pivot)
        assert np.all(np.abs(A.get_matrix() - (Q.get_matrix() @ R.get_matrix())) < self.eps)