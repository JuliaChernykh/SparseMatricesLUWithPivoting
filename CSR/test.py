from CSR import CSR
from CSR import reformat_to_CSR
import pytest

class TestCSR:
    def test_transpose_1(self):
        A = CSR([1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 0, 1, 2, 0, 1, 2], [0, 3, 6, 9], 3)
        transposed = A.transpose()
        assert transposed.values == [1, 4, 7, 2, 5, 8, 3, 6, 9]
        assert transposed.cols == [0, 1, 2, 0, 1, 2, 0, 1, 2]
        assert transposed.row_start == [0, 3, 6, 9]

    def test_transpose_2(self):
        A = CSR([3, 6, 8, 9], [1, 2, 0, 2], [0, 1, 2, 4], 3)
        transposed = A.transpose()
        assert transposed.values == [8, 3, 6, 9]
        assert transposed.cols == [2, 0, 1, 2]
        assert transposed.row_start == [0, 1, 2, 4]

    def test_transpose_3(self):
        A = CSR([1, 3, -2, 9, 2], [1, 2, 0, 1, 2], [0, 2, 3, 5], 3)
        transposed = A.transpose()
        assert transposed.values == [-2, 1, 9, 3, 2]
        assert transposed.cols == [1, 0, 2, 0, 2]
        assert transposed.row_start == [0, 1, 3, 5]

    def test_transpose_4(self):
        A = CSR([1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 2, 3, 4], 4)
        transposed = A.transpose()
        assert transposed.values == [1, 2, 3, 4]
        assert transposed.cols == [0, 1, 2, 3]
        assert transposed.row_start == [0, 1, 2, 3, 4]

    def test_transpose_5(self):
        A = CSR([1, 2, 3, 4, 5, 6], [0, 2, 3, 1, 2, 1], [0, 2, 3, 5, 6], 4)
        transposed = A.transpose()
        assert transposed.values == [1, 4, 6, 2, 5, 3]
        assert transposed.cols == [0, 2, 3, 0, 2, 1]
        assert transposed.row_start == [0, 1, 3, 5, 6]

    def test_reformat_to_CSR_1(self):
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        reformatted = reformat_to_CSR(A)
        assert reformatted.values == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert reformatted.cols == [0, 1, 2, 0, 1, 2, 0, 1, 2]
        assert reformatted.row_start == [0, 3, 6, 9]

    def test_reformat_to_CSR_2(self):
        A = [[1, 0, 0], [0, 0, 6], [7, 8, 0]]
        reformatted = reformat_to_CSR(A)
        assert reformatted.values == [1, 6, 7, 8]
        assert reformatted.cols == [0, 2, 0, 1]
        assert reformatted.row_start == [0, 1, 2, 4]