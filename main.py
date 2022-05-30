from CSR.CSR import CSR, Vector
from LU_decomposition.LU_decomposition import LU_decompose
from LU_decomposition.tests import test
from read_matrix_collection import read_data
from tabulate import tabulate
from time import process_time
from functools import partial
from pivoting_methods.exact_local_filling_estimate import get_pivot_with_lowest_local_filling
from pivoting_methods.rough_local_filling_estimate import (
    get_pivot_with_lowest_local_filling_estimate,
    get_estimation,
    get_estimation_2,
    get_estimation_3,
    get_pivot_from_min_column_row_count,
    get_pivot_from_min_row_column_count,
    without_pivoting,
)
from pivoting_methods.absolute_maximum import get_abs_max_pivot
from QR_decomposition.QR_decomposition import QR_decompose

def output(table):
    with open("output.txt", "w") as f:
        f.write(table)


def main():
    collection = read_data()
    for i in range(len(collection)):
        collection[i] = CSR(*collection[i])

    table = [['Size', 'Pivoting method', 'Filling before decomposition', 'Filling after decomposition', 'Filling increase', 'Time']]
    LU_pivoting_methods_names = [
        # 'absolute maximum',
        # 'exact estimation',
        # 'minimizing row count * column count',
        # 'minimizing row count + column count',
        # 'minimizing row count * column count^2',
        'min_row_column_count',
        'min_column_row_count',
    ]
    LU_pivoting_methods = [
        # get_abs_max_pivot,
        # get_pivot_with_lowest_local_filling,
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation),
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_2),
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_3),
        get_pivot_from_min_row_column_count,
        get_pivot_from_min_column_row_count,
    ]
    QR_pivoting_methods_names = [
        'without pivoting',
        # 'minimizing row count * column count',
        # 'minimizing row count + column count',
        # 'minimizing row count * column count^2',
        # 'min_row_column_count',
        # 'min_column_row_count',
    ]
    QR_pivoting_methods = [
        without_pivoting,
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation),
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_2),
        # partial(get_pivot_with_lowest_local_filling_estimate, estimation=get_estimation_3),
        # get_pivot_from_min_row_column_count,
        # get_pivot_from_min_column_row_count,
    ]

    # test_table = [['Time']]
    for matrix in collection:
        # if matrix.n == 261:
        #     start = process_time()
        #     mm = matrix.multiply_by(matrix)
        #     end = process_time()
        #     test_table.append([f'{end - start}'])
        #
        #     start = process_time()
        #     mm_2 = matrix.multiply_by_2(matrix)
        #     end = process_time()
        #     test_table.append([f'{end - start}'])
        #     print(len(mm.values), len(mm_2.values))
        #     print(mm == mm_2)
        #     print(tabulate(test_table, tablefmt='fancy_grid', headers='firstrow'))
        # if matrix.n == 261:
        #     print(matrix.n)
        #     for idx, method in enumerate(QR_pivoting_methods):
        #         start = process_time()
        #         Q, R = QR_decompose(matrix)
        #         end = process_time()
        #         table.append([f'{matrix.n}', QR_pivoting_methods_names[idx], f'{len(matrix.values) / matrix.n**2}', f'{len(R.values) / R.n**2}', f'{len(R.values) / len(matrix.values)}', f'{end - start}'])
        #         print(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))
        if matrix.n == 420:
            print(matrix.n)
            for idx, method in enumerate(LU_pivoting_methods):
                start = process_time()
                LU, P, Q = LU_decompose(matrix, method)
                end = process_time()
                table.append([f'{matrix.n}', LU_pivoting_methods_names[idx], f'{len(matrix.values) / matrix.n**2}', f'{len(LU.values) / LU.n**2}', f'{len(LU.values) / len(matrix.values)}', f'{end - start}'])
                print(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))
                print(test(matrix, P, Q, LU))

    output(tabulate(table, tablefmt='fancy_grid', headers='firstrow'))


def func():
    a = Vector([1, 4], [0, 5])
    b = Vector([2, 3], [1, 5])
    print(a*b)


if __name__ == '__main__':
    main()
    # func()
